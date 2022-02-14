from django.shortcuts import render
from django.http import HttpResponse
from test.models import *
from django.forms.models import model_to_dict
# from django.template.defaultfilters import linebreaksbr

# `show_word_info` page
HIGHLIGHT_WORD_TEMPLATE = """
<span class="search-word-highlight">{}</span>
""".replace("\n", "")

# `show_definition` page
P_START = r"<div class='passage-text-para'>"
P_END = r"</div>"
# args: blank_id, blank_width, select_width
#   lem_name, blank_placeholder, lem_name(hint), ans
BLANK_E_TEMPLATE = {
    "choice-grammar": """<select class="form-select multiple-choice" style="width: {select_width}em;" id="blank_{blank_id}"></select>""", 
    "choice": """<span class="lem-blank" id="blank_{blank_id}" onclick="click_blank({blank_id})">{blank_placeholder}</span>""", 
    "blank": """<input type="text" class="test-blank" id="blank_{blank_id}" style="width: {blank_width}em;" placeholder="">
<div class="hint-btn" onclick="document.getElementById('blank_' + {blank_id}).placeholder='{hint}'">hint</div>
""".replace("\n", ""), 
}
HTML_TEMPLATE = {
    "choice-grammar": "test-chioce-0.html", # focus on grammar
    "choice": "test-standard.html", 
    "blank": "test-blank.html",
}
CHOICE_NUM = 4


def index(request):
    passages = Passage.objects.all()
    return render(request, "index.html", {"passages": passages})


def passage_handler(request):
    from json import loads
    passage_id = request.GET.get("p_id", None)
    lem_pos = loads(Passage.objects.get(id=passage_id).lemma_pos)
    lemma_list = []
    for lem_id in lem_pos:
        lem_id = int(lem_id)
        lemma_list.append(model_to_dict(Lemma.objects.get(id=lem_id)))
    return render(request, "select-words.html", {
        "words": lemma_list, 
        "p_id": passage_id, 
    })

# def render_lemma_defs(lemma):
#     lemma.def_en = linebreaksbr(lemma.def_en)
#     lemma.def_zh = linebreaksbr(lemma.def_zh)
#     return lemma


def render_sentence(text, word_pos_list):
    # return [(rendered_text, passage_title), ]
    # word_pos_list = {word1: [pos1, ], }
    pos_offset = 0
    for word in word_pos_list:
        for pos in word_pos_list[word]:
            word_len = len(word)
            word_e = HIGHLIGHT_WORD_TEMPLATE.format(word)
            text = text[:pos + pos_offset] + word_e + text[pos + pos_offset + word_len:]
            pos_offset += len(word_e) - word_len
    return text


def show_word_search_result(request):
    from json import loads, dumps
    search_word = request.POST.get("word")
    match_word = Word.objects.filter(name=search_word)
    if match_word.exists():
        lemma = Lemma.objects.get(id=match_word.first().lem_id)
        sent_ids = lemma.sent_ids
        sentences = [] # [(rendered_text, passage_obj), ]
        if sent_ids:
            sent_ids_changed = False
            sent_ids = loads(sent_ids)
            new_sent_ids = sent_ids.copy() # del sent_id when sent deleted
            for s_id in sent_ids:
                sent_objs = Sentence.objects.filter(id=s_id)
                if sent_objs.exists():
                    sent_obj = sent_objs.first()
                    sentences.append((
                        render_sentence(sent_obj.text, sent_ids[s_id]), 
                        Passage.objects.get(id=sent_obj.passage_id), 
                    ))
                else:
                    # pop when sent deleted
                    new_sent_ids.pop(s_id)
                    sent_ids_changed = True
            if sent_ids_changed:
                lemma.sent_ids = dumps(new_sent_ids)
                lemma.save()
        return render(request, "show_word_info.html", {
            "lemma": lemma, 
            "sentences": sentences, 
        })
    return render(request, "error-message.html", {
        "error_message": "'%s' does not exist\nTry another word" % search_word, 
    })


def show_definition(request):
    passage_id = request.POST.get("p_id")
    lemma_id = request.POST.get("lemma_id")
    if (lemma_id):
        lemma_id = [int(w_id) for w_id in lemma_id.split(',')]
    else:
        lemma_id = []
    lemmas = []
    lem_cnt = 0
    for lem_id in lemma_id:
        lem_obj = Lemma.objects.get(id=lem_id)
        if lem_obj.def_en or lem_obj.def_zh:
            lem_cnt += 1
            lemmas.append(model_to_dict(lem_obj))
    return render(request, "show-definition.html", {
        "p_id": passage_id, 
        "lemmas": lemmas, 
        "lemma_id": lemma_id, 
        "lem_cnt": lem_cnt, 
    })


def blank_rep_init(lemma_pos, request):
    blank_rep_buf = []
    hints = []
    ans = {}
    blank_id = 0
    lemma_id = request.POST.get("lemma_id")
    if (lemma_id):
        lemma_id = lemma_id.split(',')
    else:
        lemma_id = []
    for lem_id in lemma_pos:
        if lem_id not in lemma_id:
            continue
        lem_name = Lemma.objects.get(id=lem_id).name
        cur_lemma_hint = []
        for word_id, pos_list in lemma_pos[lem_id]:
            word_name = Word.objects.get(id=word_id).name
            cur_lemma_hint.append((word_name, int(word_id)))
            for pos in pos_list:
                blank_id += 1
                ans[blank_id] = {"id": int(word_id), "name": word_name}
                blank_rep_buf.append((pos, len(word_name), blank_id, word_name, lem_name, lem_id))
        hints.append((lem_id, lem_name, cur_lemma_hint))
    blank_rep_buf.sort(key=lambda x: x[0])
    # blank_rep_buf = [(pos, word_len, blank_id, word_name, lem_name, lem_id), ]
    # hints = [
    #     (lemma.name, lemma.id, [(word1, word1.id), ]), 
    # ]
    # ans = {blank_id: {"id": ans_id, "name": ans}, }
    return blank_rep_buf, hints, ans


def get_grammar_choices(ans_lem_id, ans):
    # return [ans, wrong_choice1, ]
    # all choices from same lemma
    from random import sample, choice
    word_objs = Word.objects.filter(lem_id=ans_lem_id)
    choices = sample(list(word_objs), min(CHOICE_NUM + 1, len(word_objs)))
    choices = [word_obj.name for word_obj in choices if word_obj.name != ans]
    choices = [ans] + choices
    # print(choices)
    return choices


def test_passage(request):
    mode = request.POST.get("test_mode")
    passage_id = request.POST.get("p_id")
    passage = Passage.objects.get(id=passage_id)
    text = passage.text
    
    from json import loads
    pos_offset = 0
    blank_rep_buf, hints, ans = blank_rep_init(loads(passage.lemma_pos), request)

    # for "choice-grammar"
    # {blank_id: [ans, wrong_choice1, ], }
    choices = {}

    for pos, word_len, blank_id, word_name, lem_name, lem_id in blank_rep_buf:
        blank_e = BLANK_E_TEMPLATE[mode].format(
            blank_id=blank_id, 
            blank_width=word_len/2 + 1, 
            select_width=word_len/1.5 + 3, 
            hint=lem_name, 
            blank_placeholder="_____", 
        )
        text = text[:pos + pos_offset] + blank_e + text[pos + pos_offset + word_len:]
        pos_offset += len(blank_e) - word_len
        choices[blank_id] = get_grammar_choices(lem_id, word_name)
    text = P_START + text.replace("\n", P_END + P_START) + P_END
    context = {
        "passage_text": text, 
        "passage_title": passage.title, 
        "hints": sorted(hints, key=lambda x: x[0]),
        "ans": ans, # {blank_id: {"id": ans_id, "name": ans}, }
    }
    if mode == "choice-grammar":
        context["choices"] = choices
    return render(request, HTML_TEMPLATE[mode], context)





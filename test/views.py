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
CHOICE_TEST_TEMPLATE = """
<span class="lem-blank" id="blank_{}" onclick="click_blank({})">{}</span>
""".replace("\n", "")
BLANK_TEST_TEMPLATE = """
<input type="text" class="test-blank" id="blank_{}" style="width: {}em;" placeholder="">
<div class="hint-btn" onclick="document.getElementById('blank_' + {}).placeholder='{}'">hint</div>
""".replace("\n", "")


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
    from json import loads
    search_word = request.POST.get("word")
    match_word = Word.objects.filter(name=search_word)
    if match_word.exists():
        lemma = Lemma.objects.get(id=match_word.first().lem_id)
        sent_ids = lemma.sent_ids
        sentences = [] # [(rendered_text, passage_title), ]
        if sent_ids:
            sent_ids = loads(sent_ids)
            for s_id in sent_ids:
                sent_obj = Sentence.objects.get(id=s_id)
                sentences.append((
                    render_sentence(sent_obj.text, sent_ids[s_id]), 
                    Passage.objects.get(id=sent_obj.passage_id).title, 
                    sent_obj.passage_id, 
                ))
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
                blank_rep_buf.append((pos, len(word_name), blank_id, lem_name))
        hints.append((lem_id, lem_name, cur_lemma_hint))
    blank_rep_buf.sort(key=lambda x: x[0])
    # blank_rep_buf = {(pos, word_len, blank_id), }
    # hints = [
    #     (lemma.name, lemma.id, [(word1, word1.id), ]), 
    # ]
    # ans = {blank_id: {"id": ans_id, "name": ans}, }
    return blank_rep_buf, hints, ans


def test_passage(request):
    test_mode = request.POST.get("test_mode");
    passage_id = request.POST.get("p_id")
    passage = Passage.objects.get(id=passage_id)
    text = passage.text
    
    from json import loads

    blank_e_template = CHOICE_TEST_TEMPLATE if test_mode == "choice" else BLANK_TEST_TEMPLATE
    pos_offset = 0
    blank_rep_buf, hints, ans = blank_rep_init(loads(passage.lemma_pos), request)
    for pos, word_len, blank_id, lem_name in blank_rep_buf:
        if test_mode == "choice":
            blank_e = blank_e_template.format(blank_id, blank_id, "_"*5)
        else:
            blank_e = blank_e_template.format(blank_id, word_len/2 + 1, blank_id, lem_name)
        text = text[:pos + pos_offset] + blank_e + text[pos + pos_offset + word_len:]
        pos_offset += len(blank_e) - word_len
    text = P_START + text.replace("\n", P_END + P_START) + P_END

    return render(request, "test-standard.html" if test_mode == "choice" else "test-blank.html", {
        "passage_text": text, 
        "passage_title": passage.title, 
        "hints": sorted(hints, key=lambda x: x[0]), 
        "ans": ans, 
    })


from django.shortcuts import render
from django.http import HttpResponse
from test.models import Word, Lemma, Passage
from django.forms.models import model_to_dict


def select_passage(request):
    passages = Passage.objects.all()
    return render(request, "select-passage.html", {"passages": passages})


def passage_handler(request):
    from json import loads
    passage_id = request.GET.get("p_id", None)
    lem_pos = loads(Passage.objects.get(id=passage_id).lemma_pos)
    lemma_list = []
    for lem_id in lem_pos:
        lem_id = int(lem_id)
        lemma_list.append(model_to_dict(Lemma.objects.get(id=lem_id)))
    return render(request, "select-words.html", \
        {"words": lemma_list, "p_id": passage_id})

def show_definition(request):
    passage_id = request.POST.get("p_id")
    lemma_id = request.POST.get("lemma_id")
    if (lemma_id):
        lemma_id = [int(w_id) for w_id in lemma_id.split(',')]
    else:
        lemma_id = []
    lemmas = []
    lem_cnt = 0
    str_defs = {}
    for lem_id in lemma_id:
        lem_cnt += 1
        lem_obj = Lemma.objects.get(id=lem_id)
        lemmas.append(model_to_dict(lem_obj))
        str_defs[lem_id] = [lem_obj.def_en, lem_obj.def_zh]
    return render(request, "show-definition.html", {
        "p_id": passage_id, 
        "lemmas": lemmas, 
        "lemma_id": lemma_id, 
        "lem_cnt": lem_cnt, 
        "str_defs": str_defs, 
    })
    


def test_passage(request):
    from json import loads
    hints = []
    passage_id = request.POST.get("p_id")
    p_start = r"<div class='passage-text'>"
    p_end = r"</div>"
    lemma_id = request.POST.get("lemma_id")
    if (lemma_id):
        lemma_id = lemma_id.split(',')
    else:
        lemma_id = []
    selected_defs_id = [int(i) for i in lemma_id]
    passage = Passage.objects.get(id=passage_id)
    text = passage.text
    e_blank = """<span class="word-blank" id="blank_{}" onclick="click_blank({})">{}</span>"""
    ans = {} # {blank_id: ans_id, }

    global blank_id, ans_id
    blank_id = 1

    def get_e_blank(arg):
        global blank_id
        blank_id += 1
        ans[blank_id] = ans_id;
        return e_blank.format(blank_id, blank_id, "_"*5)

    lemma_pos = loads(passage.lemma_pos)
    for lem_id in lemma_pos:
        if lem_id not in lemma_id:
            continue
        for word_len, pos_list in lemma_pos[lem_id]:
            for pos in pos_list:
                text = text[:pos] + "_"*word_len + text[pos + word_len:]
    print(lemma_id)
    text = p_start + text.replace("\n", p_end + p_start) + p_end
    # for paragraph in loads(passage.text_expand):
    #     for word, lemma, tag, word_id in paragraph:
    #         word_def = Word.objects.filter(id=word_id).first() if word_id else None
    #         if word_def and word_def.def_id in selected_defs_id:
    #             ans_id = word_id;
    #             text = sub(r"\b%s\b" % word, get_e_blank, text)
    #             hints.append((word, ans_id))

    return render(request, "test-passage.html", {
        "passage_text": text, 
        "passage_title": passage.title, 
        "hints": sorted(hints, key=lambda x: x[0]), 
        "ans": ans, 
    })


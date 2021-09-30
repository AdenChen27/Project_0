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
    for lem_id in lemma_id:
        lem_cnt += 1
        lemmas.append(model_to_dict(Lemma.objects.get(id=lem_id)))
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
        word_name_list = []
        for word_id, word_len, pos_list in lemma_pos[lem_id]:
            word_name_list.append(Word.objects.get(id=word_id).name)
            for pos in pos_list:
                blank_id += 1
                ans[blank_id] = int(lem_id)
                blank_rep_buf.append((pos, word_len, blank_id))
        hints.append((Lemma.objects.get(id=lem_id).name, int(lem_id), word_name_list))
    blank_rep_buf.sort(key=lambda x: x[0])
    return blank_rep_buf, hints, ans
    

def test_passage(request):
    from json import loads
    passage_id = request.POST.get("p_id")
    p_start = r"<div class='passage-text'>"
    p_end = r"</div>"
    passage = Passage.objects.get(id=passage_id)
    text = passage.text
    blank_e_template = """<span class="lem-blank" id="blank_{}" onclick="click_blank({})">{}</span>"""
    pos_offset = 0
    blank_rep_buf, hints, ans = blank_rep_init(loads(passage.lemma_pos), request)
    # blank_rep_buf = {(pos, word_len, blank_id), }
    # ans = {blank_id: ans_id, }
    for pos, word_len, blank_id in blank_rep_buf:
        blank_e = blank_e_template.format(blank_id, blank_id, "_"*5)
        text = text[:pos + pos_offset] + blank_e + text[pos + pos_offset + word_len:]
        pos_offset += len(blank_e) - word_len
    text = p_start + text.replace("\n", p_end + p_start) + p_end

    return render(request, "test-passage.html", {
        "passage_text": text, 
        "passage_title": passage.title, 
        "hints": sorted(hints, key=lambda x: x[0]), 
        "ans": ans, 
    })


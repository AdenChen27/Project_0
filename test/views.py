from django.shortcuts import render
from django.http import HttpResponse
from test.models import Passage, Word
from django.forms.models import model_to_dict


def select_passage(request):
    passages = Passage.objects.all()
    return render(request, "select-passage.html", {"passages": passages})


def passage_handler(request):
    passage_id = request.GET.get("p_id", None)
    words = Word.objects.filter(p_id=int(passage_id))
    word_list = []
    for word in words:
        word_list.append(model_to_dict(word))
    return render(request, "select-words.html", {"words": word_list, "p_id": passage_id})

def show_definition(request):
    from test.models import WordDef
    from json import loads
    passage_id = request.POST.get("p_id")
    words_id = request.POST.get("words_id")
    if (words_id):
        words_id = [int(w_id) for w_id in words_id.split(',')]
    else:
        words_id = []
    words = []
    words_cnt = 0
    str_defs = [""]
    for w_id in words_id:
        words_cnt += 1
        word = WordDef.objects.get(id=w_id)
        defs = loads(word.definition)
        words.append({"id": words_cnt, "name": word.name, "defs": defs})
        if defs:
            str_defs.append(";\n".join(
                [str(key + ": " + ",".join(defs[key])) for key in defs]
                ))
    return render(request, "show-definition.html", {
        "p_id": passage_id, 
        "words": words, 
        "words_id": words_id, 
        "words_cnt": words_cnt, 
        "str_defs": str_defs, 
    })
    


def test_passage(request):
    from re import sub
    from json import loads
    hints = []
    passage_id = request.POST.get("p_id")
    p_start = r"<div class='passage-text'>"
    p_end = r"</div>"
    selected_defs_id = [int(i) for i in request.POST.get("words_id").split(',')]
    passage = Passage.objects.get(id=passage_id)
    text = p_start + passage.text.replace("\n", p_end + p_start) + p_end
    e_blank = """<span class="word-blank" id="blank_{}" onclick="click_blank({})">{}</span>"""
    ans = {}

    global blank_id, ans_id
    blank_id = 1

    def get_e_blank(arg):
        global blank_id
        blank_id += 1
        ans[blank_id] = ans_id;
        return e_blank.format(blank_id, blank_id, "_"*5)

    for paragraph in loads(passage.text_expand):
        for word, lemma, tag, word_id in paragraph:
            word_def = Word.objects.filter(id=word_id).first() if word_id else None
            if word_def and word_def.def_id in selected_defs_id:
                ans_id = word_id;
                text = sub(r"\b%s\b" % word, get_e_blank, text)
                hints.append((word, ans_id))

    return render(request, "test-passage.html", {
        "passage_text": text, 
        "passage_title": passage.title, 
        "hints": sorted(hints, key=lambda x: x[0]), 
        "ans": ans, 
    })


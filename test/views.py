from django.shortcuts import render
from django.http import HttpResponse
from test.models import *
from django.forms.models import model_to_dict
from django.utils.translation import gettext as _
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
<div class="hint-btn" onclick="document.getElementById('blank_' + {blank_id}).value='{hint}'">hint</div>
""".replace("\n", ""),
}
HTML_TEMPLATE = {
    "choice-grammar": "test-chioce-0.html",  # focus on grammar
    "choice": "test-standard.html",
    "blank": "test-blank.html",
}
CHOICE_NUM = 4

app_system_info = SystemInfo.objects.first()


# author page
def main_page(request):
    return render(request, "author-page.html", {"view_count": app_system_info.counter})


# renew view counter
# return Passage list
def index_page(request):
    app_system_info.counter_add()
    passages = list(Passage.objects.all())
    passages.sort(key=lambda x: x.title)
    return render(request, "index.html", {
        "passages": passages,
        "user": request.session.get('name', ''),
        "view_count": app_system_info.counter,
    })


# return a page that jumps back to index
def jump_to_index(request):
    return render(request, "jump-to-index.html")


def login_page(request, login_error="", register_error="", init_page="login"):
    return render(request, "login.html", {
        "init_page": init_page,  # login/register
        "login_error": login_error,
        "register_error": register_error,
    })


def login_action(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if User.objects.filter(username=username).exists() and \
                User.objects.get(username=username).password == password:
            request.session['name'] = User.objects.get(username=username).name
            return jump_to_index(request)
        else:
            return login_page(
                request,
                init_page="login",
                login_error="username or password is incorrect"
            )


def register_action(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if User.objects.filter(username=username).exists():
            return login_page(
                request,
                init_page="register",
                register_error="username already in use. pick another one."
            )
        else:
            User(name=name, username=username, password=password).save()
            request.session['name'] = name
            return jump_to_index(request)
            # set language_code


def select_words_page(request):
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


# return [(rendered_text, passage_title), ]
def render_sentence(text, word_pos_list):
    # word_pos_list = {word1: [pos1, ], }
    pos_offset = 0
    for word in word_pos_list:
        for pos in word_pos_list[word]:
            word_len = len(word)
            word_e = HIGHLIGHT_WORD_TEMPLATE.format(word)
            text = text[:pos + pos_offset] + word_e + \
                text[pos + pos_offset + word_len:]
            pos_offset += len(word_e) - word_len
    return text


def show_word_info_page(request):
    from json import loads, dumps
    search_word = request.POST.get("word").lower()
    match_word = Word.objects.filter(name=search_word)
    if match_word.exists():
        lemma = Lemma.objects.get(id=match_word.first().lem_id)
        sent_ids = lemma.sent_ids
        sentences = []  # [(rendered_text, passage_obj), ]
        if sent_ids:
            sent_ids_changed = False
            sent_ids = loads(sent_ids)
            new_sent_ids = sent_ids.copy()  # del sent_id when sent deleted
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


def show_definition_page(request):
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


def quiz_render_init(text_lemma_pos, request):
    word_render_list = []
    # word_render_list = [(pos, render_args), ]
    # render_args = {blank_id, word_len, word_name, lem_name, lem_id}

    # hints for test-standard
    hints = []
    # hints = [
    #     (lemma.name, lemma.id, [(word1, word1.id), ]),
    # ]
    ans = {}
    # ans = {blank_id: {"id": ans_id, "name": ans}, }
    
    tmp_blank_id = 0

    # get lemma id list of words to be quizzed
    lemma_id = request.POST.get("lemma_id")
    if (lemma_id):
        lemma_id = lemma_id.split(',')
    else:
        lemma_id = []


    for lem_id in text_lemma_pos:
        if lem_id not in lemma_id:
            continue

        lem_name = Lemma.objects.get(id=lem_id).name
        cur_lemma_hint = []

        for word_id, pos_list in text_lemma_pos[lem_id]:
            word_name = Word.objects.get(id=word_id).name
            cur_lemma_hint.append((word_name, int(word_id)))

            for pos in pos_list:
                tmp_blank_id += 1
                ans['t' + str(tmp_blank_id)] = {"id": int(word_id), "name": word_name}
                render_args = {
                    "blank_id": 't' + str(tmp_blank_id),
                    "word_len": len(word_name),
                    "word_name": word_name,
                    "lem_name": lem_name,
                    "lem_id": lem_id,
                }
                word_render_list.append((pos, render_args))
        hints.append((lem_id, lem_name, cur_lemma_hint))

    # sort by `pos` from smallest to greatest
    word_render_list.sort(key=lambda x: x[0])

    # reassign `blank_id` so that blank with smaller `pos` have smaller `blank_id`
    blank_id = 0
    for i in range(len(word_render_list)):
        blank_id += 1
        ans[blank_id] = ans.pop(word_render_list[i][1]["blank_id"], None)
        word_render_list[i][1]["blank_id"] = blank_id

    return word_render_list, hints, ans


# return [ans, wrong_choice1, ]
# all choices from same lemma
def get_grammar_choices(ans_lem_id, ans):
    from random import sample, choice
    word_objs = Word.objects.filter(lem_id=ans_lem_id)
    choices = sample(list(word_objs), min(CHOICE_NUM + 1, len(word_objs)))
    choices = [word_obj.name for word_obj in choices if word_obj.name != ans]
    choices = [ans] + choices
    return choices


# wrap each paragraoh with <p> tag and
#   replace words to be tested in text with empty <span> tag
# <span>.id: `blank_{id}`
def render_text(text, word_render_list):
    pos_offset = 0
    for pos, word_render_args in word_render_list:
        word_len = word_render_args["word_len"]
        # blank_id = word_render_args["blank_id"]
        # word_name = word_render_args["word_name"]
        # lem_name = word_render_args["lem_name"]
        # lem_id = word_render_args["lem_id"]

        # replacement = "<span id='blank_{blank_id}'></span>".format(
        replacement = "<span id='blank_{blank_id}'></span>".format(
            blank_id=word_render_args["blank_id"],
        )
        text = text[:pos + pos_offset] + replacement + \
            text[pos + pos_offset + word_len:]
        pos_offset += len(replacement) - word_len
        # choices[blank_id] = get_grammar_choices(lem_id, word_name)
    return P_START + text.replace("\n", P_END + P_START) + P_END


# return rendered multiple choice quiz page
def multiple_choice_quiz_page(request):
    from json import loads
    passage_id = request.POST.get("p_id")
    passage = Passage.objects.get(id=passage_id)
    passage.counter_add()
    text = passage.text
    word_render_list, hints, ans = quiz_render_init(
        loads(passage.lemma_pos), request)

    return render(request, "quiz-choice.html", {
        "passage_text": render_text(text, word_render_list),
        "ans": ans,
    })


def test_passage_page(request):
    mode = request.POST.get("test_mode")
    if mode == "choice-grammar":
        return multiple_choice_quiz_page(request)

    passage_id = request.POST.get("p_id")
    passage = Passage.objects.get(id=passage_id)
    passage.counter_add()
    text = passage.text

    from json import loads
    pos_offset = 0
    word_render_list, hints, ans = quiz_render_init(
        loads(passage.lemma_pos), request)
    # {blank_id: [ans, wrong_choice1, ], }
    choices = {}

    for pos, word_render_args in word_render_list:
        word_len = word_render_args["word_len"]
        blank_id = word_render_args["blank_id"]
        word_name = word_render_args["word_name"]
        lem_name = word_render_args["lem_name"]
        lem_id = word_render_args["lem_id"]

        blank_e = BLANK_E_TEMPLATE[mode].format(
            blank_id=blank_id,
            blank_width=word_len/2 + 1,
            select_width=word_len/1.5 + 3,
            hint=lem_name,
            blank_placeholder="_____",
        )
        text = text[:pos + pos_offset] + blank_e + \
            text[pos + pos_offset + word_len:]
        pos_offset += len(blank_e) - word_len
        choices[blank_id] = get_grammar_choices(lem_id, word_name)
    text = P_START + text.replace("\n", P_END + P_START) + P_END
    context = {
        "passage_text": text,
        "passage_title": passage.title,
        "hints": sorted(hints, key=lambda x: x[0]),
        "ans": ans,  # {blank_id: {"id": ans_id, "name": ans}, }
    }
    if mode == "choice-grammar":
        context["choices"] = choices
    return render(request, HTML_TEMPLATE[mode], context)

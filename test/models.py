from django.db import models
from django_mysql.models import ListCharField as model_ListCharField
from jsonfield import JSONField


from functools import wraps
from time import time

def timer(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        # print("func:%r args:[%r, %r] took: %2.4f sec" % \
          # (f.__name__, args, kw, te - ts))
        print("[t]func:%s took: %2.4fs" % (f.__name__, te - ts))
        return result
    return wrap


PASSAGE_TITLE_MAX_LEN = 100
PASSAGE_AUTHOR_MAX_LEN = 100
TAG_MAX_NUM = 5
WORD_MAX_LEN = 34


class Lemma(models.Model):
    name = models.CharField(max_length=WORD_MAX_LEN, default="")
    freq = models.IntegerField(default=0)
    def_en = models.TextField(default="", blank=True)
    def_zh = models.TextField(default="", blank=True)
    sent_ids = JSONField(null=True)
    # {sentence_id1: {word1: [pos1, ], }, }

    def __str__(self):
        return self.name


class Word(models.Model):
    name = models.CharField(max_length=WORD_MAX_LEN, default="")
    lem_id = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Sentence(models.Model):
    passage_id = models.IntegerField(default=0)
    text = models.TextField(default="")

    def __str__(self):
        return self.text


def get_lem_word_map(text):
    from nltk.corpus import stopwords
    from re import findall
    stop_words = set(stopwords.words("english"))
    all_words = set(findall(r"'?\w+", text))
    lem_word_map = {}
    for word in all_words:
        if word in stop_words:
            continue
        word_objs = Word.objects.filter(name=word)
        if not word_objs.exists():
            continue
        lem_id = word_objs.first().lem_id
        word_id = word_objs.first().id
        if lem_id not in lem_word_map:
            lem_word_map[lem_id] = []
        lem_word_map[lem_id].append((word_id, word))
    return lem_word_map # {lem_id1: [(word1id, word1.name), ], }


def find_all_word_pos(word, text):
    import re
    if word[0] == "'":
        reg = r"(%s)(\W|'|$)" % (word)
        return [w.start() for w in re.finditer(reg, text)]
    else:
        reg = r"(\W|')(%s)(\W|'|$)" % (word)
        reg2 = r"^(%s)(\W|'|$)" % (word)
        return [w.start() + 1 for w in re.finditer(reg, text)] + \
            [w.start() + 1 for w in re.finditer(reg2, text)]


@timer
def get_lemma_pos_string(text):
    from json import dumps
    lemma_pos = {}
    lem_word_map = get_lem_word_map(text)
    for lem_id in lem_word_map:
        for word_id, word in lem_word_map[lem_id]:
            if lem_id not in lemma_pos:
                lemma_pos[lem_id] = []
            pos_list = find_all_word_pos(word, text)
            lemma_pos[lem_id].append((word_id, pos_list))
    # {lemma1.id: [(word1.id, len(word1.name), [pos1, ]), ], }
    return dumps(lemma_pos)


def add_words(sentence, s_id, stop_words):
    from nltk.tokenize import word_tokenize
    from json import loads, dumps
    words = word_tokenize(sentence)
    for word in words:
        if word in stop_words:
            continue
        word_objs = Word.objects.filter(name=word)
        if not word_objs.exists():
            continue
        lemma = Lemma.objects.get(id=word_objs.first().lem_id)
        sent_ids = loads(lemma.sent_ids) if lemma.sent_ids else {}
        all_pos = find_all_word_pos(word, sentence)
        if s_id not in sent_ids:
            sent_ids[s_id] = {}
        if word not in sent_ids[s_id]:
            sent_ids[s_id][word] = []
        sent_ids[s_id][word].extend(all_pos)
        # sent_ids = {sentence_id1: {word1: [pos1, ], }, }
        lemma.sent_ids = dumps(sent_ids)
        lemma.save()

# def temp():
#     from nltk.corpus import stopwords
#     stop_words = list(stopwords.words("english"))
#     stop_words.extend([',', '.', '?', '!'])
#     for sent in Sentence.objects.all():
#         add_words(sent.text, sent.id, stop_words)
#         if i % 10000 == 0:
#             print("done", i)


@timer
def add_sentences_to_db(p_id, p_text):
    # delete all `Sentence` with same `passage_id`
    # add all sentences in passage to db
    # link `Lemma` to newly created `Sentence` for lemma of each word in passage
    if Sentence.objects.filter(passage_id=p_id).exists():
        Sentence.objects.filter(passage_id=p_id).delete()
    from nltk.corpus import stopwords
    from nltk.tokenize import sent_tokenize
    sentences = sent_tokenize(p_text)
    stop_words = list(stopwords.words("english"))
    stop_words.extend([',', '.', '?', '!'])
    for sentence in sentences:
        new_sent = Sentence(passage_id=p_id, text=sentence)
        new_sent.save()
        add_words(sentence, new_sent.id, stop_words)


class Passage(models.Model):
    title = models.CharField(max_length=PASSAGE_TITLE_MAX_LEN)
    author = models.CharField(max_length=PASSAGE_AUTHOR_MAX_LEN, default="")
    text = models.TextField(default="")
    lemma_pos = models.TextField(default="", blank=True)
    # {lemma1.id: [(word1.id, len(word1.name), [pos1, ]), ], }
    counter = models.IntegerField(default=0) # test count
    tags = model_ListCharField(
        base_field=models.CharField(max_length=WORD_MAX_LEN), 
        size=TAG_MAX_NUM, 
        max_length=TAG_MAX_NUM*(WORD_MAX_LEN + 1), 
        default=""
    )

    def counter_add(self):
        self.counter += 1
        self.save()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # generate `lemma_pos`
        if not self.lemma_pos:
            self.lemma_pos = get_lemma_pos_string(self.text)
        # creat `Lemma` to `Sentence` mappings
        super().save(*args, **kwargs)
        if not Sentence.objects.filter(passage_id=self.id).exists():
            add_sentences_to_db(self.id, self.text)


# one instance only, for storing system information
class System(models.Model):
    counter = models.IntegerField(default=0) # total visit

    def counter_add(self):
        self.counter += 1
        self.save()


def del_passage(p_id):
    # del passage & sentences
    Passage.objects.get(id=p_id).delete()
    if Sentence.objects.filter(passage_id=p_id).exists():
        Sentence.objects.filter(passage_id=p_id).delete()


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


# passage
PASSAGE_TITLE_MAX_LEN = 100
PASSAGE_AUTHOR_MAX_LEN = 100
TAG_MAX_NUM = 5
# word
WORD_MAX_LEN = 34
# user
FIRST_NAME_MAX_LEN = 15
LAST_NAME_MAX_LEN = 15
PASSWORD_MAX_LEN = 32
LANGUAGE_CODE_MAX_LEN = 2


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
    return lem_word_map  # {lem_id1: [(word1id, word1.name), ], }


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


# delete all `Sentence` with same `passage_id`
# add all sentences in passage to db
# link `Lemma` to newly created `Sentence` for lemma of each word in passage
@timer
def add_sentences_to_db(p_id, p_text):
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


def count_syllable(word):
    if len(word) <= 1:
        return int(word == 'a')  # filter punctuations
    word = word.lower()
    vowels = "aeiouy"
    count = 0
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count


# from https://eayd.in/?p=232
def count_syllable_2(word):
    import re
    word = word.lower()

    # exception_add are words that need extra syllables
    # exception_del are words that need less syllables

    exception_add = ['serious', 'crucial']
    exception_del = ['fortunately', 'unfortunately']

    co_one = ['cool', 'coach', 'coat', 'coal', 'count', 'coin', 'coarse',
              'coup', 'coif', 'cook', 'coign', 'coiffe', 'coof', 'court']
    co_two = ['coapt', 'coed', 'coinci']

    pre_one = ['preach']

    syls = 0  # added syllable number
    disc = 0  # discarded syllable number

    # 1) if letters < 3 : return 1
    if len(word) <= 3:
        syls = 1
        return syls

    # 2) if doesn't end with "ted" or "tes" or "ses" or "ied" or "ies", discard "es" and "ed" at the end.
    # if it has only 1 vowel or 1 set of consecutive vowels, discard. (like "speed", "fled" etc.)

    if word[-2:] == "es" or word[-2:] == "ed":
        doubleAndtripple_1 = len(re.findall(r'[eaoui][eaoui]', word))
        if doubleAndtripple_1 > 1 or len(re.findall(r'[eaoui][^eaoui]', word)) > 1:
            if word[-3:] == "ted" or word[-3:] == "tes" or word[-3:] == "ses" or word[-3:] == "ied" or word[-3:] == "ies":
                pass
            else:
                disc += 1

    # 3) discard trailing "e", except where ending is "le"

    le_except = ['whole', 'mobile', 'pole', 'male', 'female',
                 'hale', 'pale', 'tale', 'sale', 'aisle', 'whale', 'while']

    if word[-1:] == "e":
        if word[-2:] == "le" and word not in le_except:
            pass

        else:
            disc += 1

    # 4) check if consecutive vowels exists, triplets or pairs, count them as one.

    doubleAndtripple = len(re.findall(r'[eaoui][eaoui]', word))
    tripple = len(re.findall(r'[eaoui][eaoui][eaoui]', word))
    disc += doubleAndtripple + tripple

    # 5) count remaining vowels in word.
    numVowels = len(re.findall(r'[eaoui]', word))

    # 6) add one if starts with "mc"
    if word[:2] == "mc":
        syls += 1

    # 7) add one if ends with "y" but is not surrouned by vowel
    if word[-1:] == "y" and word[-2] not in "aeoui":
        syls += 1

    # 8) add one if "y" is surrounded by non-vowels and is not in the last word.

    for i, j in enumerate(word):
        if j == "y":
            if (i != 0) and (i != len(word)-1):
                if word[i-1] not in "aeoui" and word[i+1] not in "aeoui":
                    syls += 1

    # 9) if starts with "tri-" or "bi-" and is followed by a vowel, add one.

    if word[:3] == "tri" and word[3] in "aeoui":
        syls += 1

    if word[:2] == "bi" and word[2] in "aeoui":
        syls += 1

    # 10) if ends with "-ian", should be counted as two syllables, except for "-tian" and "-cian"

    if word[-3:] == "ian":
        # and (word[-4:] != "cian" or word[-4:] != "tian") :
        if word[-4:] == "cian" or word[-4:] == "tian":
            pass
        else:
            syls += 1

    # 11) if starts with "co-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.

    if word[:2] == "co" and word[2] in 'eaoui':

        if word[:4] in co_two or word[:5] in co_two or word[:6] in co_two:
            syls += 1
        elif word[:4] in co_one or word[:5] in co_one or word[:6] in co_one:
            pass
        else:
            syls += 1

    # 12) if starts with "pre-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.

    if word[:3] == "pre" and word[3] in 'eaoui':
        if word[:6] in pre_one:
            pass
        else:
            syls += 1

    # 13) check for "-n't" and cross match with dictionary to add syllable.

    negative = ["doesn't", "isn't", "shouldn't", "couldn't", "wouldn't"]

    if word[-3:] == "n't":
        if word in negative:
            syls += 1
        else:
            pass

    # 14) Handling the exceptional words.

    if word in exception_del:
        disc += 1

    if word in exception_add:
        syls += 1

    # calculate the output
    return numVowels - disc + syls


# return Flesch-Kincaid Grade Level = (.39 * ASL) + (11.8 * ASW) - 15.59
def get_text_difficulty(text):
    from nltk import word_tokenize, sent_tokenize
    sents = sent_tokenize(text)
    syllable_cnt = 0
    word_cnt = 0
    sent_cnt = len(sents)

    for sent in sents:
        # `sent_tokenize` does not separate sentences connected by dashes
        sent_cnt += sent.count(" - ") + sent.count(" — ")

        words = word_tokenize(sent)
        for word in words:
            if len(word) <= 1:
                # 'a'
                if word == 'a':
                    word_cnt += 1
                    syllable_cnt += 1
            else:
                word_cnt += 1
                syllable_cnt += count_syllable_2(word)
            # syllable_cnt += sylco(word)

    asl = word_cnt/sent_cnt
    # average sentence length (average number of words per sentence)
    asw = syllable_cnt/word_cnt
    # average number of syllables per word
    return .39*asl + 11.8*asw - 15.59


class Passage(models.Model):
    title = models.CharField(max_length=PASSAGE_TITLE_MAX_LEN)
    author = models.CharField(
        max_length=PASSAGE_AUTHOR_MAX_LEN,
        default="",
        blank=True
    )
    text = models.TextField(default="")
    lemma_pos = models.TextField(default="", blank=True)
    # {lemma1.id: [(word1.id, len(word1.name), [pos1, ]), ], }
    # test count
    counter = models.IntegerField(default=0)
    # Flesch–Kincaid Level
    difficulty = models.FloatField(default=0, blank=True)

    tags = model_ListCharField(
        base_field=models.CharField(max_length=WORD_MAX_LEN),
        size=TAG_MAX_NUM,
        max_length=TAG_MAX_NUM*(WORD_MAX_LEN + 1),
        default="",
        blank=True,
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
        if not self.difficulty:
            self.difficulty = get_text_difficulty(self.text)

        super().save(*args, **kwargs)

        # creat `Lemma` to `Sentence` mappings
        if not Sentence.objects.filter(passage_id=self.id).exists():
            add_sentences_to_db(self.id, self.text)


class User(models.Model):
    name = models.CharField(max_length=FIRST_NAME_MAX_LEN, default="")
    username = models.CharField(max_length=LAST_NAME_MAX_LEN, default="")
    # stored in md5
    password = models.CharField(max_length=PASSWORD_MAX_LEN, default="")

    # ISO 639-1 Code
    language_code = models.CharField(
        max_length=LANGUAGE_CODE_MAX_LEN,
        default=""
    )
    points = models.IntegerField(default=0)

    tests_taken = models.IntegerField(default=0)
    words_studied = models.IntegerField(default=0)

    # 0 -> root; 1 -> administrators; 10 -> users (default)
    permission = models.IntegerField(default=10)

    def points_add(self, v):
        self.points += v
        self.save()

    def tests_taken_add(self):
        self.tests_taken += 1
        self.save()

    def words_studied_add(self, v):
        self.words_studied += v
        self.save()


# one instance only, for storing system information
class SystemInfo(models.Model):
    counter = models.IntegerField(default=0)  # total visit

    def counter_add(self):
        self.counter += 1
        self.save()


# del passage & sentences in the passage
def del_passage(p_id):
    Passage.objects.get(id=p_id).delete()
    if Sentence.objects.filter(passage_id=p_id).exists():
        Sentence.objects.filter(passage_id=p_id).delete()


# calculate difficulty of all passages
def calc_passage_difficulty():
    for passage in Passage.objects.all():
        passage.difficulty = get_text_difficulty(passage.text)
        passage.save()

from django.db import models
from django_mysql.models import ListCharField as model_ListCharField

PASSAGE_TITLE_MAX_LEN = 100
TAG_MAX_NUM = 5
WORD_MAX_LEN = 12

MAX_RANK = 60025
DEFAULT_WORD_ID = 0


class WordFreq(models.Model):
    # COCA
    name = models.CharField(max_length=WORD_MAX_LEN, default="")
    rank = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class WordDef(models.Model):
    name = models.CharField(max_length=WORD_MAX_LEN, default="")
    definition = models.TextField(default="", blank=True)

    def __str__(self):
        return self.name


class Word(models.Model):
    name = models.CharField(max_length=WORD_MAX_LEN, default="")
    rank = models.IntegerField(default=0)
    p_id = models.IntegerField(default=0)
    select_cnt = models.IntegerField(default=0)

    def_id = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


def get_wordnet_pos(treebank_tag):
    from nltk.corpus import wordnet
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def get_word_rank(word):    
    results = WordFreq.objects.filter(name=word)
    if results.exists():
        word = results.first()
        return word.rank, word.id
    else:
        return MAX_RANK, DEFAULT_WORD_ID


def add_words(pharagraphs, stop_words, passage_id):
    # full_word_list = {(word, tag)..}
    # stop_words = [stopword1, stopword2..]
    from nltk.stem.wordnet import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    added_words = set([])
    text_expand = []
    results = {}

    def add_word(word, pos):
        word_folded = word.casefold()
        if (not pos) or (word_folded in stop_words):
            return (word, word_folded, tag, DEFAULT_WORD_ID)
        lemma = lemmatizer.lemmatize(word_folded, pos=pos).casefold()
        if (lemma in added_words) or (not lemma.islower()):
            # if added or doesn't contain alphabets
            return (word, lemma, tag, DEFAULT_WORD_ID)
        added_words.add(lemma)
        rank, word_freq_id = get_word_rank(lemma)
        new_word = Word.objects.create(
            name=lemma, 
            p_id=passage_id, 
            select_cnt=0, 
            rank=rank, 
        )
        return (word, lemma, tag, new_word.id)

    for para in pharagraphs:
        para_expand = []
        for word, tag in para:
            para_expand.append(add_word(word, get_wordnet_pos(tag)))
        text_expand.append(para_expand)
    return text_expand


def add_definitions(passage_id):
    for word in Word.objects.filter(p_id=passage_id):
        if word.def_id:
            continue
        result = WordDef.objects.filter(name=word.name)
        if result.exists():
            word.def_id = result.first().id
        else:
            word_def = WordDef(name=word.name, definition = "{}")
            word_def.save()
            word.def_id = word_def.id
        word.save()


def get_defs():
    from json import dumps
    from PyDictionary import PyDictionary
    dictionary = PyDictionary()

    def get_def(word):
        try:
            word.definition = dumps(dictionary.meaning(word.name))
            word.save()
        except Exception as e:
            print("failed at '%s' exception: %s" % (word.name, str(e)))
            word.definition = "0"
            word.save()

    for word in WordDef.objects.filter(definition="{}"):
        get_def(word)
    print("done all")


class Passage(models.Model):
    title = models.CharField(max_length=PASSAGE_TITLE_MAX_LEN)
    text = models.TextField(default="")
    text_expand = models.TextField(default="", blank=True)
    tags = model_ListCharField(
        base_field=models.CharField(max_length=WORD_MAX_LEN), 
        size=TAG_MAX_NUM, 
        max_length=TAG_MAX_NUM*(WORD_MAX_LEN + 1), 
        default=""
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not Word.objects.filter(p_id=self.id).exists():
            from json import dumps
            from nltk import pos_tag
            from nltk.corpus import stopwords
            from nltk.tokenize import word_tokenize
            stop_words = set(stopwords.words("english"))
            paragraphs = [para.replace('\r', '') for para in self.text.split("\n")]
            paragraphs = filter(None, paragraphs)
            paragraphs = [pos_tag(word_tokenize(para)) for para in paragraphs]
            self.text_expand = dumps(add_words(paragraphs, stop_words, self.id))
            super().save(*args, **kwargs)
        add_definitions(self.id)

        



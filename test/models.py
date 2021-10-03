from django.db import models
from django_mysql.models import ListCharField as model_ListCharField

PASSAGE_TITLE_MAX_LEN = 100
TAG_MAX_NUM = 5
WORD_MAX_LEN = 34


class Lemma(models.Model):
    name = models.CharField(max_length=WORD_MAX_LEN, default="")
    freq = models.IntegerField(default=0)
    def_en = models.TextField(default="", blank=True)
    def_zh = models.TextField(default="", blank=True)

    def __str__(self):
        return self.name


class Word(models.Model):
    name = models.CharField(max_length=WORD_MAX_LEN, default="")
    lem_id = models.IntegerField(default=0)

    def __str__(self):
        return self.name


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


class Passage(models.Model):
    title = models.CharField(max_length=PASSAGE_TITLE_MAX_LEN)
    text = models.TextField(default="")
    lemma_pos = models.TextField(default="", blank=True)
    # {lemma1.id: [(word1.id, len(word1.name), [pos1, ]), ], }
    tags = model_ListCharField(
        base_field=models.CharField(max_length=WORD_MAX_LEN), 
        size=TAG_MAX_NUM, 
        max_length=TAG_MAX_NUM*(WORD_MAX_LEN + 1), 
        default=""
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        from json import dumps
        import re

        lemma_pos = {}
        lem_word_map = get_lem_word_map(self.text)
        for lem_id in lem_word_map:
            for word_id, word in lem_word_map[lem_id]:
                pos_offset = 0
                if word[0] == "'":
                    reg = r"(%s)(\W|')" % (word)
                else:
                    reg = r"(\W|')(%s)(\W|')" % (word)
                    pos_offset = 1
                if lem_id not in lemma_pos:
                    lemma_pos[lem_id] = []
                pos_list = [w.start() + pos_offset for w in re.finditer(reg, self.text)]
                lemma_pos[lem_id].append((word_id, pos_list))
        
        self.lemma_pos = dumps(lemma_pos)
        super().save(*args, **kwargs)

        



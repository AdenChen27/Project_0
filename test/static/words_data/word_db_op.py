# from test.static.words_data import word_db_op;import importlib
# importlib.reload(word_db_op); word_db_op.main()
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
        print("func:%s took: %2.4fs" % (f.__name__, te - ts))
        return result
    return wrap


def read_lemma():
    lines = []
    with open(r"test/static/words_data/lemma.en.txt", "r") as lemma_file:
        while True:
            line = lemma_file.readline()
            if line == '':
                break
            if line[0] != ';':
                line_l, line_r = line[:-1].split("->")
                line_l = line_l.strip().split("/")
                if len(line_l) == 1:
                    lemma, freq = line_l[0], -1
                else:
                    lemma, freq = line_l
                words = [w.strip() for w in line_r.split(",")]
                lines.append((lemma, freq, words))
    return lines

def read_dict():
    with open(r"test/static/words_data/ecdict_slim.csv", "r") as file:
        lines = {}
        while True:
            line = file.readline()
            if not line:
                break
            word, def1, def2 = line.split(",")
            if lines.get(word, -1) != -1:
                print(word)
            lines[word] = (def1, def2)
    return lines


from test.models import Lemma

@timer
def f1(length):
    for i in range(length):
        le = Lemma.objects.get(id=i + 1).name


@timer
def f2(lemmas):
    for i in range(len(lemmas)):
        # le = Lemma.objects.filter(name=lemmas[i][0]).first().name
        le = Lemma.objects.get(name=lemmas[i][0]).name


def main():
    test_len = 100
    f1(test_len)
    f2(read_lemma()[:test_len])
    #     for word in words:
    #         Word(name=word, lem_id=lemma_id).save()
    # from test.models import Lemma, Word
    # ecdict = read_dict()
    # lemma_lines = read_lemma()
    # for i in range(len(lemma_lines)):
    #     lemma, *_ = lemma_lines[i]
    #     lemma_obj = Lemma.objects.filter(name=lemma).first()
    #     defs = ecdict.get(lemma, ("", ""))
    #     lemma_obj.def_en, lemma_obj.def_zh = defs
    #     lemma_obj.save()
    #     if i % 500 == 0:
    #         print("[done %d]" % i)

    # lemma_lines = read_lemma()
    # for i in range(len(lemma_lines)):
    #     lemma, *_ = lemma_lines[i]
    #     if not Word.objects.filter(name=lemma).exists():
    #         Word(name=lemma, lem_id=Lemma.objects.filter(name=lemma).first().id).save()
    #     if i % 1000 == 0:
    #         print("[done %d]" % i)



    





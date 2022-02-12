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


@timer
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


@timer
def read_dict():
    with open(r"test/static/words_data/ecdict_slim.csv", "r") as file:
        lines = {}
        while True:
            line = file.readline()
            if not line:
                break
            word, def1, def2 = line.split(",")
            lines[word.lower()] = (def1, def2)
    return lines

def read_full_dict():
    import csv
    csv_reader = csv.reader(open(r"test/static/words_data/ecdict.csv"))
    d = {}
    for row in csv_reader:
        if ',' in row[2] or ',' in row[3]:
            d[row[0]] = [row[2], row[3]]
    return d

from test.models import Word, Lemma


@timer
def f1(length):
    for i in range(length):
        le = Lemma.objects.get(id=i + 1).name


@timer
def f2(length):
    for i in range(length):
        le = Word.objects.get(id=i + 1).name


# from test.static.words_data import word_db_op;import importlib
# importlib.reload(word_db_op); word_db_op.main()
# from test.static.words_data import word_db_op;import importlib; importlib.reload(word_db_op); word_db_op.main()
@timer
def main():
    i = 0
    for lemma in Lemma.objects.all():
        lemma.def_en = lemma.def_en.replace("\\n", "\n")
        lemma.def_zh = lemma.def_zh.replace("\\n", "\n")
        lemma.save()
        i += 1
        if i % 1000 == 0:
            print("[+]done", i)

    # d = read_full_dict();
    # lemmas = [a for a, b, c in read_lemma()]
    # i = 0
    # for lem in lemmas:
    #     if lem in d and (',' in d[lem][0] or ',' in d[lem][1]):
    #         lem_objs = Lemma.objects.filter(name=lem)
    #         if lem_objs.exists():
    #             lem_obj = lem_objs.first()
    #             if lem_obj.name != lem:
    #                 print("[-]diff name: %s %s" % (lem, lem_obj.name))
    #             else:
    #                 if ',' in d[lem][0]:
    #                     if d[lem][0][:2] == 'v ':
    #                         # print(">", type(d[lem][0]), d[lem][0])
    #                         d[lem][0] = "v. " + d[lem][0][2:]
    #                     if d[lem][0][:2] == 'n ':
    #                         d[lem][0] = "n. " + d[lem][0][2:]
    #                     # print("%s \n%s \n" % (lem_obj.def_en, d[lem][0]))
    #                     lem_obj.def_en = d[lem][0]
    #                     lem_obj.save()
    #                 if ',' in d[lem][1]:
    #                     if d[lem][1][:2] == 'v ':
    #                         d[lem][1] = "v. " + d[lem][1][2:]
    #                     if d[lem][1][:2] == 'n ':
    #                         d[lem][1] = "n. " + d[lem][1][2:]
    #                     # print("%s \n%s \n" % (lem_obj.def_zh, d[lem][1]))
    #                     lem_obj.def_zh = d[lem][1]
    #                     lem_obj.save()
    #         i += 1
    #         if i % 1000 == 0:
    #             print("[+]done %d" % i)

    # print(d["fly"])
    # test_len = 10000
    # f1(test_len)
    # f2(test_len)
    # @timer
    # def f():
    #     from test.models import Lemma
    #     lem_objs = Lemma.objects.all()
    #     cnt = 0
    #     outer_cnt = 0
    #     for lem in lem_objs:
    #         changed = False
    #         if lem.def_en and lem.def_en[:2] == 'v ':
    #             changed = True
    #             lem.def_en = "v. " + lem.def_en[2:]

    #         if lem.def_zh and lem.def_zh[:2] == 'v ':
    #             changed = True
    #             lem.def_zh = "v. " + lem.def_zh[2:]

    #         if changed:
    #             lem.save()
    #         outer_cnt += 1
    #         if outer_cnt % 5000 == 0:
    #             print("done %d" % outer_cnt)
    # f()

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



    





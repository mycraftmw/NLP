#!/usr/bin/python3
import os
import random
import string
import xml.etree.ElementTree as ET


tab = str.maketrans("", "", string.punctuation.replace("-", "").replace("|", "").replace('_', ''))

def extract_RDFdata_and_lex(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    enrties = root.findall(".//entry")
    r = []
    for each in enrties:
        alltp = each.findall(".//mtriple")
        # lexs = each.findall(".//lex")
        lex = each.find(".//lex")
        tptxt = " | ".join([tp.text.translate(tab) for tp in alltp])
        # for en in lexs:
        #     r.append((tptxt.lower(), en.text.lower()))
        r.append((tptxt.lower(), lex.text.lower()))
    return r


if __name__ == "__main__":
    devenfile = open("dev_ty.en", "w")
    devvifile = open("dev_ty.vi", "w")
    trainenfile = open("train_ty.en", "w")
    trainvifile = open("train_ty.vi", "w")
    testvifile = open("tst_ty.vi", "w")
    testenfile = open("tst_ty.en", "w")
    vocabenfile = open("vocab_ty.en", "w")
    vocabvifile = open("vocab_ty.vi", "w")
    infervifile = open("infer_ty.vi", "w")
    vocaben = set()
    vocabvi = set()

    for dtri in os.scandir("./challenge_data_train_dev/dev"):
        for fn in os.scandir(dtri.path):
            data = extract_RDFdata_and_lex(fn.path)
            for each in data:
                devvifile.write(each[0] + "\n")
                devenfile.write(each[1] + "\n")
                # for a in [a.strip().translate(tab).split(' ') for a in each[0].split("|")]:
                #     vocabvi.update(a)
                vocabvi.update([a.strip() for a in each[0].split("|")])
                vocaben.update([a.strip() for a in each[1].split(" ")])

    for dtri in os.scandir("./challenge_data_train_dev/train"):
        for fn in os.scandir(dtri.path):
            data = extract_RDFdata_and_lex(fn.path)
            for each in data:
                p = random.random()
                if p <= 0.9:
                    trainvifile.write(each[0] + "\n")
                    trainenfile.write(each[1] + "\n")
                else:
                    testvifile.write(each[0] + "\n")
                    testenfile.write(each[1] + "\n")
                # for a in [a.strip().translate(tab).split(' ') for a in each[0].split("|")]:
                #     vocabvi.update(a)
                vocabvi.update([a.strip() for a in each[0].split("|")])
                vocaben.update([a.strip() for a in each[1].split(" ")])

    sym = ["<unk>", "<s>", "</s>"]
    if "" in vocaben:
        vocaben.remove("")
    if "" in vocabvi:
        vocabvi.remove("")
    vocaben.update(string.punctuation)
    vocabvi.update(string.punctuation)
    vocabenlist = list(vocaben)
    vocabvilist = list(vocabvi)
    vocabenlist.sort()
    vocabvilist.sort()
    vocabenfile.write("\n".join(sym + vocabenlist))
    vocabvifile.write("\n".join(sym + vocabvilist))

    ## build the inerence file
    tree = ET.parse("./testdata_no_lex.xml")
    root = tree.getroot()
    enrties = root.findall(".//entry")
    for each in enrties:
        alltp = each.findall(".//mtriple")
        tptxt = " ".join([tp.text for tp in alltp])
        infervifile.write(tptxt.lower() + "\n")

    devenfile.close()
    devvifile.close()
    trainenfile.close()
    trainvifile.close()
    vocabenfile.close()
    vocabvifile.close()
    testenfile.close()
    testvifile.close()
    infervifile.close()

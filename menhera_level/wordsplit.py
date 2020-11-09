import re

import numpy as np
import MeCab


nmw = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
nmc = MeCab.Tagger('-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')


def get_words(text, pos_list=[], form="asitis", stopwords=[]):
    word_list = []
    inflection_index = inflection(form)
    text = re.sub('[!-/:-@[-`{-~！？♥♡＆]', ' ', text)
    for chunk in nmc.parse(text).splitlines()[:-1]:
        morpheme = chunk.split('\t')
        morpheme = parts_of_speech(morpheme, pos_list)
        if morpheme == None:
            continue
        word = morpheme[inflection_index]
        if word in stopwords:
            continue
        word_list.append(word.lower())
    return word_list


def parts_of_speech(morpheme, pos_list):
    if pos_list == []:
        return morpheme
    else:
        for pos in pos_list:
            if morpheme[3].startswith(pos):
                return morpheme


def inflection(form):
    if form == "asitis":
        return 0
    elif form == "origin":
        return 2
    else:
        return "error in form"
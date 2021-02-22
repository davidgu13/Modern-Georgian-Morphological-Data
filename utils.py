__author__ = "David Guriel"
import sys
import string
import os

misc = ['', ' ', '\xa0'] + list(string.punctuation + string.ascii_lowercase + string.ascii_uppercase + string.digits)
kat2eng = dict(zip(['ა', 'ბ', 'გ', 'დ', 'ე', 'ვ', 'ზ', 'თ', 'ი', 'კ', 'ლ', 'მ', 'ნ', 'ო', 'პ', 'ჟ', 'რ', 'ს', 'ტ', 'უ', 'ფ', 'ქ', 'ღ', 'ყ', 'შ', 'ჩ', 'ც', 'ძ', 'წ', 'ჭ', 'ხ', 'ჯ', 'ჰ']+misc,
                   ['a', 'b', 'g', 'd', 'e', 'v', 'z', 't', 'i', "k'", 'l', 'm', 'n', 'o', "p'", 'ž', 'r', 's', "t'", 'u', 'p', 'k', 'ġ', "q'", 'š', 'č', 'c', 'j', "c'", "č'", 'x', 'ǰ', 'h']+misc))

eng2kat = dict((v,k) for k,v in kat2eng.items()) # swap keys & values.

vowels = ['ა', 'ე', 'ი', 'ო', 'უ']
def vowel_in_word(word): return any(v in word for v in vowels)

screeves_formats = dict(zip(range(1,12),['IND;PRS','IND;IPFV','SBJV;PRS','IND;FUT','COND','SBJV;FUT','IND;PST;PFV','OPT','IND;PRF','IND;PST;PRF','SBJV;PRF'])) # as shown in the Unimorph data.

def transliterate_kat2eng(kat_word): return ''.join([kat2eng[c] for c in list(kat_word)])
def transliterate_eng2kat(eng_word): # requires a bit more attention, due to apostrophe (') issues.
    kat_chars_list = list()
    for i in range(len(eng_word)):
        if eng_word[i]=="'":
            continue
        elif eng_word[i] not in eng2kat: # e.g. "q'"
            kat_char = eng2kat[eng_word[i]+"'"]
        else:
            if i+1<len(eng_word):
                if eng_word[i+1]=="'":
                    kat_char = eng2kat[eng_word[i]+"'"]
                else:
                    kat_char = eng2kat[eng_word[i]]
            else:
                kat_char = eng2kat[eng_word[i]]
        kat_chars_list.append(kat_char)
    return ''.join(kat_chars_list)

def format_pronouns(key): return "{};{}".format(key[2],str.upper(key[:2]))

def zip_paas(vals): return dict(zip(['pref','suff'], vals))
def zip_pronouns_paas(vals): return dict(zip(['sg1','sg2','sg3','pl1','pl2','pl3'],[zip_paas(paa) for paa in vals]))
def zip_pronouns(vals): return dict(zip(['sg1', 'sg2', 'sg3', 'pl1', 'pl2', 'pl3'], vals))

SUBJECTIVE_VERSION = zip_pronouns(['ი', 'ი', 'უ', 'ი', 'ი', 'უ'])
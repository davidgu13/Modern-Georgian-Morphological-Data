__author__ = "David Guriel"
# from utils import *
# from Lemma import *
from Screeve import *


class Conjugation:
    def __init__(self, screeves_list:[Screeve]):
        self.screeves = screeves_list

    def gen_all_forms(self, lemma:Lemma, use_unimorph_format, verbose):
        lemma.generate_clean_paradigm(self.screeves, use_unimorph_format, verbose)



if __name__=='__main__':
    params = sys.argv[1:]
    lemma_choice = int(params[0])
    verbose, use_unimorph_format = bool(int(params[1])), bool(int(params[2])) # verbose includes English transliteration and printing Screeves headlines.

    transitive_class = Conjugation(define_Transitive_Screeves())
    intransitive_class = Conjugation(define_Intransitive_Screeves())

    # region transitive_verbs
    # 2 simple regular verbs for example, and then the actual 5 verbs:
    write = Transitive_Lemma('და','','წერ','','ა','OV','IOV', masdar_imprf='წერა')
    build = Transitive_Lemma('ა','ა','შენ','ებ','ა','OV','IOV', masdar_prf='აშენება', masdar_imprf='შენება')
    take = Transitive_Lemma('ა','ი','ღ','ებ','ო','OV','IOV', masdar_imprf='აღება')
    lose = Transitive_Lemma('და','','კარგ','ავ','ა','OV','IOV', masdar_prf='დაკარგვა')    # Note: 1. In Screeve 9, 'damik'arg-i-a'='damik'arg-av-s' and 'dagik'arg-i-a-t'='dagik'arg-av-t' (Wiktionary uses one version, I use the other).   2. In Screeves 10 & 11, the TS disappears.
    do = Transitive_Lemma('გა','ა','კეთ','ებ','ა','OV','IOV', masdar_prf='გაკეთება', masdar_imprf='კეთება')
    listen = Transitive_Lemma('მო','უ','სმენ','','ა','OV','IOV','სმინ', masdar_prf='მოსმენა')   # Note: The root changes from 'smen' to 'smin' in Screeves {7,8,10,11}
    let_pass = Transitive_Lemma('გა','ა','ტარ','ებ','ა','OV','IOV', masdar_prf='გატარება')

    transitive_lemmas_dict = {1: write, 2: build, 3: take, 4: lose, 5: do, 6: listen, 7:let_pass}
    example_lemma_transitive = transitive_lemmas_dict [lemma_choice]
    # transitive_class.gen_all_forms(example_lemma_transitive, use_unimorph_format, verbose)
    # endregion transitive

    # region intransitive_verbs
    blush = Intransitive_Lemma('გა', '', 'წითლ', 'ებ', 'ა', 'ი', '', '', 2, masdar_prf='გაწითლება', masdar_imprf='წითლება')
    be_done = Intransitive_Lemma('გა', '', 'კეთ', 'ებ', 'ა', 'ი', '', '', 2, masdar_prf='?')
    be_opened = Intransitive_Lemma('გა', 'ი', 'ღ', 'ებ', 'ო', 'ე', '', '', 1, masdar_prf='გაიღება ?') # you can add the active parallel to the first list!
    written = Intransitive_Lemma('და', 'ი', 'წერ', 'ებ', 'ა', 'ე',  '', '', 1, masdar_imprf='იწერა?')
    be_cleaned = Intransitive_Lemma('გა', 'ი', 'წმინდ', 'ებ', 'ა', 'ე', '', '', 1, masdar_prf='გაწმნიდება?', masdar_imprf='წმინდება')
    err = Intransitive_Lemma('შე', '', 'ცდ', 'ებ', 'ა' , 'ი', '', '', 3, masdar_prf='შეცდომა')
    hide = Intransitive_Lemma('და', 'ი', 'მალ', 'ებ', 'ა', 'ე', '', '', 1, masdar_prf='დამალვა', masdar_imprf='მალვა')
    choke = Intransitive_Lemma('და', 'ი', 'ხრჩ', 'ობ', 'ო', 'ე', '', '', 1, masdar_prf='დახრჩობა', masdar_imprf='ხრჩობა')

    intransitive_lemmas_dict = {1: blush, 2: be_done, 3:be_opened, 4:written, 5:be_cleaned, 6:err, 7:hide, 8:choke}
    # endregion intransitive_verbs

    example_lemma_intransitive = intransitive_lemmas_dict[8]
    intransitive_class.gen_all_forms(example_lemma_intransitive, use_unimorph_format, verbose)

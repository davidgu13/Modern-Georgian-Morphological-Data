__author__ = "David Guriel"
from Screeve import *
import pandas as pd


class Conjugation:
    def __init__(self, screeves_list:[Screeve]):
        self.screeves = screeves_list

    def gen_paradigm(self, lemma:Lemma, use_unimorph_format, verbose, f):
        lemma.generate_clean_paradigm(self.screeves, use_unimorph_format, verbose, f)

    @staticmethod
    def gen_lemma_object(row, conj):
        if conj=='tv':
            obj = Transitive_Lemma(*row.tolist())
        elif conj=='itv':
            obj = Intransitive_Lemma(*row.tolist())
        elif conj=='med':
            obj = Medial_Lemma(*row.tolist())
        elif conj=='ind':
            obj = Indirect_Lemma(*row.tolist())
        elif conj=='stat':
            obj = Stative_Lemma(*row.tolist())
        else:
            raise Exception("Unknown Conjugation class!")
        return obj


if __name__=='__main__':
    params = sys.argv[1:]
    file_path, verbose, use_unimorph_format = params[0], bool(int(params[1])), bool(int(params[2])) # verbose includes English transliteration and printing Screeves headlines.

    transitive_class = Conjugation(define_Transitive_Screeves())
    TV_df = pd.read_excel(file_path, sheet_name=0)
    TV_df = TV_df.drop(columns=TV_df.columns.tolist()[13:])
    TV_df.fillna('', inplace=True)

    intransitive_class = Conjugation(define_Intransitive_Screeves())
    ITV_df = pd.read_excel(file_path, sheet_name=1)
    ITV_df = ITV_df.drop(columns=ITV_df.columns.tolist()[18:])
    ITV_df.fillna('', inplace=True)

    medial_class = Conjugation(define_Medial_Screeves())
    MED_df = pd.read_excel(file_path, sheet_name=2)
    MED_df = MED_df.drop(columns=MED_df.columns.tolist()[10:])
    MED_df.fillna('', inplace=True)

    indirect_class = Conjugation(define_Indirect_Screeves())
    IND_df = pd.read_excel(file_path, sheet_name=3)
    IND_df = IND_df.drop(columns=IND_df.columns.tolist()[15:])
    IND_df.fillna('', inplace=True)

    stative_class = Conjugation(define_Stative_Screeves())
    STAT_df = pd.read_excel(file_path, sheet_name=4)
    STAT_df = STAT_df.drop(columns=STAT_df.columns.tolist()[12:])
    STAT_df.fillna('', inplace=True)


    TV_lemmas_dict = {(idx+1):transitive_class.gen_lemma_object(row,'tv') for idx,row in TV_df.iterrows()}
    ITV_lemmas_dict = {(idx+1):intransitive_class.gen_lemma_object(row,'itv') for idx,row in ITV_df.iterrows()}
    MED_lemmas_dict = {(idx+1):medial_class.gen_lemma_object(row,'med') for idx,row in MED_df.iterrows()}
    IND_lemmas_dict = {(idx+1):indirect_class.gen_lemma_object(row,'ind') for idx,row in IND_df.iterrows()}
    STAT_lemmas_dict = {(idx+1):stative_class.gen_lemma_object(row,'stat') for idx,row in STAT_df.iterrows()}

    # region transitive_and_intarnsitive_verbs
    # 2 simple regular verbs for example, and then the actual 5 verbs:
    # write = Transitive_Lemma(1, 'write', 'და','','წერ','','ა','OV','IOV', masdar_imprf='წერა')
    # build = Transitive_Lemma(2, 'build', 'ა','ა','შენ','ებ','ა','OV','IOV', masdar_prf='აშენება', masdar_imprf='შენება')
    # take = Transitive_Lemma(3, 'take', 'ა','ი','ღ','ებ','ო','OV','IOV', masdar_imprf='აღება?')
    # lose = Transitive_Lemma(4, 'lose', 'და','','კარგ','ავ','ა','OV','IOV', masdar_prf='დაკარგვა') # Note: 1. In Screeve 9, 'damik'arg-i-a'='damik'arg-av-s' and 'dagik'arg-i-a-t'='dagik'arg-av-t' (Wiktionary uses one version, I use the other).   2. In Screeves 10 & 11, the TS disappears.
    # do = Transitive_Lemma(5, 'do', 'გა','ა','კეთ','ებ','ა','OV','IOV', masdar_prf='გაკეთება', masdar_imprf='კეთება')
    # listen = Transitive_Lemma(6, 'listen', 'მო','უ','სმენ','','ა','OV','IOV','სმინ', masdar_prf='მოსმენა') # Note: The root changes from 'smen' to 'smin' in Screeves {7,8,10,11}
    # let_pass = Transitive_Lemma(7, 'let_pass', 'გა','ა','ტარ','ებ','ა','OV','IOV', masdar_prf='გატარება')
    # transitive_lemmas_dict = {1: write, 2: build, 3: take, 4: lose, 5: do, 6: listen, 7:let_pass}

    # blush = Intransitive_Lemma(1, 'blush', 2, 1, 'გა', '', 'წითლ', 'ებ', 'ა', 'ი', '', '', 'ულ', '', masdar_prf='გაწითლება', masdar_imprf='წითლება')
    # be_done = Intransitive_Lemma(2, 'be_done', 2, 1, 'გა', '', 'კეთ', 'ებ', 'ა', 'ი', 'ებ', '', 'ულ', '', masdar_prf='?')
    # be_opened = Intransitive_Lemma(3, 'be_opened', 1, 1, 'გა', 'ი', 'ღ', 'ებ', 'ო', 'ე', 'ებ', '', 'ულ', '', masdar_prf='გაიღება ?') # you can add the active parallel to the first list!
    # written = Intransitive_Lemma(4, 'written', 1, 1, 'და', 'ი', 'წერ', 'ებ', 'ა', 'ე', '', '', 'ილ', '', masdar_imprf='იწერა?')
    # be_cleaned = Intransitive_Lemma(5, 'be_cleaned', 1, 1, 'გა', 'ი', 'წმინდ', 'ებ', 'ა', 'ე', '', '', 'ილ', '', masdar_prf='გაწმნიდება?', masdar_imprf='წმინდება')
    # err = Intransitive_Lemma(6, 'err', 3, 1, 'შე', '', 'ცდ', 'ებ', 'ა' , 'ი', '', '', 'მარ', '', masdar_prf='შეცდომა')
    # hide = Intransitive_Lemma(7, 'hide', 1, 1, 'და', 'ი', 'მალ', 'ებ', 'ა', 'ე', '', '', 'ულ', '', masdar_prf='დამალვა', masdar_imprf='მალვა')
    # choke = Intransitive_Lemma(8, 'choke', 1, 1, 'და', 'ი', 'ხრჩ', 'ობ', 'ო', 'ე', '', '', 'მვალ', '', masdar_prf='დახრჩობა', masdar_imprf='ხრჩობა')
    # hide_tv = Intransitive_Lemma(9, 'hide_tv', 1, 2, 'და', 'ე', 'მალ', 'ებ', 'ა', 'ე', 'ვ', '', '', '', masdar_prf='დამალვა?', masdar_imprf='მალვა?')
    # stay_from = Intransitive_Lemma(10, 'stay_from', 3, 1, 'და', '', 'რჩ', 'ებ', 'ა', 'ე', 'ენ', '', '', '', masdar_prf='დარჩენა')
    # be_born = Intransitive_Lemma(11, 'be_born', 'და', 'ი', )
    # intransitive_lemmas_dict = {1: blush, 2: be_done, 3:be_opened, 4:written, 5:be_cleaned, 6:err, 7:hide, 8:choke, 9: hide_tv, 10: stay_from}
    # endregion transitive_and_intarnsitive_verbs

    conjugations_names = ['Transitive', 'Intransitive', 'Medial', 'Indirect', 'Stative']
    if not os.path.isdir("Clean Paradigms"):
        os.mkdir("Clean Paradigms")
    for dir_name in conjugations_names:
        if not os.path.isdir(os.path.join("Clean Paradigms", dir_name)):
            os.mkdir(os.path.join("Clean Paradigms", dir_name))
    choice_mapping = dict(zip(range(5),zip([transitive_class, intransitive_class, medial_class, indirect_class, stative_class],
                                           [TV_lemmas_dict, ITV_lemmas_dict, MED_lemmas_dict, IND_lemmas_dict, STAT_lemmas_dict])))
    
    class_choice = -1  # can be either 0,1,2,3,4 ; write -1 for locking.
    lemma_choices = [46, 21, 18, -1, -1] # when index isn't used, always insert 0 or -1 to disable the possibility of overriding
    assert 0 <= class_choice < len(conjugations_names)
    
    example_lemma = choice_mapping[class_choice][1][lemma_choices[class_choice]] # equivalent to CLS_lemmas_dict[46]
    with open(os.path.join("Clean Paradigms", conjugations_names[class_choice], example_lemma.translation + ".txt"), 'w+', encoding='utf8') as f:
        choice_mapping[class_choice][0].gen_paradigm(example_lemma, use_unimorph_format, verbose, f)

__author__ = "David Guriel"
import copy
from utils import *

class Lemma:
    def __init__(self, idx:int, translation:str, preverb:str, version:str, root:str, ts:str, aor_indic_3rd_sg:str, alternative_root='', masdar_prf='', masdar_imprf='', lemma_form=''):
        self.idx = int(idx)
        self.translation = translation
        self.preverb = preverb
        self.version = zip_pronouns([version]*6)
        self.lemma_form = lemma_form

        self.root = root
        self.passive_marker = '' # only used in Intransitive class
        self.ts = ts
        self.aor_indic_3rd_sg = aor_indic_3rd_sg # used for Aorist Subjunctive and 3rd Subjunctive Screeves.
        self.alter_root = alternative_root # used for Screeve 7,8,10,11 (which are morphologically highly related to each other)

        self.masdar_prf = masdar_prf # not necessarily exist, can be ''
        self.masdar_imprf = masdar_imprf # not necessarily exist, can be ''

    def gen_lemma_form(self, screeves):
        if self.lemma_form=='': # calculating the lemma name, if not already given
            self.lemma_form = self.version['sg3'] + self.root + self.passive_marker + self.ts + screeves[0].paas['sg3']['suff']  # 1st Screeve, 3rd person singular


    def generate_clean_paradigm(self, screeves, use_unimorph_format, verbose, file):
        self.gen_lemma_form(screeves)
        if verbose: file.write(f"#{self.idx} - {self.lemma_form} - {self.translation}:\n")

        for screeve in screeves: # print the 71 verbal forms (66 + 5 Imperative)
            screeve.generate_forms(copy.copy(self), use_unimorph_format, verbose, file)
        # region print masdars
        for s1,s2,f in [('PRF','Perfective',self.masdar_prf), ('IPFV','Imperfective',self.masdar_imprf)]:
            if f != '':
                if use_unimorph_format: file.write(f"{self.lemma_form}\t{f}\tV;V.MSDR;{s1}\n")
                else: file.write(f"Masdar form, {s2}: ", f, '\n')
        # endregion print masdars
        # print('\n\n')



class Transitive_Lemma(Lemma):
    def __init__(self, idx:int, translation:str, preverb:str, version:str, root:str, ts:str, aor_indic_3rd_sg:str,
                 perfect_version:str, pluperfect_version:str, alternative_root='', masdar_prf='', masdar_imprf='', lemma_form=''):
        super(Transitive_Lemma, self).__init__(idx, translation, preverb, version, root, ts, aor_indic_3rd_sg, alternative_root, masdar_prf, masdar_imprf, lemma_form)
        if perfect_version=='OV':
            self.perfect_version = zip_pronouns(['ი','ი','უ','ი','ი','უ'])
        else:
            raise Exception("Unhandled case!")
        if pluperfect_version=='IOV': self.pluperfect_version = zip_pronouns(['ე']*6)
        else:
            raise Exception("Unhandled case!")


class Intransitive_Lemma(Lemma):
    def __init__(self, idx:int, translation:str, lemma_formation:int, valency: int, preverb:str, version:str, root:str, ts:str,
                 aor_indic_3rd_sg:str, aor_indic_vowel:str,
                 perfect_ts:str, pluperfect_ts:str, perfect_marker:str, perfects_3rd_IDO:str,
                 alternative_root='', masdar_prf='', masdar_imprf='', lemma_form=''):
        super(Intransitive_Lemma, self).__init__(idx, translation, preverb, version, root, ts, aor_indic_3rd_sg, alternative_root, masdar_prf, masdar_imprf, lemma_form)
        self.aor_indic_vowel = aor_indic_vowel
        # self.aor_subj_vowel = aor_subj_vowel # if the rule in the Screeve formation is too specific, use this property to assign it,
                                               # and act similarly to the way aor_indic_vowel is used
        self.perfect_ts = perfect_ts
        self.pluperfect_ts = pluperfect_ts
        self.valency = valency
        if self.valency==1:
            self.perfect_marker = perfect_marker
        elif self.valency==2:
            assert perfects_3rd_IDO in {'', 'ს', 'ჰ'}
            self.perfects_3rd_IDO = perfects_3rd_IDO # should be
        else:
            raise Exception("Invalid valency for Intransitive class!")

        if lemma_formation in [1,2,3]: # Option 1 for prefixal (ი version), 2 for d (დ) addition, 3 for markerless
            self.formation_option = lemma_formation
        else: raise Exception('Invalid Formation value!')

        self.passive_marker = 'დ' if self.formation_option==2 else ''
        # Other modifications of the stem are found in Intransitive_Screeve class!


class Medial_Lemma(Lemma):
    def __init__(self, idx: int, translation: str, version:str, root:str, ts:str, future_ts:str, alternative_root='', masdar_prf='', masdar_imprf='', lemma_form=''):
        super(Medial_Lemma, self).__init__(idx, translation, '', version, root, ts, alternative_root, masdar_prf, masdar_imprf, lemma_form) # preverb=''
        self.future_ts = future_tsל

        self.perfect_version = zip_pronouns(['ი','ი','უ','ი','ი','უ']) # if it is not always correct, then modify manuaaly or copy from Transitive_class
        self.pluperfect_version = zip_pronouns(['ე']*6)

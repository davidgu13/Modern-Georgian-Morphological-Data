from utils import *

class Lemma:
    def __init__(self, preverb:str, version:str, root:str, ts:str, aor_indic_3rd_sg:str, alternative_root='', masdar_prf='', masdar_imprf='', lemma_form=''):
        self.preverb = preverb
        self.version = zip_pronouns([version]*6)
        self.lemma_form = lemma_form

        self.root = root
        self.ts = ts
        self.aor_indic_3rd_sg = aor_indic_3rd_sg # used for Aorist Subjunctive and 3rd Subjunctive Screeves.
        self.alter_root = alternative_root # used for Screeve 7,8,10,11 (which are morphologically highly related to each other)

        self.masdar_prf = masdar_prf # not necessarily exist, can be ''
        self.masdar_imprf = masdar_imprf # not necessarily exist, can be ''

    def generate_clean_paradigm(self, screeves, use_unimorph_format, verbose):
        for screeve in screeves: # print the 71 verbal forms (66 + 5 Imperative)
            basic_form = screeve.generate_forms(copy.copy(self), print_by_format=use_unimorph_format, verbose=verbose)
        # region print masdars
        if self.masdar_prf != '':
            if use_unimorph_format: print("{}\t{}\tV;V.MSDR;PRF".format(basic_form,self.masdar_prf))
            else: print("Masdar form, Perfective: ", self.masdar_prf)
        if self.masdar_imprf != '':
            if use_unimorph_format: print("{}\t{}\tV;V.MSDR;IPFV".format(basic_form,self.masdar_imprf))
            else: print("Masdar form, Imperfective: ", self.masdar_imprf)
        # endregion print masdars
        print()


class Transitive_Lemma(Lemma):
    def __init__(self, preverb:str, version:str, root:str, ts:str, aor_indic_3rd_sg:str, perfect_version:str, pluperfect_version:str, alternative_root='', masdar_prf='', masdar_imprf='', lemma_form=''):
        super(Transitive_Lemma, self).__init__(preverb, version, root, ts, aor_indic_3rd_sg, alternative_root, masdar_prf, masdar_imprf, lemma_form)
        if perfect_version=='OV':
            self.perfect_version = zip_pronouns(['ი','ი','უ','ი','ი','უ'])
        else:
            raise Exception("Unhandled case!")
        if pluperfect_version=='IOV': self.pluperfect_version = zip_pronouns(['ე']*6)
        else:
            raise Exception("Unhandled case!")


class Intransitive_Lemma(Lemma):
    def __init__(self, preverb:str, version:str, root:str, ts:str, aor_indic_3rd_sg:str, aor_indic_vowel:str, perfect_version:str, pluperfect_version:str, lemma_formation,
                 alternative_root='', masdar_prf='', masdar_imprf='', lemma_form=''):
        super(Intransitive_Lemma, self).__init__(preverb, version, root, ts, aor_indic_3rd_sg, alternative_root, masdar_prf, masdar_imprf, lemma_form)
        self.aor_indic_vowel = aor_indic_vowel
        # self.aor_subj_vowel = aor_subj_vowel # if the rule in the Screeve formation is too specific, use this property to assign it,
                                               # and act similarly to the way aor_indic_vowel is used

        if lemma_formation in [1,2,3]: # Option 1 for prefixal (ი version), 2 for d (დ) addition, 3 for markerless
            self.formation_option = lemma_formation
        else: raise Exception('Invalid Formation value!')
        # The actual modifications of the stem are found in Intransitive_Screeve class!

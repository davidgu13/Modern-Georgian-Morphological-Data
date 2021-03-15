__author__ = "David Guriel"
from Lemma import *
import abc

class Screeve:
    def __init__(self, idx:int, PAAs:[[str]], screeve_markers:[str], formula):
        self.idx = idx
        self.paas = zip_pronouns_paas(PAAs)# Pronominal Agreement Affixes
        self.markers = zip_pronouns(screeve_markers)
        self.formulate = formula # concatenates the different elements required for the forms.

    @abc.abstractmethod
    def screeve_specifications(self, lemma:Lemma):
        pass

    def generate_forms(self, lemma:Lemma, print_by_format:bool, verbose:bool, file):
        self.screeve_specifications(lemma) # implemented per each class

        forms = []
        if verbose: file.write(f'Screeve #{self.idx}:\n')
        for p in self.paas:
            form = self.formulate(self.paas[p]['pref'],
                                  lemma.preverb,
                                  lemma.version[p],
                                  lemma.root,
                                  lemma.passive_marker,
                                  lemma.ts,
                                  self.markers[p],
                                  self.paas[p]['suff']) # not all of them are actually used, depends on the Screeve.
            eng_form = " = {}".format(transliterate_kat2eng(form)) if verbose else ''
            if print_by_format:
                file.write(f"{lemma.lemma_form}\t{form}\tV;{format_pronouns(p)};{screeves_formats[self.idx]}{eng_form}\n")
            else:
                file.write(f"{form}{eng_form}\n")
            forms.append(form)
        current_forms_dict = zip_pronouns(forms)
        file.write('\n')
        self.gen_imperatives(current_forms_dict, lemma.lemma_form, print_by_format, verbose, file)

    def gen_imperatives(self, current_forms_dict, lemma_form, print_by_format, verbose, file):
        if self.idx == 7:  # generating Imperative forms for sg2 and pl2.
            iter_prons = ['sg2', 'pl2']
        elif self.idx == 8:  # generating Imperative forms for pl1, sg3, pl3.
            iter_prons = ['pl1', 'sg3', 'pl3']
        else:
            iter_prons = []
        for p in iter_prons:
            form = current_forms_dict[p]
            eng_form = " = {}".format(transliterate_kat2eng(form)) if verbose else ''
            if print_by_format:
                file.write(f"{lemma_form}\t{form}\tV;{format_pronouns(p)};IMP{eng_form}\n")
            else:
                file.write(f"Imperative form, {p}: {form}{eng_form}\n")
        s = '\n' if self.idx in {7,8} else ''
        file.write('\n'+s)


class Transitive_Screeve(Screeve):
    def __init__(self, idx:int, PAAs:[[str]], screeve_markers:[str], formula):
        super(Transitive_Screeve, self).__init__(idx, PAAs, screeve_markers, formula)

    def screeve_specifications(self, lemma:Transitive_Lemma):
        # region Screeves specifications
        if self.idx in {1,4} and lemma.ts=='ი':
            self.paas['pl3']['suff'] = 'ან' # instead of 'en'
        if self.idx == 9:
            lemma.version = lemma.perfect_version
        elif self.idx in {10, 11}:
            lemma.version = lemma.pluperfect_version

        if self.idx == 7:
            self.paas['sg3']['suff'] = lemma.aor_indic_3rd_sg  # can be "a" or "o"

        if self.idx == 9 and (lemma.ts == 'ებ' and not vowel_in_word(lemma.root) or lemma.root == 'ხურ'):
            lemma.ts = ''  # if a root has no vowel and ts==ებ, then in 9th screeve the ts is ommited!

        if self.idx in {7, 8, 10, 11}:
            if lemma.alter_root != '':
                lemma.root = lemma.alter_root  # a simple case of root changing
            if lemma.ts=='ენ':
                if self.idx in {7,8}:
                    lemma.root += 'ინ'
                else:
                    lemma.ts = 'ინ'
            elif lemma.ts == 'ევ':
                if self.idx in {7,8}:
                    lemma.root += 'ი'
                else:
                    lemma.ts = 'ი'

        if lemma.ts=='ოფ':
            if self.idx==9: lemma.ts = 'ვ'
            elif self.idx in {10,11}: lemma.ts=''

        if self.idx in {9, 10, 11} and lemma.ts in {'ავ','ი','ობ','ამ'}:
            lemma.ts = ''

        if self.idx in {10, 11} and lemma.ts == 'ებ':
            if vowel_in_word(lemma.root):
                lemma.ts = 'ებინ'
            else:
                lemma.ts = ''
            # An unhandled case regarding lemma.ts=='ავ' - sometimes the 3rd Subjunctive screeve marker is ა and not ო! (irrelevant for "lose")
        # endregion Screeves specifications

def define_Transitive_Screeves(conj='tv'):
    if conj=='tv': conj_class = Transitive_Screeve
    elif conj=='med': conj_class = Medial_Screeve
    else: raise Exception('Invalid Screeve class!')

    # Present Indicative
    screeve1_paas = [['ვ', ''], ['', ''], ['', 'ს'], ['ვ', 'თ'], ['', 'თ'], ['', 'ენ']]  # paa = pronominal agreement affixes
    screeve1_markers = [''] * 6
    def screeve1_form(paa_pref, prev, version, root, _, ts, screeve_marker, paa_suff): return paa_pref + version + root + ts + paa_suff  # Here, stem := version + root + ts
    present_indicative = conj_class(1, screeve1_paas, screeve1_markers, screeve1_form)

    # Imperfect Indicative
    screeve2_paas = [['ვ', ''], ['', ''], ['', 'ა'], ['ვ', 'თ'], ['', 'თ'], ['', 'ნენ']]
    screeve2_markers = ['დ' + s for s in ['ი', 'ი', '', 'ი', 'ი', '']]
    def screeve2_form(paa_pref, prev, version, root, _, ts, screeve_marker, paa_suff): return paa_pref + version + root + ts + screeve_marker + paa_suff  # stem := version + root + ts + screeve_marker
    imperfect_indicative = conj_class(2, screeve2_paas, screeve2_markers, screeve2_form)

    # Present Subjunctive
    screeve3_paas = [['ვ', ''], ['', ''], ['', 'ს'], ['ვ', 'თ'], ['', 'თ'], ['', 'ნენ']]
    screeve3_markers = ['დ' + s for s in ['ე', 'ე', 'ე', 'ე', 'ე', '']]
    present_subjunctive = conj_class(3, screeve3_paas, screeve3_markers, screeve2_form)

    # Future Indicative
    def screeve4_form(paa_pref, prev, version, root, _, ts, screeve_marker, paa_suff): return prev + paa_pref + version + root + ts + screeve_marker + paa_suff  # stem is the same as in screeve2_form
    future_indicative = conj_class(4, screeve1_paas, screeve1_markers, screeve4_form)

    # Conditional
    conditional = conj_class(5, screeve2_paas, screeve2_markers, screeve4_form)

    # Future Subjunctive
    future_subjunctive = conj_class(6, screeve3_paas, screeve3_markers, screeve4_form)

    # Aorist Indicative
    screeve7_paas = [['ვ', ''], ['', ''], ['', ''], ['ვ', 'თ'], ['', 'თ'], ['', 'ეს']]
    screeve7_markers = ['ე', 'ე', '', 'ე', 'ე', '']
    def screeve7_form(paa_pref, prev, version, root, _, ts, screeve_marker, paa_suff): return prev + paa_pref + version + root + screeve_marker + paa_suff  # stem := version + root + screeve_marker
    aorist_indicative = conj_class(7, screeve7_paas, screeve7_markers, screeve7_form)

    # Aorist Subjunctive
    screeve8_paas = [['ვ', ''], ['', ''], ['', 'ს'], ['ვ', 'თ'], ['', 'თ'], ['', 'ნ']]
    screeve8_markers = ['ო'] * 6
    aorist_subjunctive = conj_class(8, screeve8_paas, screeve8_markers, screeve7_form)

    # Perfect
    screeve9_paas = [['მ', ''], ['გ', ''], ['', ''], ['გვ', ''], ['გ', 'თ'], ['', 'თ']]
    screeve9_markers = ['ი' + 'ა'] * 6  # the 'ა' is for Inversion - marks 3rd person object
    perfect = conj_class(9, screeve9_paas, screeve9_markers, screeve4_form)

    # Pluperfect
    screeve10_markers = ['ა'] * 6  # the 'ა' is for Inversion - marks 3rd person object
    pluperfect = conj_class(10, screeve9_paas, screeve10_markers, screeve4_form)

    # 3rd Subjunctive
    screeve11_markers = ['ო' + 'ს', 'ო' + 'ს', 'ო' + 'ს', 'ო' + 'ს', 'ო' + '','ო' + '']  # the ს' is for Inversion - marks 3rd person object
    third_subjunctive = conj_class(11, screeve9_paas, screeve11_markers, screeve4_form)

    screeves = [present_indicative, imperfect_indicative, present_subjunctive, future_indicative, conditional, future_subjunctive,  # Series 1
                aorist_indicative, aorist_subjunctive,  # Series 2
                perfect, pluperfect, third_subjunctive]  # Series 3
    return screeves


class Intransitive_Screeve(Screeve):
    def __init__(self, idx: int, PAAs: [[str]], screeve_markers: [str], formula):
        super(Intransitive_Screeve, self).__init__(idx, PAAs, screeve_markers, formula)

    def screeve_specifications(self, lemma: Intransitive_Lemma):
        if self.idx == 7:
            self.paas['sg3']['suff'] = lemma.aor_indic_3rd_sg  # can mostly be "a" or "o"

            vowel = lemma.aor_indic_vowel
            self.markers = zip_pronouns([vowel, vowel, '', vowel, vowel, ''])

        if self.idx == 8:
            if lemma.formation_option in {2,3}:
                vowel = 'ე'
                markers = [vowel] * 5 + ['']
                self.paas['pl3']['suff'] = 'ნენ'
            else:
                vowel = 'ო'
                markers = [vowel] * 6
                self.paas['pl3']['suff'] = 'ნ'
            self.markers = zip_pronouns(markers)

        if self.idx in {9, 10, 11}:
            lemma.ts = lemma.perfect_ts if self.idx==9 else lemma.pluperfect_ts
            if lemma.valency==1:
                if lemma.perfect_marker in {'მარ', 'მალ'} : # special case of marker = m-___-ar (circumfix)
                    lemma.root = 'მ' + lemma.root
                    lemma.perfect_marker = lemma.perfect_marker[1:]
                self.markers = zip_pronouns([lemma.perfect_marker] * 6)
            else: # lemma.valency==2:
                marker_char = 'ოდ' if self.idx in {10,11} else ''
                if self.idx==9:
                    markers = ['ი']*6
                elif self.idx==10:
                    markers = ['ი', 'ი', '', 'ი', 'ი', 'ი']
                elif self.idx==11:
                    markers = ['ე']*6
                else: raise Exception("Impossible!")
                self.markers = zip_pronouns([marker_char+c for c in markers])

                self.paas['sg3']['pref'] = lemma.perfects_3rd_IDO

        if self.idx==10:
            if lemma.valency==1:
                self.paas = zip_pronouns_paas([['ვ','იყავი'], ['','იყავი'], ['','იყო'], ['ვ','იყავით'], ['','იყავით'], ['','იყვნენ']])
            else:
                self.paas = zip_pronouns_paas([['ვ',''], ['',''], ['','ა'], ['ვ','თ'], ['','თ'], ['','ნენ']])
        if self.idx==11:
            if lemma.valency==1:
                self.paas = zip_pronouns_paas([['ვ','იყო'], ['','იყო'], ['','იყოს'], ['ვ','იყოთ'], ['','იყოთ'], ['','იყონ']])
            else:
                self.paas = zip_pronouns_paas([['ვ',''], ['',''], ['','ს'], ['ვ','თ'], ['','თ'], ['','ნენ']])

def define_Intransitive_Screeves():
    # Present Indicative
    screeve1_paas = [['ვ', ''], ['', ''], ['', 'ა'], ['ვ', 'თ'], ['', 'თ'], ['', 'ან']]
    screeve1_markers = ['ი', 'ი', '', 'ი', 'ი', 'ი']
    def screeve1_form(paa_pref, prev, version, root, passive, ts, screeve_marker, paa_suff): return paa_pref + version + root + passive + ts + screeve_marker + paa_suff  # Here, stem := version + root + ts
    present_indicative = Intransitive_Screeve(1, screeve1_paas, screeve1_markers, screeve1_form)

    # Imperfect Indicative
    screeve2_paas = [['ვ', ''], ['', ''], ['', 'ა'], ['ვ', 'თ'], ['', 'თ'], ['', 'ნენ']]
    screeve2_markers = ['ოდ' + s for s in ['ი', 'ი', '', 'ი', 'ი', '']]
    imperfect_indicative = Intransitive_Screeve(2, screeve2_paas, screeve2_markers, screeve1_form)

    # Present Subjunctive
    screeve3_paas = [['ვ', ''], ['', ''], ['', 'ს'], ['ვ', 'თ'], ['', 'თ'], ['', 'ნენ']]
    screeve3_markers = ['ოდ' + s for s in ['ე', 'ე', 'ე', 'ე', 'ე', '']]
    present_subjunctive = Intransitive_Screeve(3, screeve3_paas, screeve3_markers, screeve1_form)

    def screeve4_form(paa_pref, prev, version, root, passive, ts, screeve_marker, paa_suff): return prev + paa_pref + version + root + passive + ts + screeve_marker + paa_suff  # stem is the same as in screeve2_form
    future_indicative = Intransitive_Screeve(4, screeve1_paas, screeve1_markers, screeve4_form)

    # Conditional
    conditional = Intransitive_Screeve(5, screeve2_paas, screeve2_markers, screeve4_form)

    # Future Subjunctive
    future_subjunctive = Intransitive_Screeve(6, screeve3_paas, screeve3_markers, screeve4_form)

    # Aorist Indicative
    screeve7_paas = [['ვ', ''], ['', ''], ['', ''], ['ვ', 'თ'], ['', 'თ'], ['', 'ნენ']]
    screeve7_markers = [] # in this case, a property of the lexeme!
    def screeve7_form(paa_pref, prev, version, root, passive, ts, screeve_marker, paa_suff): return prev + paa_pref + version + root + passive + screeve_marker + paa_suff  # stem := version + root + screeve_marker
    aorist_indicative = Intransitive_Screeve(7, screeve7_paas, screeve7_markers, screeve7_form)

    # Aorist Subjunctive
    screeve8_paas = [['ვ', ''], ['', ''], ['', 'ს'], ['ვ', 'თ'], ['', 'თ'], ['', '']] # 3.pl det. by the formation
    screeve8_markers = [] # in this case, a property of the lexeme! (perhaps of the formation option)
    aorist_subjunctive = Intransitive_Screeve(8, screeve8_paas, screeve8_markers, screeve7_form)

    # Perfect
    screeve9_paas = [['ვ', 'ვარ'], ['', 'ხარ'], ['', 'ა'], ['ვ', 'ვართ'], ['', 'ხართ'], ['', 'ან']]
    screeve9_markers = [''] * 6
    def screeve9_form(paa_pref, prev, version, root, passive, ts, screeve_marker, paa_suff): return prev + paa_pref + root + ts + screeve_marker + paa_suff  # stem is the same as in screeve2_form
    perfect = Intransitive_Screeve(9, screeve9_paas, screeve9_markers, screeve9_form)


    # Pluperfect
    screeve10_paas = [['','']]*6 # TBD by valency
    screeve10_markers = [''] * 6 # TBD by valency
    pluperfect = Intransitive_Screeve(10, screeve10_paas, screeve10_markers, screeve9_form)


    # 3rd Subjunctive
    third_subjunctive = Intransitive_Screeve(11, screeve10_paas, screeve10_markers, screeve9_form)


    screeves = [present_indicative, imperfect_indicative, present_subjunctive, future_indicative, conditional, future_subjunctive, # Series 1
                aorist_indicative, aorist_subjunctive, # Series 2
                perfect, pluperfect, third_subjunctive] # Series 3
    return screeves

class Medial_Screeve(Screeve):
    def __init__(self, idx: int, PAAs: [[str]], screeve_markers: [str], formula):
        super().__init__(idx, PAAs, screeve_markers, formula)

    def screeve_specifications(self, lemma: Medial_Lemma):
        assert lemma.preverb==''
        if self.idx in {4,5,6,7,8}:
            lemma.ts = lemma.future_ts
            lemma.version = zip_pronouns(['ი']*6)

        if self.idx in {9,10,11}:
            if lemma.ts not in {'ენ','ინავ'}:
                lemma.ts = ''

        if self.idx == 9:
            lemma.version = lemma.perfect_version
        elif self.idx in {10, 11}:
            lemma.version = lemma.pluperfect_version

        if self.idx == 7:
            self.paas['sg3']['suff'] = 'ა' # instead of lemma.aor_indic_3rd_sg - can be "a" except the verb "feel".

        if self.idx in {7, 8, 10, 11}:
            if lemma.alter_root != '':
                lemma.root = lemma.alter_root  # a simple case of root changing
            if lemma.ts in {'ენ','ინავ'}:
                if self.idx in {7,8}:
                    lemma.root += 'ინ'
                else:
                    lemma.ts = 'ინ'

def define_Medial_Screeves(): return define_Transitive_Screeves('med')


class Indirect_Screeve(Screeve):
    def __init__(self, idx: int, PAAs: [[str]], screeve_markers: [str], formula):
        super().__init__(idx, PAAs, screeve_markers, formula)

    def screeve_specifications(self, lemma: Indirect_Lemma):
        if self.idx==1:
            for i,k in enumerate(self.paas):
                if i < 4: # [1sg, 2sg, 3sg, 1pl]
                    if lemma.pres_IDO_3sg_suffix == 'ს': curr_3sg_suff = 'ს'
                    elif lemma.pres_IDO_3sg_suffix == 'ა': curr_3sg_suff = 'ა'
                    else: raise Exception("Invalid 3sg suffix marker")
                else: # [2pl, 3pl]
                    if lemma.pres_IDO_3sg_suffix == 'ს': curr_3sg_suff = 'თ'
                    elif lemma.pres_IDO_3sg_suffix == 'ა': curr_3sg_suff = 'ათ'
                    else: raise Exception("Invalid 3sg suffix marker")
                    # otherwise do nothing
                self.paas[k]['suff'] = curr_3sg_suff

        if self.idx in {1,2,3}:
            self.paas['sg3']['pref'] = lemma.pres_S_3sg_pref
            self.paas['pl3']['pref'] = lemma.pres_S_3sg_pref
            # lemma.root = lemma.root
            # lemma.ts = lemma.ts
        elif self.idx in {4,5,6}:
            lemma.version = zip_pronouns(['ე']*6)
            lemma.root = lemma.root_fut
            lemma.ts = lemma.ts_fut
        elif self.idx in {9,10,11}:
            self.paas['sg3']['pref'] = lemma.pres_S_3sg_pref
            self.paas['pl3']['pref'] = lemma.pres_S_3sg_pref
            lemma.version = zip_pronouns([''] * 6)
            lemma.root = lemma.root_perf
            lemma.ts = lemma.ts_perf
        else:
            raise Exception("No more screeves exist! If 7,8 do exist, add them manually!")

        if self.idx in {2,3,5,6,10,11}: # <=> not in 1,4,9
            d_marker = lemma.screeve_marker_d if self.idx in {2,3} else 'ოდ'
            self.markers = zip_pronouns([d_marker + v for k, v in self.markers.items()])

def define_Indirect_Screeves():
    # if conj=='tv': Indirect_Screeve = Transitive_Screeve
    # elif conj=='med': Indirect_Screeve = Medial_Screeve
    # else: raise Exception('Invalid Screeve class!')

    # Note: there is a marker in the Future Sub-Series that can be -d or -od. It is specified as a parameter in the Excel, and added in the Lemma class (not here!).

    # Present Indicative
    screeve1_paas = [['მ', ''], ['გ', ''], ['', ''], ['გვ', ''], ['გ', 'თ'], ['', 'თ']]  # some of these affixes are set later!
    screeve1_markers = [''] * 6
    def screeve1_form(paa_pref, prev, version, root, d_marker, ts, screeve_marker, paa_suff): return paa_pref + version + root + d_marker + ts + paa_suff
    present_indicative = Indirect_Screeve(1, screeve1_paas, screeve1_markers, screeve1_form)

    # Imperfect Indicative
    screeve2_paas = [['მ', 'ა'], ['გ', 'ა'], ['', 'ა'], ['გვ', 'ა'], ['გ', 'ათ'], ['', 'ათ']]
    screeve2_markers = [''] * 6 # ['დ']*6
    def screeve2_form(paa_pref, prev, version, root, d_marker, ts, screeve_marker, paa_suff): return paa_pref + version + root + d_marker + ts + screeve_marker + paa_suff
    imperfect_indicative = Indirect_Screeve(2, screeve2_paas, screeve2_markers, screeve2_form)

    # Present Subjunctive
    screeve3_paas = [['მ', 'ს'], ['გ', 'ს'], ['', 'ს'], ['გვ', 'ს'], ['გ', 'თ'], ['', 'თ']]
    screeve3_markers = ['ე', 'ე', 'ე', 'ე', 'ე', 'ე']  # ['დ' + s for s in ['ე', 'ე', 'ე', 'ე', 'ე', '']]
    present_subjunctive = Indirect_Screeve(3, screeve3_paas, screeve3_markers, screeve2_form)

    # Future Indicative
    screeve4_paas = [[v1,'ა'+v2] for [v1,v2] in screeve1_paas]

    def screeve4_form(paa_pref, prev, version, root, d_marker, ts, screeve_marker, paa_suff): return prev + paa_pref + version + root + d_marker + ts + screeve_marker + paa_suff  # stem is the same as in screeve2_form
    future_indicative = Indirect_Screeve(4, screeve4_paas, screeve1_markers, screeve4_form)

    # Conditional
    def screeve5_form(paa_pref, prev, version, root, d_marker, ts, screeve_marker, paa_suff): return prev + paa_pref + version + root + d_marker + ts + screeve_marker + paa_suff
    conditional = Indirect_Screeve(5, screeve2_paas, screeve2_markers, screeve5_form)

    # Future Subjunctive
    future_subjunctive = Indirect_Screeve(6, screeve3_paas, screeve3_markers, screeve5_form)

    # Perfect
    screeve9_paas = [['მ', ''], ['გ', ''], ['', ''], ['გვ', ''], ['გ', 'თ'], ['', 'თ']]
    screeve9_markers = ['ი' + 'ა'] * 6  # the 'ა' is for Inversion - marks 3rd person object
    perfect = Indirect_Screeve(9, screeve9_paas, screeve9_markers, screeve4_form)

    # Pluperfect
    screeve10_markers = ['ა'] * 6  # the 'ა' is for Inversion - marks 3rd person object
    pluperfect = Indirect_Screeve(10, screeve9_paas, screeve10_markers, screeve5_form)

    # 3rd Subjunctive
    screeve11_markers = ['ე' + 'ს', 'ე' + 'ს', 'ე' + 'ს', 'ე' + 'ს', 'ე' + '','ე' + '']
    third_subjunctive = Indirect_Screeve(11, screeve9_paas, screeve11_markers, screeve5_form)

    screeves = [present_indicative, imperfect_indicative, present_subjunctive, future_indicative, conditional, future_subjunctive,  # Series 1
                perfect, pluperfect, third_subjunctive]  # Series 3
    return screeves

class Stative_Screeve(Screeve):
    def __init__(self, idx: int, PAAs: [[str]], screeve_markers: [str], formula):
        super().__init__(idx, PAAs, screeve_markers, formula)

    def gen_imperatives(self, current_forms_dict, lemma_form, print_by_format, verbose, file):
        pass # No Imperatives exist in this class!!!

    def screeve_specifications(self, lemma: Stative_Lemma):
        # Note: in this class, because 5 screeves do not exist, the screeves' indices are different!
        # for p in ['sg1', 'sg2', 'pl1', 'pl2']:
        #     del self.paas[p]

        if self.idx!=1:
            lemma.o3sg_suff = 'ა'
        for i, k in enumerate(self.paas):
            # if k=='sg3':
            if i < 4:  # [1sg, 2sg, 3sg, 1pl]
                if lemma.o3sg_suff == 'ს':
                    curr_3sg_suff = 'ს'
                elif lemma.o3sg_suff == 'ა':
                    curr_3sg_suff = 'ა'
                else:
                    raise Exception("Invalid 3sg suffix marker")
            else:  # 'pl3'   # [2pl, 3pl]
                if lemma.o3sg_suff == 'ს':
                    curr_3sg_suff = 'თ'
                elif lemma.o3sg_suff == 'ა':
                    curr_3sg_suff = 'ათ'
                else:
                    raise Exception("Invalid 3sg suffix marker")
                # otherwise do nothing
            self.paas[k]['suff'] = curr_3sg_suff

        if self.idx in {4,7,8}:
            lemma.version = zip_pronouns(['ე']*6)
            lemma.root = lemma.root_fut
            lemma.ts = lemma.ts_fut

        if self.idx in {7,8}:
            self.paas['sg3']['suff'] = lemma.aor_indic_3rd_sg + ('ს' if self.idx==8 else '') # can mostly be "a" or "o"
            self.paas['pl3']['suff'] = lemma.aor_indic_3rd_sg + 'თ'  # can mostly be "a" or "o"

        if self.idx in {9,10}:
            lemma.root = lemma.root_fut
            lemma.ts = lemma.ts_fut
            lemma.version = zip_pronouns(['']*6)

        if self.idx==9: # Originally Screeve 9
            if lemma.valency==1: marker = 'ულ'
            elif lemma.valency==2: marker = 'ი'
            else: raise Exception("Invalid valency!")
            self.markers = zip_pronouns([marker]*6)
        elif self.idx==10: # Originally Screeve 10
            if lemma.valency==1:
                marker = 'ულიყო'
            elif lemma.valency==2: marker = 'ოდ'
            else: raise Exception("Invalid valency!")
            self.markers = zip_pronouns([marker]*6)


def define_Stative_Screeves():
    # Present Indicative
    screeve1_paas = [['მ', ''], ['გ', ''], ['', ''], ['გვ', ''], ['გ', 'თ'], ['', 'თ']]  # some of these affixes are set later!
    screeve1_markers = [''] * 6
    def screeve1_form(paa_pref, prev, version, root, d_marker, ts, screeve_marker, paa_suff): return paa_pref + version + root + d_marker + ts + paa_suff
    present_indicative = Stative_Screeve(1, screeve1_paas, screeve1_markers, screeve1_form)

    # Future Indicative
    # screeve4_paas = [[v1,'ა'+v2] for [v1,v2] in screeve1_paas]

    def screeve4_form(paa_pref, prev, version, root, d_marker, ts, screeve_marker, paa_suff): return prev + paa_pref + version + root + d_marker + ts + screeve_marker + paa_suff  # stem is the same as in screeve2_form
    future_indicative = Stative_Screeve(4, screeve1_paas, screeve1_markers, screeve4_form)

    # Aorist Indicative
    # screeve7_paas = [['მ', ''], ['გ', ''], ['', ''], ['გვ', ''], ['', 'თ'], ['', 'ნენ']]
    screeve7_markers = [''] * 6 # in this case, a property of the lexeme!
    def screeve7_form(paa_pref, prev, version, root, passive, ts, screeve_marker, paa_suff): return prev + paa_pref + version + root + passive + screeve_marker + paa_suff  # stem := version + root + screeve_marker
    aorist_indicative = Stative_Screeve(7, screeve1_paas, screeve7_markers, screeve7_form)

    # Aorist Subjunctive
    screeve8_paas = screeve1_paas  #[['ვ', ''], ['', ''], ['', 'ს'], ['ვ', 'თ'], ['', 'თ'], ['', '']] # 3.pl det. by the formation
    # for i in range(4):
    #     screeve8_paas[i][1] = 'ს'
    # screeve8_markers = zip_pronouns(['']*6) # in this case, a property of the lexeme! (perhaps of the formation option)
    aorist_subjunctive = Stative_Screeve(8, screeve8_paas, screeve7_markers, screeve7_form)

    # Perfect
    screeve9_paas = [['მ', ''], ['გ', ''], ['', ''], ['გვ', ''], ['გ', 'თ'], ['', 'თ']]
    screeve9_markers = ['ი' + 'ა'] * 6  # the 'ა' is for Inversion - marks 3rd person object
    perfect = Stative_Screeve(9, screeve9_paas, screeve9_markers, screeve4_form)

    # Pluperfect
    screeve10_markers = ['ოდ'] * 6  # the 'ა' is for Inversion - marks 3rd person object
    pluperfect = Stative_Screeve(10, screeve9_paas, screeve10_markers, screeve4_form)


    screeves = [present_indicative, future_indicative,  # Series 1
                aorist_indicative, aorist_subjunctive,   # Series 2
                perfect, pluperfect]  # Series 3
    return screeves
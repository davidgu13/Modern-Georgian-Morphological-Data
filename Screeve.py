# from utils import *
from Lemma import *

class Screeve:
    def __init__(self, idx:int, PAAs:[[str]], screeve_markers:[str], formula):
        self.idx = idx
        self.paas = zip_pronouns_paas(PAAs)# Pronominal Agreement Affixes
        self.markers = zip_pronouns(screeve_markers)
        self.formulate = formula # concatenates the different elements required for the forms.


    def generate_forms(self, lemma:Lemma, print_by_format:bool, verbose:bool):
        if lemma.lemma_form=='': # calculating the lemma name if necessary
            basic_form = lemma.version['sg3'] + lemma.root + lemma.ts + self.paas['sg3']['suff']  # 1st Screeve, 3rd person singular
        else:
            basic_form = lemma.lemma_form

        curr_version = lemma.version


        forms = []
        if verbose: print('Screeve #{}:'.format(self.idx))
        for p in self.paas:
            form = self.formulate(self.paas[p]['pref'], lemma.preverb, curr_version[p], lemma.root, lemma.ts,
                                  self.markers[p],
                                  self.paas[p]['suff']) # not all of them are actually used, depends on the Screeve.
            eng_form = " = {}".format(transliterate_kat2eng(form)) if verbose else ''
            if print_by_format:
                print("{}\t{}\tV;{};{}{}".format(basic_form,form,format_pronouns(p),screeves_formats[self.idx],eng_form))
            else:
                print("{}{}".format(form,eng_form))

            forms.append(form)
        current_forms_dict = zip_pronouns(forms)
        # print()


        if self.idx==7: # generating Imperative forms for sg2 and pl2.
            iter_prons = ['sg2', 'pl2']
        elif self.idx==8: # generating Imperative forms for pl1, sg3, pl3.
            iter_prons = ['pl1', 'sg3', 'pl3']
        else:
            iter_prons = []
        for p in iter_prons:
            form = current_forms_dict[p]
            eng_form = " = {}".format(transliterate_kat2eng(form)) if verbose else ''
            if print_by_format:
                print("{}\t{}\tV;{};{}{}".format(basic_form, form, format_pronouns(p), 'IMP', eng_form))
            else:
                print("Imperative form, {}: {}{}".format(p, form, eng_form))
            # print()

        return basic_form


class Transitive_Screeve(Screeve):
    def __init__(self, idx:int, PAAs:[[str]], screeve_markers:[str], formula):
        super(Transitive_Screeve, self).__init__(idx, PAAs, screeve_markers, formula)

    def generate_forms(self, lemma: Transitive_Lemma, print_by_format: bool, verbose: bool):
        if lemma.lemma_form == '':
            basic_form = lemma.version['sg3'] + lemma.root + lemma.ts + self.paas['sg3']['suff']  # 1st Screeve, 3rd person singular
        else:
            basic_form = lemma.lemma_form

        # region Screeves specifications
        if self.idx == 9:
            curr_version = lemma.perfect_version
        elif self.idx in {10, 11}:
            curr_version = lemma.pluperfect_version
        else:
            curr_version = lemma.version

        if self.idx == 7:
            self.paas['sg3']['suff'] = lemma.aor_indic_3rd_sg  # can mostly be "a" or "o"

        if self.idx == 9 and (lemma.ts == 'ებ' and not vowel_in_word(lemma.root) or lemma.root == 'ხურ'):
            lemma.ts = ''  # if a root has no vowel and ts==ებ, then in 9th screeve the ts is ommited!

        if self.idx in {7, 8, 10, 11} and lemma.alter_root != '':
            lemma.root = lemma.alter_root  # a simple case of root changing

        if self.idx in {9, 10, 11} and lemma.ts == 'ავ':
            lemma.ts = ''

        if self.idx in {10, 11} and lemma.ts == 'ებ':
            lemma.ts = 'ებინ'  # in these Screeves and this TS, "eb" turns into "ebin".
            # An unhandled case regarding lemma.ts=='ავ' - sometimes the 3rd Subjunctive screeve marker is ა and not ო! (irrelevant for "lose")
        # endregion Screeves specifications

        forms = []
        if verbose: print('Screeve #{}:'.format(self.idx))
        for p in self.paas:
            form = self.formulate(self.paas[p]['pref'], lemma.preverb, curr_version[p], lemma.root, lemma.ts,
                                  self.markers[p],
                                  self.paas[p]['suff'])  # not all of them are actually used, depends on the Screeve.
            eng_form = " = {}".format(transliterate_kat2eng(form)) if verbose else ''
            if print_by_format:
                print("{}\t{}\tV;{};{}{}".format(basic_form, form, format_pronouns(p), screeves_formats[self.idx],
                                                 eng_form))
            else:
                print("{}{}".format(form, eng_form))

            forms.append(form)
        current_forms_dict = zip_pronouns(forms)
        # print()

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
                print("{}\t{}\tV;{};{}{}".format(basic_form, form, format_pronouns(p), 'IMP', eng_form))
            else:
                print("Imperative form, {}: {}{}".format(p, form, eng_form))
            # print()

        return basic_form


class Intransitive_Screeve(Screeve):
    def __init__(self, idx: int, PAAs: [[str]], screeve_markers: [str], formula):
        super(Intransitive_Screeve, self).__init__(idx, PAAs, screeve_markers, formula)


    def generate_forms(self, lemma: Intransitive_Lemma, print_by_format: bool, verbose: bool):
        # region gen_lemma
        if lemma.lemma_form == '':
            basic_form = lemma.version['sg3'] + lemma.root + lemma.ts + self.paas['sg3']['suff']  # 1st Screeve, 3rd person singular
        else:
            basic_form = lemma.lemma_form
        # endregion gen_lemma

        curr_version = lemma.version

        if lemma.formation_option==2:
            lemma.root += 'დ' # Passive Marker

        if self.idx == 7:
            self.paas['sg3']['suff'] = lemma.aor_indic_3rd_sg  # can mostly be "a" or "o"

            vowel = lemma.aor_indic_vowel
            markers = [vowel, vowel, '', vowel, vowel, '']
            self.markers = zip_pronouns(markers)

        if self.idx == 8:
            if lemma.formation_option in {2,3}:
                vowel = 'ე'
                markers = [vowel, vowel, vowel, vowel, vowel, '']
                self.paas['pl3']['suff'] = 'ნენ'
            else:
                vowel = 'ო'
                markers = [vowel] * 6
                self.paas['pl3']['suff'] = 'ნ'
            self.markers = zip_pronouns(markers)


        forms = []
        if verbose: print('Screeve #{}:'.format(self.idx))
        for p in self.paas:
            form = self.formulate(self.paas[p]['pref'],
                                  lemma.preverb,
                                  curr_version[p],
                                  lemma.root,
                                  lemma.ts,
                                  self.markers[p],
                                  self.paas[p]['suff'])  # not all of them are actually used, depends on the Screeve.
            eng_form = " = {}".format(transliterate_kat2eng(form)) if verbose else ''
            if print_by_format:
                print("{}\t{}\tV;{};{}{}".format(basic_form, form, format_pronouns(p), screeves_formats[self.idx],eng_form))
            else:
                print("{}{}".format(form, eng_form))
            forms.append(form)
        current_forms_dict = zip_pronouns(forms)
        print()

        # region imperatives
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
                print("{}\t{}\tV;{};{}{}".format(basic_form, form, format_pronouns(p), 'IMP', eng_form))
            else:
                print("Imperative form, {}: {}{}".format(p, form, eng_form))
            # print()
        print()
        # endregion imperatives

        return basic_form


def define_Transitive_Screeves():
    # Present Indicative
    screeve1_paas = [['ვ', ''], ['', ''], ['', 'ს'], ['ვ', 'თ'], ['', 'თ'], ['', 'ენ']]  # paa = pronominal agreement affixes
    screeve1_markers = [''] * 6
    def screeve1_form(paa_pref, prev, version, root, ts, screeve_marker, paa_suff): return paa_pref + version + root + ts + paa_suff  # Here, stem := version + root + ts
    present_indicative = Transitive_Screeve(1, screeve1_paas, screeve1_markers, screeve1_form)

    # Imperfect Indicative
    screeve2_paas = [['ვ', ''], ['', ''], ['', 'ა'], ['ვ', 'თ'], ['', 'თ'], ['', 'ნენ']]
    screeve2_markers = ['დ' + s for s in ['ი', 'ი', '', 'ი', 'ი', '']]
    def screeve2_form(paa_pref, prev, version, root, ts, screeve_marker, paa_suff): return paa_pref + version + root + ts + screeve_marker + paa_suff  # stem := version + root + ts + screeve_marker
    imperfect_indicative = Transitive_Screeve(2, screeve2_paas, screeve2_markers, screeve2_form)

    # Present Subjunctive
    screeve3_paas = [['ვ', ''], ['', ''], ['', 'ს'], ['ვ', 'თ'], ['', 'თ'], ['', 'ნენ']]
    screeve3_markers = ['დ' + s for s in ['ე', 'ე', 'ე', 'ე', 'ე', '']]
    present_subjunctive = Transitive_Screeve(3, screeve3_paas, screeve3_markers, screeve2_form)

    # Future Indicative
    def screeve4_form(paa_pref, prev, version, root, ts, screeve_marker, paa_suff): return prev + paa_pref + version + root + ts + screeve_marker + paa_suff  # stem is the same as in screeve2_form
    future_indicative = Transitive_Screeve(4, screeve1_paas, screeve1_markers, screeve4_form)

    # Conditional
    conditional = Transitive_Screeve(5, screeve2_paas, screeve2_markers, screeve4_form)

    # Future Subjunctive
    future_subjunctive = Transitive_Screeve(6, screeve3_paas, screeve3_markers, screeve4_form)

    # Aorist Indicative
    screeve7_paas = [['ვ', ''], ['', ''], ['', ''], ['ვ', 'თ'], ['', 'თ'], ['', 'ეს']]
    screeve7_markers = ['ე', 'ე', '', 'ე', 'ე', '']
    def screeve7_form(paa_pref, prev, version, root, ts, screeve_marker, paa_suff): return prev + paa_pref + version + root + screeve_marker + paa_suff  # stem := version + root + screeve_marker
    aorist_indicative = Transitive_Screeve(7, screeve7_paas, screeve7_markers, screeve7_form)

    # Aorist Subjunctive
    screeve8_paas = [['ვ', ''], ['', ''], ['', 'ს'], ['ვ', 'თ'], ['', 'თ'], ['', 'ნ']]
    screeve8_markers = ['ო'] * 6
    aorist_subjunctive = Transitive_Screeve(8, screeve8_paas, screeve8_markers, screeve7_form)

    # Perfect
    screeve9_paas = [['მ', ''], ['გ', ''], ['', ''], ['გვ', ''], ['გ', 'თ'], ['', 'თ']]
    screeve9_markers = ['ი' + 'ა'] * 6  # the 'ა' is for Inversion - marks 3rd person object
    perfect = Transitive_Screeve(9, screeve9_paas, screeve9_markers, screeve4_form)

    # Pluperfect
    screeve10_markers = ['ა'] * 6  # the 'ა' is for Inversion - marks 3rd person object
    pluperfect = Transitive_Screeve(10, screeve9_paas, screeve10_markers, screeve4_form)

    # 3rd Subjunctive
    screeve11_markers = ['ო' + 'ს', 'ო' + 'ს', 'ო' + 'ს', 'ო' + 'ს', 'ო' + '','ო' + '']  # the ს' is for Inversion - marks 3rd person object
    third_subjunctive = Transitive_Screeve(11, screeve9_paas, screeve11_markers, screeve4_form)

    screeves = [present_indicative, imperfect_indicative, present_subjunctive, future_indicative, conditional, future_subjunctive,  # Series 1
                aorist_indicative, aorist_subjunctive,  # Series 2
                perfect, pluperfect, third_subjunctive]  # Series 3
    return screeves



def define_Intransitive_Screeves():
    # Present Indicative
    screeve1_paas = [['ვ', ''], ['', ''], ['', 'ა'], ['ვ', 'თ'], ['', 'თ'], ['', 'ან']]
    screeve1_markers = ['ი', 'ი', '', 'ი', 'ი', 'ი']
    def screeve1_form(paa_pref, prev, version, root, ts, screeve_marker, paa_suff): return paa_pref + version + root + ts + screeve_marker + paa_suff  # Here, stem := version + root + ts
    present_indicative = Intransitive_Screeve(1, screeve1_paas, screeve1_markers, screeve1_form)

    # Imperfect Indicative
    screeve2_paas = [['ვ', ''], ['', ''], ['', 'ა'], ['ვ', 'თ'], ['', 'თ'], ['', 'ნენ']]
    screeve2_markers = ['ოდ' + s for s in ['ი', 'ი', '', 'ი', 'ი', '']]
    imperfect_indicative = Intransitive_Screeve(2, screeve2_paas, screeve2_markers, screeve1_form)

    # Present Subjunctive
    screeve3_paas = [['ვ', ''], ['', ''], ['', 'ს'], ['ვ', 'თ'], ['', 'თ'], ['', 'ნენ']]
    screeve3_markers = ['ოდ' + s for s in ['ე', 'ე', 'ე', 'ე', 'ე', '']]
    present_subjunctive = Intransitive_Screeve(3, screeve3_paas, screeve3_markers, screeve1_form)

    def screeve4_form(paa_pref, prev, version, root, ts, screeve_marker, paa_suff): return prev + paa_pref + version + root + ts + screeve_marker + paa_suff  # stem is the same as in screeve2_form
    future_indicative = Intransitive_Screeve(4, screeve1_paas, screeve1_markers, screeve4_form)

    # Conditional
    conditional = Intransitive_Screeve(5, screeve2_paas, screeve2_markers, screeve4_form)

    # Future Subjunctive
    future_subjunctive = Intransitive_Screeve(6, screeve3_paas, screeve3_markers, screeve4_form)


    # Aorist Indicative
    screeve7_paas = [['ვ', ''], ['', ''], ['', ''], ['ვ', 'თ'], ['', 'თ'], ['', 'ნენ']]
    screeve7_markers = [] # in this case, a property of the lexeme!
    def screeve7_form(paa_pref, prev, version, root, ts, screeve_marker, paa_suff): return prev + paa_pref + version + root + screeve_marker + paa_suff  # stem := version + root + screeve_marker
    aorist_indicative = Intransitive_Screeve(7, screeve7_paas, screeve7_markers, screeve7_form)

    # Aorist Subjunctive
    screeve8_paas = [['ვ', ''], ['', ''], ['', 'ს'], ['ვ', 'თ'], ['', 'თ'], ['', '']] # 3.pl det. by the formation
    screeve8_markers = [] # in this case, a property of the lexeme! (perhaps of the formation option)
    aorist_subjunctive = Intransitive_Screeve(8, screeve8_paas, screeve8_markers, screeve7_form)

    # Perfect
    screeve9_paas = [['ვ', 'ვარ'], ['', 'ხარ'], ['', 'ა'], ['ვ', 'ვართ'], ['', 'ხართ'], ['', 'ან']]



    screeves = [present_indicative, imperfect_indicative, present_subjunctive, future_indicative, conditional, future_subjunctive, # Series 1
                aorist_indicative, aorist_subjunctive] # Series 2
                # perfect, pluperfect, third_subjunctive]
    return screeves
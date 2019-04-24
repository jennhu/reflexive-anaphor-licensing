'''
    util.py
    Helper functions for generating stimuli for RNNG experiments.
'''

import pandas as pd
import random

def read_csv(path):
    return pd.read_csv(path)

def write_sentences(sentences, path):
    # TODO: in non-dummy version, this will write out all information
    with open(path, 'w') as f:
        for s in sentences:
            f.write('%s\n' % s)

def generate_stimuli(grammatical_sentences):
    pass

class Lexicon(object):
    def __init__(self, lex_path):
        self.lex_path = lex_path

        # read and separate verbs
        verbs = read_csv(self._path('verbs.csv'))
        self.refl_verbs = verbs.loc[verbs.verb_type == 'refl'].verb
        self.matrix_verbs = verbs.loc[verbs.verb_type == 'matrix'].verb

        self.nouns = read_csv(self._path('nouns.csv'))
        self.nouns = self.nouns.loc[~self.nouns.singular.isin(['man','woman','groom'])]
        self.pronouns = read_csv(self._path('pronouns.csv'))

    def _path(self, suffix):
        return self.lex_path + '/%s' % suffix

    def generate_sentence(self, clause_type, **kwargs):
        # TODO: in non-dummy version, return tuple with all information,
        #       not just content of sentence itself
        if clause_type == 'simple':
            return self._simple_sent(**kwargs)
        else:
            return self._embed_sent(**kwargs)

    def _flip_gender(self, gender):
        return 'male' if gender == 'female' else 'female'

    def _flip_number(self, number):
        return 'singular' if number == 'plural' else 'plural'

    def _get_pn_features(self, sentence):
        if 'himself' in sentence:
            return 'male', 'singular'
        elif 'herself' in sentence:
            return 'female', 'singular'
        elif 'themselves' in sentence:
            return 'none', 'plural'
        else:
            raise NameError('no reflexive pronoun in sentence')

    def _get_nouns_by_gender(self, gender):
        return self.nouns.loc[self.nouns.gender == gender]

    def _simple_sent(self, local=True, c_command=True, mismatch='none'):
        assert local, 'local=True for simple clause'
        
        # 1. randomly choose reflexive verb
        verb = self.refl_verbs.sample().values[0]

        # 2. randomly choose features of reflexive pronoun
        pn_gender = 'male' # random.choice(['male', 'female'])
        pn_number = 'singular' # random.choice(['singular', 'plural'])
        opp_gender = self._flip_gender(pn_gender)
        opp_number = self._flip_number(pn_number)

        # 3. get reflexive pronoun based on chosen features
        if pn_number == 'singular':
            pn = 'himself' if pn_gender == 'male' else 'herself'
        else:
            pn = 'themselves'

        # 4. get rows corresponding to matching and mismatching gender
        gen_nouns = self._get_nouns_by_gender(pn_gender)
        opp_gen_nouns = self._get_nouns_by_gender(opp_gender)

        # 5. set features of antecedent to match or mismatch pronoun features
        nouns = gen_nouns if mismatch in ['none', 'number'] else opp_gen_nouns
        number = pn_number if mismatch in ['none', 'gender'] else opp_number

        # 6. choose antecedent
        antecedent = nouns[number].sample().values[0]

        # 7. construct and return sentence based on c-command relation
        if c_command:
            return 'The {} {} {} . <eos>'.format(antecedent, verb, pn)
        else:
            poss = gen_nouns[number + '_poss'].sample().values[0]
            return 'The {} {} {} {} . <eos>'.format(poss, antecedent, verb, pn)
    
    def _embed_sent(self, local=True, c_command=True, mismatch='none'):
        assert c_command, 'c_command=True for embedded clause'

        # 1. generate simple clause to be embedded
        embedded = self._simple_sent(c_command=c_command,
                                     mismatch=mismatch).lower()

        # 2. get features of reflexive pronoun
        pn_gender, pn_number = self._get_pn_features(embedded)

        # 3. randomly choose matrix verb
        matrix_verb = self.matrix_verbs.sample().values[0]

        # 4. construct and return sentence based on locality condition
        # choose inanimate noun for matrix subject if locality is satisfied
        matrix_subj_gender = 'none' if local else pn_gender
        # get nouns that match gender of matrix subject
        matrix_nouns = self._get_nouns_by_gender(matrix_subj_gender)
        matrix_subj = matrix_nouns[pn_number].sample().values[0]
        return 'The {} {} that {}'.format(matrix_subj, matrix_verb, embedded)


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

class Lexicon(object):
    def __init__(self, lex_path):
        self.lex_path = lex_path
        self.verbs = read_csv(self._path('verbs.csv'))
        self.nouns = read_csv(self._path('nouns.csv'))
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

    def _simple_sent(self, local=True, c_command=True, mismatch='none'):
        assert local, 'local must be True for simple clause'

        # 1. randomly choose reflexive verb
        refl_verbs = self.verbs.loc[self.verbs.verb_type == 'refl'].verb
        verb = refl_verbs.sample().values[0]

        # 2. randomly choose features of reflexive pronoun
        pn_gender = random.choice(['male', 'female'])
        pn_number = random.choice(['singular', 'plural'])
        opp_gender = self._flip_gender(pn_gender)
        opp_number = self._flip_number(pn_number)

        # 3. get reflexive pronoun based on chosen features
        if pn_number == 'singular':
            pn = 'himself' if pn_gender == 'male' else 'herself'
        else:
            pn = 'themselves'

        # 4. get rows corresponding to matching and mismatching gender
        gen_nouns = self.nouns.loc[self.nouns.gender == pn_gender]
        opp_gen_nouns = self.nouns.loc[self.nouns.gender == opp_gender]

        # 5. set features of antecedent to match or mismatch pronoun features
        nouns = gen_nouns if mismatch in ['none', 'number'] else opp_gen_nouns
        number = pn_number if mismatch in ['none', 'gender'] else opp_number

        # 6. choose antecedent
        antecedent = nouns[number].sample().values[0]

        # 7. construct and return sentence based on c-command relation
        if c_command:
            return 'The {} {} {} . <eos>'.format(antecedent, verb, pn)
        else:
            possessor = gen_nouns[number + '_poss'].sample().values[0]
            return 'The {} {} {} {} . <eos>'.format(possessor, antecedent, verb, pn)
    
    def _embed_sent(self, local=True, c_command=True, mismatch='none'):
        raise NotImplementedError

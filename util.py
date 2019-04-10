'''
    util.py
    Helper functions for generating stimuli for RNNG experiments.
'''

import pandas as pd

def read_txt(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    lines = [l.strip('\n') for l in lines]
    return lines

def read_csv(path):
    return pd.read_csv(path)

class Lexicon(object):
    def __init__(self, lex_path):
        self.lex_path = lex_path
        self.matrix_verbs = read_txt(self._path('matrix_verb.txt'))
        self.refl_verbs = read_txt(self._path('refl_verb.txt'))
        self.N_female = read_csv(self._path('N_female.csv'))
        self.N_inanimate = read_csv(self._path('N_inanimate.csv'))
        self.N_male = read_csv(self._path('N_male.csv'))

    def _path(self, suffix):
        return self.lex_path + '/%s' % suffix

    def _generate_stim(self, clause_type, local, c_command, grammatical, 
                             match):
        raise NotImplemented
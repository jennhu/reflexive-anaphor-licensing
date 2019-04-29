'''
    plot_util.py
    Helper functions to be used by plot_surprisals.py.
'''
from numpy import mean
import pandas as pd

#################################################################################
# Global variables
#################################################################################

MODELS = ['grnn', 'jrnn', 'trans', 'rnng', 'tiny']

TITLES = {
    'grnn': 'GRNN',
    'jrnn': 'JRNN',
    'rnng': 'RNNG',
    'tiny': 'TinyLSTM',
    'trans': 'TransXL'
}

PALETTE = {
    # ungrammatical --> red
    # grammatical --> green/blue
    'local_subj': 'indianred',
    'head': 'indianred',
    'nonlocal_subj': 'skyblue',
    'distractor': 'skyblue',
    'none': 'darkseagreen'
}

FCOLOR = '#f4f4f7'

#################################################################################
# Helper functions
#################################################################################

def _orders(exp):
    if 'loc' in exp:
        position_order = ['none', 'nonlocal_subj', 'local_subj', ]
    else:
        position_order = ['none', 'distractor', 'head']
    feature_order = ['none', 'number']
    return position_order, feature_order


def _get_title(model):
    return TITLES[model]


def _prob_ratio(df1, df2):
    prob_ratios = []
    for row in df1.itertuples():
        surprisal1 = row.surprisal
        surprisal2 = df2.loc[row.Index].surprisal
        prob_ratio = 2**(surprisal2 - surprisal1)
        prob_ratios.append(prob_ratio)
    return mean(prob_ratios)


def _get_data_df(data, surp, exp):
    # read surprisals and data
    surp_df = pd.read_csv(surp, delim_whitespace=True,
                          names=['token', 'surprisal'])
    data_df = pd.read_csv(data)

    agree, pl = 'agree' in exp, 'pl' in exp
    # only keep surprisal at specified pronoun or verb
    if agree:
        verb = 'were' if pl else 'was'
        surp_df = surp_df.loc[surp_df.token == verb]
    else:
        pn = 'themselves' if pl else exp.split('_')[1]
        surp_df = surp_df.loc[surp_df.token == pn]
        data_df = data_df.loc[data_df.pronoun == pn]

    # insert surprisal into data_df
    data_df['surprisal'] = surp_df.surprisal.values

    return data_df


def _subtract_baseline(df, exp):
    item_list = df.item.unique()
    for item in item_list:
        item_rows = df.loc[df.item == item]
        base_rows = item_rows.loc[item_rows.mismatch_position == 'none']
        baseline = base_rows.surprisal.mean()
        # subtract baseline from surprisal of all rows
        item_rows.surprisal -= baseline
        df.loc[df.item == item] = item_rows
    return df


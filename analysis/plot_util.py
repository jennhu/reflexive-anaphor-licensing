'''
    plot_util.py
    Helper functions to be used by plot_surprisals.py.
'''
from numpy import mean
import pandas as pd

#################################################################################
# Global variables
#################################################################################

MODELS = ['bert', 'trans', 'jrnn', 'grnn', 'tiny', 'rnng', '5gram']
BIG_MODELS = ['bert', 'trans', 'jrnn', 'grnn', '5gram']

PRONOUN_ORDER = ['themselves', 'himself', 'herself']
# PRONOUN_ORDER = ['them', 'him', 'her']

TITLES = {
    'bert': 'BERT',
    'grnn': 'GRNN',
    'jrnn': 'JRNN',
    'rnng': 'RNNG',
    'tiny': 'TinyLSTM',
    'trans': 'TransXL',
    '5gram': '5-gram'
}

PALETTE = {
    # ungrammatical --> red
    # grammatical --> green/blue
    'matrix_subj': 'indianred',
    'local_subj': 'indianred', # 'skyblue', 
    'head': 'indianred',
    'rc_subj': 'skyblue',
    'nonlocal_subj': 'skyblue', # 'indianred',
    'distractor': 'skyblue',
    'none': 'darkseagreen'
}

FCOLOR = '#f4f4f7'

#################################################################################
# Helper functions
#################################################################################

def _orders(exp, baseline=True):    
    if 'cc' in exp:
        position_order = ['distractor', 'head']
    elif 'rc' in exp:
        position_order = ['rc_subj', 'matrix_subj']
    elif 'nonrefl' in exp:
        position_order = ['local_subj', 'nonlocal_subj']
    else:
        position_order = ['nonlocal_subj', 'local_subj']

    if 'agree' in exp:
        target_order = ['was', 'were']
    else:
        if 'futrell' in exp:
            target_order = ['himself', 'herself']
        else:
            target_order = PRONOUN_ORDER

    if not baseline:
        position_order.insert(0, 'none')

    return position_order, target_order


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


def _get_data_df(data, surp, exp, nonrefl):
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
        if nonrefl:
            pn = 'them' if pl else exp.split('_')[-1][:3]
        else:
            pn = 'themselves' if pl else exp.split('_')[-1]
        
        print(pn)
        surp_df = surp_df.loc[surp_df.token == pn]
        # data_df = data_df.loc[data_df.pronoun == pn]

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


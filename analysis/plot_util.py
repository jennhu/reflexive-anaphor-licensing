'''
    plot_util.py
    Helper functions to be used by plot_surprisals.py.
'''
from numpy import mean
import pandas as pd

#################################################################################
# Global variables and constants.
#################################################################################

# Small-data models are trained on PTB.
SMALL_MODELS = ['tiny', 'rnng']
BIG_MODELS = ['bert', 'trans', 'jrnn', 'grnn', '5gram']
MODELS = BIG_MODELS + SMALL_MODELS

PRONOUN_ORDER = ['themselves', 'himself', 'herself']

TITLES = {
    'bert': 'BERT',
    'grnn': 'GRNN',
    'jrnn': 'JRNN',
    'rnng': 'RNNG',
    'tiny': 'TinyLSTM',
    'trans': 'TransXL',
    '5gram': '5-gram'
}

# Ungrammatical --> RED
# Distractor    --> BLUE
# Baseline      --> GREEN
PALETTE = {
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
    else:
        position_order = ['nonlocal_subj', 'local_subj']

    if not baseline:
        position_order.insert(0, 'none')

    return position_order, PRONOUN_ORDER


def _get_title(model):
    return TITLES[model]


# def _prob_ratio(df1, df2):
#     prob_ratios = []
#     for row in df1.itertuples():
#         surprisal1 = row.surprisal
#         surprisal2 = df2.loc[row.Index].surprisal
#         prob_ratio = 2**(surprisal2 - surprisal1)
#         prob_ratios.append(prob_ratio)
#     return mean(prob_ratios)


def _get_data_df(data, surp, exp, nonrefl):
    # Read surprisals and data.
    surp_df = pd.read_csv(surp, delim_whitespace=True,
                          names=['token', 'surprisal'])
    data_df = pd.read_csv(data)

    # Only keep surprisal at target pronoun, inferred from title of experiment.
    exp_suffix = exp.split('_')[-1] # 'themselves' if pl else 
    assert exp_suffix in PRONOUN_ORDER
    surp_df = surp_df.loc[surp_df.token == exp_suffix]
    # data_df = data_df.loc[data_df.pronoun == pn]

    # Insert surprisal into data_df.
    data_df['surprisal'] = surp_df.surprisal.values

    return data_df


def _subtract_baseline(df, exp):
    item_list = df.item.unique()
    for item in item_list:
        # Get rows corresponding to item.
        item_rows = df[df.item == item]
        base_rows = item_rows[item_rows.mismatch_position == 'none']
        baseline = base_rows.surprisal.mean()
        
        # Subtract baseline from surprisal of all rows.
        item_rows.surprisal -= baseline
        df[df.item == item] = item_rows
    return df


"""
    utils.py
    Constants and helper functions to be used by main plotting functions.
"""
from numpy import mean
import pandas as pd

#################################################################################
# Global variables and constants
#################################################################################

# Small-data models are trained on PTB.
SMALL_MODELS = ['tiny', 'rnng']
BIG_MODELS = ['bert', 'trans', 'jrnn', 'grnn', '5gram']
MODELS = BIG_MODELS + SMALL_MODELS

PRONOUNS = ['themselves', 'himself', 'herself']

TITLES = {
    'bert': 'BERT',
    'grnn': 'GRNN',
    'jrnn': 'JRNN',
    'rnng': 'RNNG',
    'tiny': 'TinyLSTM',
    'trans': 'TransXL',
    '5gram': '5-gram'
}

# Bar colors corresponding to mismatch_position and experiment conditions.
BASELINE_COLOR = 'darkseagreen'
DISTRACTOR_COLOR = 'skyblue'
UNGRAMMATICAL_COLOR = 'indianred'
PALETTE = {
    # Baseline --> green
    'none': BASELINE_COLOR,

    # Distractor --> blue
    'rc_subj': DISTRACTOR_COLOR, # relative clause
    'nonlocal_subj': DISTRACTOR_COLOR, # sentential complement
    'distractor': DISTRACTOR_COLOR, # prepositional phrase

    # Ungrammatical --> red
    'matrix_subj': UNGRAMMATICAL_COLOR, # relative clause
    'local_subj': UNGRAMMATICAL_COLOR, # sentential complement
    'head': UNGRAMMATICAL_COLOR # prepositional phrase
}

#################################################################################
# Helper functions
#################################################################################

def condition_order(exp, vs_baseline=False):
    """
    Returns values that mismatch_position takes in the order corresponding to
    the baseline, distractor, and ungrammatical experimental conditions.
    """
    if 'pp' in exp:
        # Experiment testing c-command only.
        order = ['distractor', 'head']
    elif 'rc' in exp:
        # Experiment testing c-command and locality.
        order = ['rc_subj', 'matrix_subj']
    else:
        # Experiment testing locality only.
        order = ['nonlocal_subj', 'local_subj']

    # Include mismatch_position = 'none' if plotting raw surprisal values.
    if not vs_baseline:
        order.insert(0, 'none')

    return order

def get_data_df(data_path, surp_path, exp, pn):
    # Read surprisals and data.
    surp_df = pd.read_csv(surp_path, delim_whitespace=True,
                          names=['token', 'surprisal'])
    data_df = pd.read_csv(data_path)

    # Only keep surprisal at target pronoun.
    surp_df = surp_df[surp_df.token == pn]
    # data_df = data_df[data_df.pronoun == pn]

    # Insert surprisal into data_df.
    data_df['surprisal'] = surp_df.surprisal.values

    return data_df

def subtract_baseline(df):
    for item in df.item.unique():
        # Get rows corresponding to item.
        item_rows = df[df.item == item]

        # Baseline condition: mismatch_position = 'none'.
        base_rows = item_rows[item_rows.mismatch_position == 'none']
        baseline = base_rows.surprisal.mean()
        
        # Subtract baseline from surprisal of all rows.
        item_rows.surprisal -= baseline
        df[df.item == item] = item_rows
    return df

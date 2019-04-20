'''
    plot_surprisals.py
    Plots mean surprisals across conditions using model surprisal data.
'''

import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from os import listdir
from numpy import mean

def plot_mean_surprisal(df, out_path, model, agree, loc):
    plt.style.use('ggplot')
    if loc:
        position_order = ['none', 'local_subj', 'nonlocal_subj']
    else:
        position_order = ['none', 'head', 'distractor']
    if agree:
        feature_order = ['none', 'number', 'both']
    else:
        feature_order = ['none', 'gender', 'number', 'both']
    params = dict(data=df, x='mismatch_feature', y='surprisal', 
                  hue='mismatch_position', 
                  hue_order=position_order, order=feature_order)
    sns.barplot(**params)
    plt.title('mean surprisal (%s)' % model)
    plt.savefig(out_path, dpi=300, bbox_inches='tight')


def prob_ratio(df1, df2):
    prob_ratios = []
    for row in df1.itertuples():
        surprisal1 = row.surprisal
        surprisal2 = df2.loc[row.Index].surprisal
        prob_ratio = 2**(surprisal2 - surprisal1)
        prob_ratios.append(prob_ratio)
    return mean(prob_ratios)


def get_data_df(data, surp, pronoun, agree):
    # read surprisals and data
    surp_df = pd.read_csv(surp, delim_whitespace=True,
                          names=['token', 'surprisal'])
    data_df = pd.read_csv(data)

    if agree:
        surp_df = surp_df.loc[surp_df.token == 'was']
    else:
        # only keep surprisal at specified pronoun
        if pronoun == 'all':
            surp_df = surp_df.loc[surp_df.token.isin(['himself'])]
        else:
            surp_df = surp_df.loc[surp_df.token == pronoun]
            data_df = data_df.loc[data_df.pronoun == pronoun]

    # insert surprisal into data_df
    data_df['surprisal'] = surp_df.surprisal.values
    
    return data_df


def main(data, surp, out_path, model, pronoun, exp):
    if exp:
        data = '../materials/%s_materials.csv' % exp
        surp = '../surprisal_data/%s/%s_surprisal_%s.txt' % (model, exp, model.upper())
        if pronoun == 'all':
            out_path = 'plots/%s_%s.png' % (exp, model)
        else:
            out_path = 'plots/%s_%s_%s.png' % (exp, model, pronoun)
    else:
        assert all(arg is not None for arg in [data, surp, out_path])
    agree = 'agree' in exp
    loc = 'loc' in exp
    df = get_data_df(data, surp, pronoun, agree)
    plot_mean_surprisal(df, out_path, model, agree, loc)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate stimuli.')
    parser.add_argument('--data', '-data',
                        help='path to data file (.csv)')
    parser.add_argument('--surp', '-surp',
                        help='path to surprisal file (.txt)')
    parser.add_argument('--out_path', '-out_path', '--O', '-O',
                        help='path to save final plots')
    parser.add_argument('--model', '-model', '--M', '-M', required=True,
                        help='name of model')
    parser.add_argument('--pronoun', '-pronoun', default='all',
                        choices=['all', 'he', 'she', 'He', 'She'],
                        help='pronouns to include in analysis')
    parser.add_argument('--exp', '-exp',
                        help='name of experiment (overrides all other args)')
    args = parser.parse_args()
    main(**vars(args))

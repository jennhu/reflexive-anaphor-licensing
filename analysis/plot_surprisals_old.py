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

def plot_mean_surprisal(df, out_path, clause_type, group_by, model): #, grammatical_baseline):
    plt.style.use('ggplot')
    position_order = ['none', 'head', 'distractor']
    feature_order = ['none', 'gender', 'number', 'both']
    params = dict(data=df, x=group_by, y='surprisal')
    if group_by == 'mismatch_feature':
        hue = 'mismatch_position' if clause_type == 'simple' else 'local'
        ax = sns.barplot(hue=hue, hue_order=position_order, order=feature_order, **params)
        ax.set_ylim(top=13)
        # ax.axhline(grammatical_baseline, ls='--', label='grammatical')
    else:
        sns.barplot(hue='mismatch', hue_order=mismatch_order, **params)
    plt.title('%s mean surprisal (%s)' % (model.upper(), clause_type))
    plt.savefig(out_path, dpi=300, bbox_inches='tight')


def prob_ratio(df1, df2):
    prob_ratios = []
    for row in df1.itertuples():
        surprisal1 = row.surprisal
        surprisal2 = df2.loc[row.Index].surprisal
        prob_ratio = 2**(surprisal2 - surprisal1)
        prob_ratios.append(prob_ratio)
    return mean(prob_ratios)


def get_data_df(data, surprisal_files):
    pronouns = ['himself', 'herself', 'themselves']
    dfs = []
    for s in surprisal_files:
        # get parameters from file name -- see README for acceptable file names
        _, clause_type, mismatch_position, mismatch_feature, _ = s.split('.')
        df = pd.read_csv('%s/%s' % (data, s), delim_whitespace=True,
                         names=['token', 'surprisal'])
        # only keep surprisal at pronoun
        # df = df.loc[df.token.isin(pronouns)]
        df = df.loc[df.token == 'himself']

        # df_male = df.loc[df.token == 'himself']
        # df_female = df.loc[df.token == 'herself']
        # df_male['pronoun'] = 'himself'
        # df_female['pronoun'] = 'herself'
        # df = pd.concat([df_male, df_female])

        # if mismatch_position == 'none':
        #     grammatical_baseline = df.surprisal.mean()
        #     pass
        # else:
        df['clause_type'] = clause_type
        df['mismatch_position'] = mismatch_position
        df['mismatch_feature'] = mismatch_feature
        # if clause_type == 'simple':
        #     df['c_command'] = (relation == 'ccommand')
        # else:
        #     df['local'] = (relation == 'local')
        dfs.append(df)
    df = pd.concat(dfs)
    # df = df.loc[df.mismatch_feature == 'none']
    return df, clause_type #, grammatical_baseline

def plot_by_pronoun(df):
    sns.barplot(data=df, x='mismatch_feature', y='surprisal', hue='pronoun')
    plt.show()


def main(data, out_path, group_by, model):
    surprisal_files = listdir(data)
    df, clause_type, = get_data_df(data, surprisal_files)
    # plot_by_pronoun(df)
    plot_mean_surprisal(df, out_path, clause_type, group_by, model)#, grammatical_baseline)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate stimuli.')
    parser.add_argument('--data', '-data', required=True,
                        help='path to files containing surprisal data')
    parser.add_argument('--out_path', '-out_path', '--O', '-O', required=True,
                        help='path to save final plots')
    parser.add_argument('--group_by', '-group_by', default='mismatch',
                        help='variable to group columns by in plot')
    parser.add_argument('--model', '-model', '--M', '-m',
                        choices=['rnng', 'grnn'],
                        help='name of model type')
    args = parser.parse_args()
    main(**vars(args))

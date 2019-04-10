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

def plot_mean_surprisal(df, out_path, group_by):
    plt.style.use('ggplot')
    mismatch_order = ['none', 'gender', 'number', 'both']
    params = dict(data=df, x=group_by, y='surprisal')
    if group_by == 'mismatch':
        sns.barplot(hue='c_command', order=mismatch_order, **params)
    else:
        sns.barplot(hue='mismatch', hue_order=mismatch_order, **params)
    plt.title('mean GRNN surprisal')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')


def prob_ratio(df1, df2):
    prob_ratios = []
    for row in df1.itertuples():
        surprisal1 = row.surprisal
        surprisal2 = df2.loc[row.Index].surprisal
        prob_ratio = 2**(surprisal2 - surprisal1)
        prob_ratios.append(prob_ratio)
    return mean(prob_ratios)


def main(data, out_path):
    pronouns = ['himself', 'herself', 'themselves']
    surprisal_files = listdir(data)
    dfs = []
    for s in surprisal_files:
        _, clause_type, mismatch, c_command, _ = s.split('.')
        df = pd.read_csv('%s/%s' % (data, s), delim_whitespace=True,
                         names=['token', 'surprisal'])
        df['clause_type'] = clause_type
        df['mismatch'] = mismatch
        df['c_command'] = (c_command == 'ccommand')
        df = df.loc[df.token.isin(pronouns)]
        dfs.append(df)
    df = pd.concat(dfs)
    plot_mean_surprisal(df, out_path)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate stimuli.')
    parser.add_argument('--data', '-data', required=True,
                        help='path to files containing surprisal data')
    parser.add_argument('--out_path', '-out_path', '--O', '-O', required=True,
                        help='path to save final plots')
    parser.add_argument('--group_by', '-group_by', default='mismatch',
                        help='variable to group columns by in plot')
    args = parser.parse_args()
    main(**vars(args))

'''
    plot_surprisals.py
    Plots mean surprisals across conditions using model surprisal data.
'''
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import mean

MODELS = ['grnn', 'jrnn', 'rnng', 'tiny', 'trans']
TITLES = {
    'grnn' : 'GRNN',
    'jrnn' : 'JRNN',
    'rnng' : 'RNNG',
    'tiny' : 'TinyLSTM',
    'trans' : 'TransXL'
}

def _orders(exp):
    if 'loc' in exp:
        position_order = ['none', 'nonlocal_subj', 'local_subj', ]
    else:
        position_order = ['none', 'distractor', 'head']
    feature_order = ['none', 'number']
    return position_order, feature_order


def _get_title(model):
    return TITLES[model]


def plot_mean_surprisal(df, out_path, model, exp):
    sns.set_style('whitegrid')
    position_order, _ = _orders(exp)
    # ungrammatical --> red, grammatical --> blue
    palette = {
        'local_subj' : 'indianred',
        'head' : 'indianred',
        'nonlocal_subj' : 'skyblue',
        'distractor' : 'skyblue',
        'none' : 'darkseagreen'
    }
    params = dict(data=df, x='mismatch_position', y='surprisal',
                  order=position_order, palette=palette)
    sns.barplot(**params)
    plt.title('%s mean surprisal (%s)' % (model, exp))
    plt.savefig(out_path, dpi=300, bbox_inches='tight')


def prob_ratio(df1, df2):
    prob_ratios = []
    for row in df1.itertuples():
        surprisal1 = row.surprisal
        surprisal2 = df2.loc[row.Index].surprisal
        prob_ratio = 2**(surprisal2 - surprisal1)
        prob_ratios.append(prob_ratio)
    return mean(prob_ratios)


def _get_data_df(data, surp, pronoun, exp):
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
        pn = 'themselves' if pl else pronoun
        surp_df = surp_df.loc[surp_df.token == pn]
        data_df = data_df.loc[data_df.pronoun == pn]

    # insert surprisal into data_df
    data_df['surprisal'] = surp_df.surprisal.values
    
    return data_df


def plot_all_models(dfs, out_path, exp):
    sns.set_style('ticks')
    position_order, _ = _orders(exp)
    cc = 'cc' in exp
    # ungrammatical --> red, grammatical --> blue
    palette = {
        'local_subj' : 'indianred',
        'head' : 'indianred',
        'nonlocal_subj' : 'skyblue',
        'distractor' : 'skyblue',
        'none' : 'darkseagreen'
    }
    fcolor = '#f4f4f7'
    _, axarr = plt.subplots(nrows=1, ncols=len(MODELS), 
                            sharey=True, figsize=(10,2))
    for i, ax in enumerate(axarr):
        model = MODELS[i]
        params = dict(data=dfs[model], x='mismatch_position', y='surprisal',
                      order=position_order, palette=palette, errwidth=1,
                      ax=ax, edgecolor=fcolor)
        sns.barplot(**params)
        if i == 0:
            ax.set_ylabel('mean surprisal', fontsize=14)
            ax.set_xlabel('')
        else:
            ax.yaxis.set_visible(False)
            if i == 2:
                ax.set_xlabel('position of feature mismatch', fontsize=12)
            else:
                ax.set_xlabel('')
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(10)
        if cc:
            ax.set_xticklabels(['none', 'distractor', 'head'])
        else:
            ax.set_xticklabels(['none', 'nonlocal', 'local'])
        ax.set_facecolor(fcolor)
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(10)
            tick.label.set_rotation(20)
        ax.set_title(_get_title(model), fontsize=14)
    plt.savefig(out_path, dpi=300, bbox_inches='tight')


def main(out_prefix, model, exp, pronoun):
    data = '../materials/%s.csv' % exp
    out_path = '%s/%s_%s.png' % (out_prefix, exp, model)
    if model == 'all':
        dfs = {}
        for m in MODELS:
            surp = '../surprisal_data/%s/%s_surprisal_%s.txt' % (m, exp, m)
            df = _get_data_df(data, surp, pronoun, exp)
            dfs[m] = df
        plot_all_models(dfs, out_path, exp)
    else:
        surp = '../surprisal_data/%s/%s_surprisal_%s.txt' % (model, exp, model)
        df = _get_data_df(data, surp, pronoun, exp)
        plot_mean_surprisal(df, out_path, model, exp)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot mean surprisals.')
    parser.add_argument('--out_prefix', '-out_prefix', '--O', '-O',
                        default='plots',
                        help='prefix to path to save final plots (file will '
                             'be named according to experiment name)')
    parser.add_argument('--model', '-model', '--M', '-M', required=True,
                        help='name of model, or all to plot all at once')
    parser.add_argument('--exp', '-exp', required=True,
                        help='name of experiment')
    parser.add_argument('--pronoun', '-pronoun', default='himself',
                        help='pronouns to include in analysis')
    args = parser.parse_args()
    main(**vars(args))

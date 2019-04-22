'''
    plot_surprisals.py
    Plots mean surprisals across conditions using model surprisal data.
'''
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import mean

def _orders(exp):
    agree, loc, pl = 'agree' in exp, 'loc' in exp, 'pl' in exp
    if loc:
        position_order = ['none', 'local_subj', 'nonlocal_subj']
    else:
        position_order = ['none', 'head', 'distractor']
    if agree or pl:
        feature_order = ['none', 'number', 'both']
    else:
        feature_order = ['none', 'gender', 'number', 'both']
    return position_order, feature_order


def plot_mean_surprisal(df, out_path, model, exp):
    plt.style.use('ggplot')
    position_order, feature_order = _orders(exp)
    params = dict(data=df, x='mismatch_feature', y='surprisal', 
                  hue='mismatch_position', hue_order=position_order, 
                  order=feature_order)
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


def _get_data_df(data, surp, pronoun, agree, pl):
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


def main(out_prefix, model, exp, pronoun):
    data = '../materials/%s_materials.csv' % exp
    surp = '../surprisal_data/%s/%s_surprisal_%s.txt' % (model, exp, model)
    out_path = '%s/%s_%s.png' % (out_prefix, exp, model)
    
    df = _get_data_df(data, surp, pronoun, exp)
    plot_mean_surprisal(df, out_path, model, exp)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot mean surprisals.')
    parser.add_argument('--out_prefix', '-out_prefix', '--O', '-O',
                        default='plots',
                        help='prefix to path to save final plots (file will '
                             'be named according to experiment name)')
    parser.add_argument('--model', '-model', '--M', '-M', required=True,
                        help='name of model')
    parser.add_argument('--exp', '-exp', required=True,
                        help='name of experiment (overrides all other args)')
    parser.add_argument('--pronoun', '-pronoun', default='himself',
                        help='pronouns to include in analysis')
    args = parser.parse_args()
    main(**vars(args))

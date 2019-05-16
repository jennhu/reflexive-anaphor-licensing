'''
    accuracy.py
    Get accuracy.
'''
import argparse
from numpy import mean
import pandas as pd

#################################################################################
# Global variables
#################################################################################

MODELS = ['grnn', 'jrnn', 'trans', 'rnng', 'tiny', '5gram', 'bert']

#################################################################################
# Helper functions
#################################################################################

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

def _get_accuracy(df, mismatch_position):
    item_list = df.item.unique()
    n_items = len(item_list)
    num_correct_vs_baseline = 0
    num_correct_vs_distractor = 0
    num_correct = 0

    for item in item_list:
        item_rows = df[df.item == item]
        ungrammatical_rows = item_rows[item_rows.grammatical == 0]
        baseline_rows = item_rows[item_rows.mismatch_position == 'none']
        distractor_rows = item_rows[item_rows.mismatch_position == mismatch_position]

        vs_baseline = ungrammatical_rows.surprisal.mean() - baseline_rows.surprisal.mean()
        vs_distractor = ungrammatical_rows.surprisal.mean() - distractor_rows.surprisal.mean()

        if vs_baseline > 0:
            num_correct_vs_baseline += 1

        if vs_distractor > 0:
            num_correct_vs_distractor += 1

        if vs_baseline > 0 and vs_distractor > 0:
            num_correct += 1

    vs_baseline_acc = num_correct_vs_baseline / float(n_items)
    vs_distractor_acc = num_correct_vs_distractor / float(n_items)
    total_acc = num_correct / float(n_items)

    return total_acc, vs_baseline_acc, vs_distractor_acc


#################################################################################
# Main function
#################################################################################

def main(out_prefix, model, exp, nonrefl, vs_baseline):
    out_path = '%s/%s_accuracy_%s.csv' % (out_prefix, exp, '_'.join(model))
    if 'futrell' in exp:
        suffixes = ['_himself', '_herself']
    elif 'agree' in exp:
        suffixes = ['', '_pl']
    else:
        suffixes = ['_himself', '_herself', '_pl']
    model_list = MODELS if model == ['all'] else model
    
    acc_dict = {'model':[], 'full_exp':[], 'total_acc':[], 'vs_baseline_acc':[], 'vs_distractor_acc':[]}
    for m in model_list:
        print(m)
        dfs = []
        for s in suffixes:
            full_exp = exp + s
            print(full_exp)
            data_path = '../materials/%s.csv' % full_exp
            surp = '../surprisal_data/%s/%s_surprisal_%s.txt' % (m, full_exp, m)
            if m == 'bert':
                df = pd.read_csv('../surprisal_data/bert/%s_surprisal_bert.csv' % full_exp)
            else:
                df = _get_data_df(data_path, surp, full_exp, nonrefl=nonrefl)

            if 'rc' in exp:
                mismatch_position = 'rc_subj'
            elif 'loc' in exp or 'ml' in exp:
                mismatch_position = 'nonlocal_subj'
            elif 'cc' in exp:
                mismatch_position = 'distractor'

            total_acc, vs_baseline_acc, vs_distractor_acc = _get_accuracy(df, mismatch_position)
            acc_dict['model'].append(m)
            acc_dict['total_acc'].append(total_acc)
            acc_dict['full_exp'].append(full_exp)
            acc_dict['vs_baseline_acc'].append(vs_baseline_acc)
            acc_dict['vs_distractor_acc'].append(vs_distractor_acc)
    acc_df = pd.DataFrame(acc_dict)
    acc_df.to_csv(out_path, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot surprisals.')
    parser.add_argument('--out_prefix', '-out_prefix', '--O', '-O',
                        default='accuracy',
                        help='prefix to path to save final plots (file will '
                             'be named according to experiment name)')
    parser.add_argument('--model', '-model', '--M', '-M', nargs='+',
                        help='names of models, or all to plot all at once')
    parser.add_argument('--exp', '-exp',
                        help='name of experiment')
    parser.add_argument('--nonrefl', '-nonrefl', action='store_true',
                        help='toggle whether using nonreflexive pronoun')
    parser.add_argument('--vs_baseline', '-vs_baseline', '--vs', '-vs',
                        default=False, action='store_true',
                        help='toggle plotting raw surprisal or surprisal '
                             'difference vs. baseline')
    args = parser.parse_args()
    main(**vars(args))

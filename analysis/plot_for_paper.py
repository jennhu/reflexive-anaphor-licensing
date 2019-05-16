'''
    plot_for_paper.py
    Generates plots to be used in paper.
'''
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import plot_util

#################################################################################
# Plot absolute surprisal values
#################################################################################

def plot_single_model(df, out_path, model, exp):
    sns.set_style('whitegrid')
    position_order, _ = plot_util._orders(exp)
    params = dict(data=df, x='mismatch_position', y='surprisal',
                  order=position_order, palette=plot_util.PALETTE)
    sns.barplot(**params)
    plt.title('%s mean surprisal (%s)' % (model, exp))
    plt.savefig(out_path, dpi=300, bbox_inches='tight')


def plot_mult_models(dfs, out_path, exp, model_list, baseline):
    if baseline:
        for m, df in dfs.items():
            dfs[m] = plot_util._subtract_baseline(df, exp)
    # set style and parameters
    sns.set_style('ticks')
    position_order, target_order = plot_util._orders(exp, baseline=baseline)
    target = 'verb' if 'agree' in exp else 'pronoun'
    params = dict(x=target, y='surprisal', order=target_order, errwidth=1,
                  palette=plot_util.PALETTE, edgecolor=plot_util.FCOLOR, 
                  hue='mismatch_position', hue_order=position_order)
    
    # legend labels and handles
    if 'cc' in exp:
        labels = ['distractor mismatch', 'head mismatch']
    elif 'rc' in exp:
        labels = ['rc subj mismatch', 'matrix subj mismatch']
    elif 'nonrefl' in exp:
        labels = ['local mismatch', 'nonlocal mismatch']
    else:
        labels = ['nonlocal mismatch', 'local mismatch']
    handles = [Patch(facecolor=plot_util.PALETTE[p]) for p in position_order]

    # tick and axis labels
    xlabel = 'target %s' % target
    ylabel = 'surprisal - baseline' if baseline else 'surprisal'
    xticklabels = target_order
    label_size = 10
    ticklabel_size = 8

    # initialize figure and subplots
    _, axarr = plt.subplots(nrows=1, ncols=len(model_list), sharey=True,
                            figsize=(2*len(model_list), 1.75))

    for i, ax in enumerate(axarr):
        # plot data
        model = model_list[i]
        sns.barplot(data=dfs[model], ax=ax, **params)
        ax.set_facecolor(plot_util.FCOLOR)

        # only keep y-axis at leftmost subplot
        if i == 0:
            ax.set_ylabel(ylabel, fontsize=label_size)
        else:
            ax.yaxis.set_visible(False)
        
        # only keep x-axis label and legend at center subplot
        if i == int(len(model_list) / 2):
            ax.set_xlabel(xlabel, fontsize=label_size)
            lg = ax.legend(labels=labels, handles=handles, fancybox=False, 
                           loc='upper center', bbox_to_anchor=(0.5, -0.45), 
                           fontsize=ticklabel_size, ncol=2)
            title = lg.get_title()
            title.set_fontsize(ticklabel_size)
            lg.get_frame().set_edgecolor('k')
            lg.get_frame().set_linewidth(0.9)
        else:
            ax.set_xlabel('')
            ax.get_legend().remove()

        # set tick labels and titles
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(ticklabel_size)
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(ticklabel_size)
            if 'agree' not in exp and 'futrell' not in exp:
                tick.label.set_rotation(20)
        ax.set_xticklabels(xticklabels)
        ax.set_title(plot_util._get_title(model), fontsize=label_size)

    # save final figure
    plt.savefig(out_path, dpi=300, bbox_inches='tight')


#################################################################################
# Main function
#################################################################################

def main(out_prefix, model, exp, nonrefl, vs_baseline):
    out_path = '%s/%s_%s.png' % (out_prefix, exp, '_'.join(model))
    if 'futrell' in exp:
        suffixes = ['_himself', '_herself']
    elif 'agree' in exp:
        suffixes = ['', '_pl']
    else:
        suffixes = ['_himself', '_herself', '_pl']
    model_list = plot_util.MODELS if model == ['all'] else model
    df_dict = {}
    for m in model_list:
        print(m)
        dfs = []
        for s in suffixes:
            full_exp = exp + s
            print(full_exp)
            data_path = '../materials/%s.csv' % full_exp
            surp = '../surprisal_data/%s/%s_surprisal_%s.txt' % (m, full_exp, m)
            df = plot_util._get_data_df(data_path, surp, full_exp, nonrefl=nonrefl)
            dfs.append(df)
        full_df = pd.concat(dfs)
        df_dict[m] = full_df
    plot_mult_models(df_dict, out_path, exp, model_list, baseline=vs_baseline)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot surprisals.')
    parser.add_argument('--out_prefix', '-out_prefix', '--O', '-O',
                        default='plots/paper',
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

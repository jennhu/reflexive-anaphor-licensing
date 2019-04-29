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
# Plot surprisal vs. baseline
#################################################################################

def plot_surprisal_vs_baseline(dfs, out_path, exp, model_list):
    for m, df in dfs.items():
        dfs[m] = plot_util._subtract_baseline(df, exp)
    plot_multiple_models(dfs, out_path, exp, model_list, ylabel='surprisal - baseline')

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


def plot_multiple_models(dfs, out_path, exp, model_list, ylabel='surprisal'):
    # set style and parameters
    sns.set_style('ticks')
    position_order, _ = plot_util._orders(exp)
    params = dict(x='pronoun', y='surprisal', errwidth=1,
                  order=plot_util.PRONOUN_ORDER, palette=plot_util.PALETTE,
                  edgecolor=plot_util.FCOLOR, hue='mismatch_position',
                  hue_order=position_order[1:])
    xticklabels = plot_util.PRONOUN_ORDER
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
        
        # only keep x-axis label at center subplot
        if i == len(model_list) / 2:
            ax.set_xlabel('target pronoun', fontsize=label_size)
        else:
            ax.set_xlabel('')

        # only keep legend at rightmost subplot
        handles = [Patch(facecolor=plot_util.PALETTE['nonlocal_subj']),
                   Patch(facecolor=plot_util.PALETTE['local_subj'])]
        if i == len(model_list) / 2:
            lg = ax.legend(labels=['nonlocal mismatch', 'local mismatch'],
                           loc='upper center', bbox_to_anchor=(0.5, -0.45), 
                           fancybox=False, fontsize=ticklabel_size, ncol=2,
                           handles=handles)
            title = lg.get_title()
            title.set_fontsize(ticklabel_size)
            lg.get_frame().set_edgecolor('k')
            lg.get_frame().set_linewidth(0.9)
        else:
            ax.get_legend().remove()

        # set tick labels and titles
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(ticklabel_size)
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(ticklabel_size)
            tick.label.set_rotation(20)
        ax.set_xticklabels(xticklabels)
        ax.set_title(plot_util._get_title(model), fontsize=label_size)

    # save final figure
    plt.savefig(out_path, dpi=300, bbox_inches='tight')


#################################################################################
# Main function
#################################################################################

def main(out_prefix, model, exp, vs_baseline):
    out_path = '%s/%s_%s.png' % (out_prefix, exp, '_'.join(model))
    
    model_list = plot_util.MODELS if model == ['all'] else model
    dfs = {}
    for m in model_list:
        print(m)

        exp1 = exp + '_himself'
        data_path = '../materials/%s.csv' % exp1
        surp1 = '../surprisal_data/%s/%s_surprisal_%s.txt' % (m, exp1, m)
        df1 = plot_util._get_data_df(data_path, surp1, exp1)

        exp2 = exp + '_herself'
        data_path = '../materials/%s.csv' % exp2
        surp2 = '../surprisal_data/%s/%s_surprisal_%s.txt' % (m, exp2, m)
        df2 = plot_util._get_data_df(data_path, surp2, exp2)

        exp3 = exp + '_pl'
        data_path = '../materials/%s.csv' % exp3
        surp3 = '../surprisal_data/%s/%s_surprisal_%s.txt' % (m, exp3, m)
        df3 = plot_util._get_data_df(data_path, surp3, exp3)

        full_df = pd.concat([df1, df2, df3])
        dfs[m] = full_df
    if vs_baseline:
        plot_surprisal_vs_baseline(dfs, out_path, exp, model_list)
    else:
        plot_multiple_models(dfs, out_path, exp, model_list)
    

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
    parser.add_argument('--vs_baseline', '-vs_baseline', '--vs', '-vs',
                        default=False, action='store_true',
                        help='toggle plotting raw surprisal or surprisal '
                             'difference vs. baseline')
    args = parser.parse_args()
    main(**vars(args))

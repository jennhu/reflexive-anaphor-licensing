'''
    plot_surprisals.py
    Plots mean surprisals across conditions using model surprisal data.
'''
import argparse
import seaborn as sns
import matplotlib.pyplot as plt

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
    params = dict(x='mismatch_position', y='surprisal', errwidth=1,
                  order=position_order, palette=plot_util.PALETTE,
                  edgecolor=plot_util.FCOLOR)
    xticklabels = ['none', 'distractor', 'head'] if 'cc' in exp else \
                  ['none', 'nonlocal', 'local']
    label_size = 10
    ticklabel_size = 8

    # initialize figure and subplots
    _, axarr = plt.subplots(nrows=1, ncols=len(model_list), sharey=True,
                            figsize=(2*len(model_list), 1.5))

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
            ax.set_xlabel('position of feature mismatch', fontsize=label_size)
        else:
            ax.set_xlabel('')

        # set tick labels and titles
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(ticklabel_size)
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(ticklabel_size)
        ax.set_xticklabels(xticklabels)
        ax.set_title(plot_util._get_title(model), fontsize=label_size)

    # save final figure
    plt.savefig(out_path, dpi=300, bbox_inches='tight')


#################################################################################
# Main function
#################################################################################

def main(out_prefix, model, exp, vs_baseline):
    data = '../materials/%s.csv' % exp
    out_path = '%s/%s_%s.png' % (out_prefix, exp, model.join('_'))

    if len(model) == 1:
        surp = '../surprisal_data/%s/%s_surprisal_%s.txt' % (model, exp, model)
        df = plot_util._get_data_df(data, surp, exp)
        plot_single_model(df, out_path, model, exp)

    else:
        model_list = plot_util.MODELS if model == 'all' else model
        dfs = {}
        for m in model_list:
            surp = '../surprisal_data/%s/%s_surprisal_%s.txt' % (m, exp, m)
            df = plot_util._get_data_df(data, surp, exp)
            dfs[m] = df
        if vs_baseline:
            plot_surprisal_vs_baseline(dfs, out_path, exp, model_list)
        else:
            plot_multiple_models(dfs, out_path, exp, model_list)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot surprisals.')
    parser.add_argument('--out_prefix', '-out_prefix', '--O', '-O',
                        default='plots',
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

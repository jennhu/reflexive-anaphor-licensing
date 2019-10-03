"""
    generate_plot.py
    Generates plots to be used in paper.
"""
import argparse
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import utils

#################################################################################
# Plotting function
#################################################################################

def plot_log_prob(dfs, out_path, exp, model_list, vs_baseline=False):
    # Set style and parameters.
    sns.set_style('ticks')
    condition_order = utils.condition_order(exp, vs_baseline=vs_baseline)
    params = dict(x='pronoun', y='surprisal', order=utils.PRONOUNS,
                  hue='mismatch_position', hue_order=condition_order,
                  palette=utils.PALETTE, errwidth=1)
    
    # Define legend labels and handles.
    if vs_baseline:
        labels = ['distractor', 'ungrammatical']
    else:
        labels = ['baseline', 'distractor', 'ungrammatical']
    handles = [Patch(facecolor=utils.PALETTE[c]) for c in condition_order]

    # Define tick and axis labels.
    xlabel = 'target pronoun'
    ylabel = 'log prob differential' if vs_baseline else 'negative log prob'
    label_size = 10
    ticklabel_size = 7.5

    # Initialize figure and subplots.
    _, axarr = plt.subplots(nrows=1, ncols=len(model_list), sharey=True,
                            figsize=(2*len(model_list), 1.75))
    
    # If plotting results for one model, make axarr into singleton list.
    if len(model_list) == 1:
        axarr = [axarr]

    # Iterate through axes and plot model data.
    for i, ax in enumerate(axarr):
        # Add barplots to ax.
        model = model_list[i]
        sns.barplot(data=dfs[model], ax=ax, **params)

        # Set tick labels and title.
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(ticklabel_size)
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(ticklabel_size)
            tick.label.set_rotation(20)
        ax.set_title(utils.TITLES[model], fontsize=label_size)

        # LEFT-MOST subplot: keep y-axis labels.
        if i == 0:
            ax.set_ylabel(ylabel, fontsize=label_size)
        else:
            ax.set_ylabel('')
        
        # CENTER subplot: keep x-axis label and legend.
        if i == int(len(model_list) / 2):
            ax.set_xlabel(xlabel, fontsize=label_size)
            lg = ax.legend(labels=labels, handles=handles, fancybox=False, 
                        loc='upper center', bbox_to_anchor=(0.5, -0.45), 
                        fontsize=ticklabel_size, ncol=len(handles))
            title = lg.get_title()
            title.set_fontsize(ticklabel_size)
            frame = lg.get_frame()
            frame.set_edgecolor('k')
            frame.set_linewidth(0.9)
        else:
            ax.set_xlabel('')
            ax.get_legend().remove()

        # RIGHT-MOST subplot: add experiment name to right side.
        if i == len(axarr) - 1:
            ax.yaxis.set_label_position('right')
            ax.set_ylabel(exp, labelpad=20, fontweight='bold', size='large', rotation=270)

    # Save final figure.
    plt.savefig(out_path, dpi=300, bbox_inches='tight')

#################################################################################
# Main function
#################################################################################

def main(args):
    # Get list of model names.
    if args.model == ['all']:
        model_list = utils.MODELS
    elif args.model == ['big']:
        model_list = utils.BIG_MODELS
    else:
        model_list = args.model

    # Ensure only large-vocabulary models are specified for M&L replication.
    if 'ml' in args.exp and any(m not in utils.BIG_MODELS for m in model_list):
        raise ValueError(
            'Only large-vocabulary models are compatible with '
            'Marvin & Linzen\'s (2018) materials. '
            'Please use "--model big" to plot the results from that experiment.'
        )
    
    # Assign file name based on name of experiment and specified models.
    out_path = Path(f'{args.out_prefix}/{args.exp}-{"_".join(args.model)}')

    # Construct dictionary of DataFrames, where each key is a model.
    model_data = {}
    for model in model_list:
        # Get data for each pronoun for current model.
        dfs = []
        for pn in utils.PRONOUNS:
            surp_ext = 'csv' if model == 'bert' else 'txt'
            surp_path = Path(
                f'../data/surprisal/{model}/{args.exp}/{pn}_{model}.{surp_ext}'
            )
            if model == 'bert':
                pn_df = pd.read_csv(surp_path)
            else:
                data_path = Path(f'../stimuli/{args.exp}/{pn}.csv')
                pn_df = utils.get_data_df(data_path, surp_path, args.exp, pn)
            dfs.append(pn_df)
        # Concatenate data for each pronoun and insert into data dictionary.
        model_data[model] = pd.concat(dfs, sort=True)

    # Subtract baseline from all surprisal values if necessary.
    if args.vs_baseline:
        for model, df in model_data.items():
            model_data[model] = utils.subtract_baseline(df)

    # Call the plotting function.
    plot_log_prob(
        model_data, out_path, args.exp, model_list, 
        vs_baseline=args.vs_baseline
    )
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot surprisal results.')
    parser.add_argument('--out_prefix', '-out_prefix', '--o', '-o',
                        default='figures/paper',
                        help='prefix to path to save final plots '
                             '(files will be named according to experiment)')
    parser.add_argument('--model', '-model', '--m', '-m', nargs='+',
                        help='list of model names, or "all" or "big"')
    parser.add_argument('--exp', '-exp', help='name of experiment')
    parser.add_argument('--vs_baseline', '-vs_baseline', '--vs', '-vs',
                        default=False, action='store_true',
                        help='toggle surprisal differential vs. baseline '
                             '(False --> plot raw surprisals)')
    args = parser.parse_args()
    main(args)

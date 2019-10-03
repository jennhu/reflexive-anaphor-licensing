"""
    accuracy.py
    Get accuracy results.
"""
import argparse
from pathlib import Path
from numpy import mean
import random
import pandas as pd

import utils

def get_accuracy(df, distractor_pos):
    item_list = df.item.unique()
    n_items = len(item_list)
    num_correct_vs_baseline = 0
    num_correct_vs_distractor = 0
    num_correct = 0

    for item in item_list:
        item_rows = df[df.item == item]
        baseline_rows = item_rows[item_rows.mismatch_position == 'none']
        distractor_rows = item_rows[item_rows.mismatch_position == distractor_pos]
        ungrammatical_rows = item_rows[item_rows.grammatical == 0]

        vs_baseline = ungrammatical_rows.surprisal.mean() - baseline_rows.surprisal.mean()
        vs_distractor = ungrammatical_rows.surprisal.mean() - distractor_rows.surprisal.mean()

        # Check if ungrammatical - baseline is positive.
        if vs_baseline > 0:
            num_correct_vs_baseline += 1

        # Check if ungrammatical - distractor is positive.
        if vs_distractor > 0:
            num_correct_vs_distractor += 1

        # Check if both differentials are positive.
        if vs_baseline > 0 and vs_distractor > 0:
            num_correct += 1

        # If both differentials are zero, then label correct with probability 1/3.
        elif vs_baseline == 0 and vs_distractor == 0:
            choice = random.choice(['baseline', 'distractor', 'ungrammatical'])
            if choice == 'ungrammatical':
                num_correct += 1

    # Calculate proportion of items where different accuracy conditions hold.
    vs_baseline_acc = num_correct_vs_baseline / float(n_items)
    vs_distractor_acc = num_correct_vs_distractor / float(n_items)
    total_acc = num_correct / float(n_items)

    return total_acc, vs_baseline_acc, vs_distractor_acc

#################################################################################
# Main function -- partially shared with generate_plot.py
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
    out_path = Path(f'{args.out_prefix}/{args.exp}-{"_".join(args.model)}.csv')

    acc_dict = []
    for model in model_list:
        # Get data for each pronoun for current model.
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

            # Assign appropriate mismatch position for distractor condition.
            if 'rc' in args.exp:
                distractor_pos = 'rc_subj'
            elif 'comp' in args.exp or 'ml' in args.exp:
                distractor_pos = 'nonlocal_subj'
            else:
                distractor_pos = 'distractor'

            total_acc, vs_baseline_acc, vs_distractor_acc = get_accuracy(
                pn_df, distractor_pos
            )
            acc_dict.append(dict(
                model=model, total_acc=total_acc, exp=args.exp, pronoun=pn,
                vs_baseline_acc=vs_baseline_acc, vs_distractor_acc=vs_distractor_acc
            ))
    acc_df = pd.DataFrame(acc_dict)
    acc_df.to_csv(out_path, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute accuracy for models.')
    parser.add_argument('--out_prefix', '-out_prefix', '--o', '-o',
                        help='prefix to path to save final .csv file '
                            '(file will be named according to experiment)')
    parser.add_argument('--model', '-model', '--m', '-m', nargs='+',
                        help='list of model names, or "all" or "big"')
    parser.add_argument('--exp', '-exp', help='name of experiment')
    args = parser.parse_args()
    main(args)

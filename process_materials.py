'''
    process_materials.py
    Saves sentences to separate files.
'''
import argparse
import pandas as pd

def main(exp, out_prefix):
    materials = pd.read_csv('materials/%s.csv' % exp)
    materials.sentence.to_csv('%s/%s_sentences.txt' % \
                              (out_prefix, exp), index=False)
    materials.sentence_no_eos.to_csv('%s/%s_sentences_no_eos.txt' % \
                                     (out_prefix, exp), index=False)
    materials.sentence.str.lower().to_csv('%s/%s_sentences_uncased.txt' % \
                              (out_prefix, exp), index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process materials.')
    parser.add_argument('--exp', '-exp', required=True,
                        help='name of experiment')
    parser.add_argument('--out_prefix', '-out_prefix', '--O', '-O',
                        default='materials',
                        help='prefix to path to save files')
    args = parser.parse_args()
    main(**vars(args))

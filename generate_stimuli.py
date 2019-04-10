'''
    generate_stimuli.py
    Generates materials to be used in RNNG experiment.
'''

import argparse
import util

def main(lex_path):
    lexicon = util.Lexicon(lex_path)
    # TODO: implement sentence generation here
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate stimuli.')
    parser.add_argument('--lex_path', '-lex_path', '--L', '-L', 
                        default='materials',
                        help='path to files containing lexical items')
    parser.add_argument('--out_path', '-out_path', '--O', '-O',
                        help='path to save final stimuli file')
    args = parser.parse_args()
    main(**vars(args))
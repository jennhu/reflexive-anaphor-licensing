'''
    generate_stimuli.py
    Generates materials to be used in RNNG experiment.
'''

import argparse
import util
import logging

def main(lex_path, out_path):
    # set up logger
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)
    log.info('Reading lexical items from %s' % lex_path)
    
    # dummy example -- saves 10 grammatical sentences
    L = util.Lexicon(lex_path)
    sentences = [L.generate_sentence(clause_type='simple') for _ in range(10)]
    util.write_sentences(sentences, out_path)
    log.info('Wrote sentences to %s' % out_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate stimuli.')
    parser.add_argument('--lex_path', '-lex_path', '--L', '-L', 
                        default='materials',
                        help='path to files containing lexical items')
    parser.add_argument('--out_path', '-out_path', '--O', '-O',
                        help='path to save final stimuli file')
    args = parser.parse_args()
    main(**vars(args))
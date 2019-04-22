'''
    generate_stimuli.py
    Generates materials to be used in experiment.
'''

import argparse
import util
import logging

def main(lex_path, out_path, n):
    # set up logger
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)
    log.info('Reading lexical items from %s' % lex_path)
    
    # generate grammatical sentences and remove duplicates
    L = util.Lexicon(lex_path)
    sentences = list(set([L.generate_sentence(clause_type='simple') 
                          for _ in range(n)]))
    
    # save data to file
    util.write_sentences(sentences, out_path)
    log.info('Wrote sentences to %s' % out_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate stimuli.')
    parser.add_argument('--lex_path', '-lex_path', '--L', '-L', 
                        default='materials/lexicon',
                        help='path to files containing lexical items')
    parser.add_argument('--out_path', '-out_path', '--O', '-O',
                        help='path to save final stimuli file')
    parser.add_argument('--n', '-n', type=int, default=20,
                        help='number of sentences to generate')
    args = parser.parse_args()
    main(**vars(args))

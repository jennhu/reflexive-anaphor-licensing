'''
    generate_stimuli.py
    Generates materials to be used in RNNG experiment.
'''

import argparse
import util
import logging

def main(lex_path, out_path, n):
    # set up logger
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)
    log.info('Reading lexical items from %s' % lex_path)
    
    # first generate grammatical sentences
    L = util.Lexicon(lex_path)
    grammatical_sentences = {
        'simple': list(set([L.generate_sentence(clause_type='simple') for _ in range(n)])),
        # 'embed': [L.generate_sentence(clause_type='embed') for _ in range(n)]
    }

    # generate sentences for all conditions based on grammatical sentences
    # all_sentences = util.generate_stimuli(grammatical_sentences)

    # save data to file
    util.write_sentences(grammatical_sentences['simple'], out_path)
    log.info('Wrote sentences to %s' % out_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate stimuli.')
    parser.add_argument('--lex_path', '-lex_path', '--L', '-L', 
                        default='materials',
                        help='path to files containing lexical items')
    parser.add_argument('--out_path', '-out_path', '--O', '-O',
                        help='path to save final stimuli file')
    parser.add_argument('--n', '-n', type=int, default=20,
                        help='number of sentences to generate')
    args = parser.parse_args()
    main(**vars(args))

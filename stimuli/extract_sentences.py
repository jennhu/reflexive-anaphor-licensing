'''
    extract_sentences.py
    Extracts sentences from stimuli file.
'''
import argparse
import pandas as pd

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extracts sentences from stimuli file.')
    parser.add_argument('--data', '-data', type=str, required=True,
                        help='path to stimuli data')
    parser.add_argument('--outf', '-outf', type=str, required=True,
                        help='path to save extracted sentences')
    parser.add_argument('--uncased', '-uncased', default=False, action='store_true',
                        help='whether to convert materials to lowercase')
    parser.add_argument('--eos', '-eos', default=False, action='store_true',
                        help='whether to add <eos> token to end of sentences')
    args = parser.parse_args()
    
    print(args)

    # Read stimuli file and select appropriate set of sentences.
    stimuli = pd.read_csv(args.data)
    sentences = stimuli.sentence if args.eos else stimuli.sentence_no_eos

    # Convert sentences to lowercase if necessary.
    if args.uncased:
        sentences = sentences.str.lower()

    # Write sentences to file.
    sentences.to_csv(args.outf, index=False)

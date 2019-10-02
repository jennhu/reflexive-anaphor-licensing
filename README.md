# A closer look at the performance of neural language models on reflexive anaphor licensing

This repository contains the code for the following paper:

Jennifer Hu, Sherry Yong Chen, and Roger Levy (2020). 
A closer look at the performance of neural language models on reflexive anaphor licensing. 
*Proceedings of the Society for Computation in Linguistics (SCiL 2020)* Volume 3.

If you use any of our code, data, or analyses, please cite the paper using the bib entry below:
```
@InProceedings{Hu:et-al:2020,
  Author = {Hu, Jennifer and Chen, Sherry Yong and Levy, Roger},
  Title = {A closer look at the performance of neural language models on reflexive anaphor licensing},
  Booktitle = {Proceedings of the Society for Computation in Linguistics Volume 3},
  Year = {2020}
}
```

## Overview

The surprisal data lives in the data folder, and the stimuli live in the stimuli folder.

**TODO**: mention that we designed lexical items to stay in-vocabulary for PTB models

1. [GRNN](https://github.com/facebookresearch/colorlessgreenRNNs) (recurrent neural network trained on Wikipedia)
2. [JRNN](https://github.com/tensorflow/models/tree/master/research/lm_1b) (recurrent neural network trained on [One Billion Word Benchmark](http://arxiv.org/abs/1312.3005))
3. [RNNG](https://github.com/clab/rnng) (recurrent neural network grammar)
4. [Transformer-XL](https://github.com/kimiyoung/transformer-xl)
5. [Tiny LSTM](https://github.com/pytorch/examples/tree/master/word_language_model)
6. n-gram

## Dependencies

See the parent repositories linked above for model-specific dependencies.
Our analysis code simply requires a basic scientific installation of Python
(`numpy`, `pandas`, `matplotlib`, etc.)

### Transformer-XL
Note that we use the [pytorch-pretrained-BERT](https://github.com/huggingface/pytorch-pretrained-BERT) implementation of Transformer-XL. To download the 
state-of-the-art model parameters, run the script `get_model.sh`.
After doing so, you'll need to load the model and tokenizer like this:

```python
tokenizer = TransfoXLTokenizer.from_pretrained('./model/')
model = TransfoXLModel.from_pretrained('./model/')
```

(Source: [Issue #451](https://github.com/huggingface/pytorch-pretrained-BERT/issues/451#issuecomment-481155274))

See [pytorch-pretrained-BERT](https://github.com/huggingface/pytorch-pretrained-BERT) 
for more detailed setup instructions.

## Data organization

Everything is organized by experiment name. An experiment is expected to have
three components:
1. `stimuli/<EXPERIMENT>.csv` 
    (list of conditions and stimuli)
2. `stimuli/<EXPERIMENT>_sentences.txt` 
    (list of sentences for most models)
3. `stimuli/<EXPERIMENT>_sentences_no_eos.txt` 
    (list of sentences with no `<eos>` token)

Then, the per-token surprisal values for a given model are saved to 
`data/<MODEL>/<EXPERIMENT>_surprisal_<MODEL>.txt`.

The plots are analogously saved to
`analysis/plots/<EXPERIMENT>_<MODEL>.png`.

## Running experiments

Given a full set of materials, run the script `./run_experiment.sh <EXPERIMENT>`
to generate the sentence files and obtain surprisals from all five models.

To generate the plots for a given experiment and model, run the following:
```bash
cd analysis
python plot_surprisals.py -exp <EXPERIMENT> -model <MODEL>
```
This will save a plot to `analysis/plots/<EXPERIMENT>_<MODEL>.png` showing
the mean surprisal at the target word across each condition.
The relevant target word (e.g. *himself*, *themselves*, *was*) will be
inferred from the name of the experiment.
# Controlled syntactic evaluation of neural language models

This repository contains the code for testing grammaticality judgments of 
English syntactic phenomena in five different language models:

1. [GRNN](https://github.com/facebookresearch/colorlessgreenRNNs) (recurrent neural network trained on Wikipedia)
2. [JRNN](https://github.com/tensorflow/models/tree/master/research/lm_1b) (recurrent neural network trained on [One Billion Word Benchmark](http://arxiv.org/abs/1312.3005))
3. [RNNG](https://github.com/clab/rnng) (recurrent neural network grammar)
4. [Transformer-XL](https://github.com/kimiyoung/transformer-xl)
5. [Tiny LSTM](https://github.com/pytorch/examples/tree/master/word_language_model)

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
1. `materials/<EXPERIMENT>_materials.csv` 
    (list of conditions and stimuli)
2. `materials/<EXPERIMENT>_sentences.txt` 
    (list of sentences for most models)
3. `materials/<EXPERIMENT>_sentences_no_eos.txt` 
    (list of sentences with no `<eos>` token for RNNG)

Then, the per-token surprisal values for a given model are saved to 
`surprisal_data/<MODEL>/<EXPERIMENT>_surprisal_<MODEL>.txt`.

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


## TODO

- [ ] Verbs: count in the corpus (Wiki?)
- [ ] Nouns: check frequency
- [ ] "Baseline baseline": no distracting NPs
- [ ] Counter-balancing of all N occurrences: double-check
- [ ] Accuracy vs. Surprisals?
- [ ] Unigram/Bigram probability of Refl/Copula in a corpus?




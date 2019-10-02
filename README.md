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

---

## Overview

**TODO: write short overview/summary here to orient people**

## Stimuli

For each experiment, a `.csv` file containing the stimuli can be found at 
`stimuli/<EXPERIMENT>.csv`, where `<EXPERIMENT>` corresponds to **TODO**. 
The file is structured as follows:

**SHERRY TODO: explain how stimuli file is structured**

To extract the sentences from this file, use the script
`extract_sentences.py`. You can toggle flags like `--uncased` and `--eos`
depending on the requirements of your model. **Please note that the final period
at the end of each sentence is separated by whitespace.** Otherwise, no 
tokenization assumptions are made.

### Vocabulary issues
In all of our novel materials (**TODO: list the experiment names**), the
lexical items are designed to be in-vocabulary for models trained on the
Penn Treebank. This is not the case for the materials used in Experiment 1, the 
[Marvin & Linzen (2018)](https://arxiv.org/abs/1808.09031) replication.

## Data
The per-token surprisal values for each model can be found in the [data](data)
folder, following the following naming convention:
```
data/<MODEL>/<EXPERIMENT>_surprisal_<MODEL>.txt
```

## Dependencies
Our analysis code requires a basic scientific installation of Python
(`numpy`, `pandas`, `matplotlib`, `seaborn`, etc.). 

If you would like to run a model on our materials -- 
whether to replicate our results or assess a new model -- 
you will have to set up the computing environment yourself. 
Please see the repositories linked below for the source code
of the models we evaluated (with the exception of n-gram, which uses SRILM).
We can make the training script for our n-gram model available upon request.

### Models evaluated in our analysis
1. [GRNN](https://github.com/facebookresearch/colorlessgreenRNNs) (Gulordava et al. 2018)
2. [JRNN](https://github.com/tensorflow/models/tree/master/research/lm_1b) (Jozefowicz et al. 2016)
3. [RNNG](https://github.com/clab/rnng) (Dyer et al. 2016; we use an unpublished version to get incremental RNNG parses, courtesy of Peng Qian)
4. [Transformer-XL](https://github.com/kimiyoung/transformer-xl) (Dai et al. 2019; we use the [huggingface](https://github.com/huggingface/transformers) implementation)
5. [Tiny LSTM](https://github.com/pytorch/examples/tree/master/word_language_model)
6. n-gram

<!-- ### Transformer-XL
Note that we use the [pytorch-pretrained-BERT](https://github.com/huggingface/pytorch-pretrained-BERT) implementation of Transformer-XL. To download the 
state-of-the-art model parameters, run the script `get_model.sh`.
After doing so, you'll need to load the model and tokenizer like this:

```python
tokenizer = TransfoXLTokenizer.from_pretrained('./model/')
model = TransfoXLModel.from_pretrained('./model/')
```

(Source: [Issue #451](https://github.com/huggingface/pytorch-pretrained-BERT/issues/451#issuecomment-481155274))

See [pytorch-pretrained-BERT](https://github.com/huggingface/pytorch-pretrained-BERT) 
for more detailed setup instructions. -->


## Reproducing our figures

To generate the plots for a given experiment and model, run the following:
**TODO: FIX/CLEAN THIS**

```bash
cd analysis
python plot_surprisals.py -exp <EXPERIMENT> -model <MODEL>
```
This will save a plot to `analysis/plots/<EXPERIMENT>_<MODEL>.png` showing
the mean surprisal at the target word across each condition.
The relevant target word (e.g. *himself*, *themselves*, *was*) will be
inferred from the name of the experiment.
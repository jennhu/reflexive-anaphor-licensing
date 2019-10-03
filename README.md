# A closer look at the performance of neural language models on reflexive anaphor licensing

This repository contains the materials for the following paper:

> Jennifer Hu, Sherry Yong Chen, and Roger Levy (2020). 
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

Our materials are organized into three primary folders:
* [analysis](analysis) (code for reproducing the results and figures in the paper)
* [data](data) (accuracy and surprisal results from each model)
* [stimuli](stimuli) (test suites and script for extracting sentences)

Please note that we do not provide code for running each model. For more details, see the [Dependencies](#dependencies) section.

## Stimuli

For each experiment, a `.csv` file containing the stimuli can be found at 
`stimuli/<EXPERIMENT>/<PRONOUN>.csv`. The file is structured as follows:

| column name | values | related experiment | purpose |
| ------------- | ------------- | ------------- | ------------- |
| item | 1/2/3/... | 1-4 | indicates the item number in that experiemnt |
| clause_type  | embed/simple | 1-4 | indicates whether there's an embedded clause (for sentential complement & relative clause constructions) or just one single clause (for prepositional phrases)  |
| locality | local/nonlocal | 1-3 | indicates whether the intended antecedent NP is in the same clause (local) or the matrix clause (non-local) |
| c-command | c-command/no-c-command | 1a,2,4 | indicates whether the intended antecedent NP is in a c-commanding relation with the reflexive or not |
| grammatical | 1/0 | 1-4 | indicates whether the item is grammatical (1) vs ungrammatical (0) |
| counterbalance | a/b(/c/d) | 1-4 | indicates the counterbalancing of the vocabulary used, to ensure that every vocab item appears the same amount of time |
| mismatch_position | none/X | 1-4 | where X is {"head_noun","distractor_noun","local_sub","nonlocal_subj","matrix_subj_noun","rc_subj_noun"}, indicates which NP involves mismatching features (if applicable) |
| mismatch_feature | none/number | 1-4 | indicates what feature is mismatched, or there's no mismatch (in the case of grammatical sentences) |
| head_noun/distractor_noun | vocab | 4 | indicates whether the antecedent NP is the head noun (licensing position) or a distracting noun inside the prepositional phrase (non-licensing position)  |
| local_sub/nonlocal_subj | vocab | 1b,3 | indicates whether the antecedent NP is the subject of the local clause (licensing position) or the subject of the superoridnate/matrix clause (non-licensing position) |
| matrix_subj_noun/rc_subj_noun | vocab | 1a,2 | indicates whether the antecedent NP is the subject of the matrix clause (licensing position) or a noun inside the relative clause (non-licensing position)   |
| verb | vocab | 1-4 | indicates the verb used for that item   |
| pronoun | herself/himself/themselves | 1-4 | indicates which reflexive pronoun is being investigated |
| sentence/sentence_no_eos | sentence | 1-4 | compiles the whole sentence for that item |


### Extracting sentences
To extract the sentences from this file, use the script
`stimuli/extract_sentences.py`. You can toggle flags like `--uncased` and `--eos`
depending on the requirements of your model. **Please note that the final period
at the end of each sentence is separated by whitespace.** Otherwise, no 
tokenization assumptions are made.

### Selecting lexical items
The [stimuli/lexicon](stimuli/lexicon) folder contains code and
counts of nouns, pronouns, and verbs in the GRNN Wikipedia
training corpus. See the paper for more details on how we
constructed our materials.

### Vocabulary issues
In all of our novel materials (**TODO: list the experiment names**), the
lexical items are designed to be in-vocabulary for models trained on the
Penn Treebank. This is not the case for the materials used in Experiment 1, the 
[Marvin & Linzen (2018)](https://arxiv.org/abs/1808.09031) replication.

## Data
The per-token surprisal values for each model can be found in the [data](data)
folder, following this naming convention:
```
data/<MODEL>/<EXPERIMENT>/<PRONOUN>_<MODEL>.txt
```
The BERT data is in a slightly different `.csv` format, but otherwise
follows the same naming convention.

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

## Reproducing our results

### Figures
To generate the plots for a given experiment and model, run the following:

```bash
cd analysis
mkdir figures
python plot_for_paper.py -o figures -model <MODELS> -exp <EXPERIMENT> -vs
```
This will save a plot to `analysis/figures/<EXPERIMENT>_<MODEL>.png`.
The `-vs` flag specifies to plot the negative log probability **differential**.
You can omit the flag to plot the raw negative log probabilities.

To plot the results for all our experiments, run the following
(replacing `figures` with your desired output folder, which will be created
if it does not exist):

```bash
cd analysis
./plot_all figures
```

### Accuracy

**TODO**

# Controlled syntactic evaluation of neural language models

This repository contains the code for testing grammaticality judgments of 
English syntactic phenomena in five different language models:

1. Recurrent neural network trained on Wikipedia ([GRNN](https://github.com/facebookresearch/colorlessgreenRNNs))
2. Recurrent neural network trained on [One Billion Word Benchmark](http://arxiv.org/abs/1312.3005) ([JRNN](https://github.com/tensorflow/models/tree/master/research/lm_1b))
3. Recurrent neural network grammar ([RNNG](https://github.com/clab/rnng))
4. [Transformer-XL](https://github.com/kimiyoung/transformer-xl)
5. TinyLSTM

## Dependencies

See the parent repositories linked above for model-specific dependencies.
Our analysis code simply requires a basic scientific installation of Python.

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
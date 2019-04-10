# Reflexive pronoun licensing in recurrent neural network grammars

This repository contains the code for testing RNNG grammaticality judgments of English reflexive pronouns.

## Dependencies

See these [prerequisites](https://github.com/clab/rnng#prerequisites) for RNNG dependencies.

## Surprisal data

The filename of a surprisal file should have the following format:

`surprisals.<CLAUSE_TYPE>.<MISMATCH>.<RELATION>.txt`,

where `<RELATION>` takes a value from `[ccommand, noccommand]` 
if `<CLAUSE_TYPE>` is `simple`,
and `<RELATION>` takes a value from `[local, nonlocal]` 
if `<CLAUSE_TYPE>` is `embed`.

## TODO

- [ ] pilot before meeting Roger
- [ ] generate stimuli
- [ ] create Singularity image with dependencies
- [ ] get GRNN surprisals
- [ ] get RNNG surprisals


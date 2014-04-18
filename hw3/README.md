There are three Python programs here (`-h` for usage):

 - `./decode` a simple non-reordering (monotone) phrase-based decoder
 - `./grade` computes the model score of your output

The commands are designed to work in a pipeline. For instance, this is a valid invocation:

    ./decode | ./grade


The `data/` directory contains the input set to be decoded and the models

 - `data/input` is the input text

 - `data/lm` is the ARPA-format 3-gram language model

 - `data/tm` is the phrase translation model

----- Method ------
0. Generated "divided" permutations of the foreign sentence. i.e.  Divide a length n sentence into n/k parts. Pemuate each of those n/k parts.
    Under above conditions
    0.1. Increasing stacksize from 20 to 100 does not change score.
    0.1 k=2, can be finished in reasonable time, else time taken is a LOT.
    Permuted both the source and the target. Unfortunately no significant/no improvement in performance.
    0.2 Ran the permutations, through the grading algorithm itself, so that I could output the highest graded permuation, as said earlier this time --running all permutations to give back highest scoring permuations takes A LOT of time.

    I was doing this without implementing the baseline, in the hope that a simpler solution might circumvent the baseline.
    

1. Implemented future cost. Implemented by calculating and storing cost of translating segment from word i to word j- "future_cost_estimation". Stored it so that it may be referenced later. Changed the hypothesis structure to keep track of already translated parts, current cost etc.Thus implemented a elaborate baseline. Unfortunately ran into bugs, that took up a lot of time!
 
2. Failed attempts are in decode1, decode2, decode3.

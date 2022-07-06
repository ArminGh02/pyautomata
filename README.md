# pyautomata

## About
Convert any regular grammar to NFA and DFA and get the image of the corresponding graph.  
Also check if an input string belongs the language described by the regular grammar.

## Example
[grammar_input.json](grammar_input.json) file is the input of the program.  
Given this grammar:

```
A->aA
A->aB
B->bB
B->b
```

The generated graph for NFA is:

![NFA](/NFA.png "NFA")

and the output graph for DFA is:

![DFA](/DFA.png "DFA")

## See also
**[Factorial Turing Machine](https://gist.github.com/ArminGh02/e3859f1e1843cd8872b77dab400d2040)**

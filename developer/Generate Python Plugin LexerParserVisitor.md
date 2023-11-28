# How to generate Python Plugin Lexer/Parser/Visitor

------



## Introduction

We use the antrl4 toolbox

We use this [grammar](https://github.com/kaby76/grammars-v4/tree/master/python/python3/Python3)

![GrammarFiles](./GrammarFiles.png)

## Set up the virtual environment





```bash
python -m venv pyenv-antlr-4.13.1
source pyenv-antlr-4.13.1/bin/activate
pip install antlr4-tools
```



Get the complete jar from https://www.antlr.org/download.html

Get the lexer/parser .g4 files from here:  https://github.com/kaby76/grammars-v4/tree/master/python/python3

![AuxillaryFiles](./AuxillaryFiles.png)

## Generate Python 3.11.5 parser



### Updates .g4 files for python

```bash
python transformGrammar.py
```



### Finally

```bash
antlr4 -Dlanguage=Python3 -visitor -no-listener -package pyutplugins.ioplugins.python -o pythonparser *.g4
```

Copy the files in the `pythonparser` directory back to the git sandbox
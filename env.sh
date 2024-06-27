#!/bin/bash

eval "$(pyenv init -)"
pyenv shell 3.7.10
source myvenv/bin/activate
export PYTHONPATH=.:$PYTHONPATH


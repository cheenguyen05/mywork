#!/bin/bash

eval "$(pyenv init -)"
pyenv shell 3.7.10
source venv/bin/activate
export PYTHONPATH=.:$PYTHONPATH


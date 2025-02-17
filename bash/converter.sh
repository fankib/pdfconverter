#!/bin/bash

source /home/benjamin/git/pdfconverter/venv/bin/activate

python /home/benjamin/git/pdfconverter/converter.py "$@"

deactivate
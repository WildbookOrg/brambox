#!/bin/bash
# Install dependency packages

#if [[ "$(which docker)" != "" ]]; then
#    echo "building with docker"
#    BDIST_FPATH=$(./run_multibuild.sh)
#    pip install $BDIST_FPATH
#else

pip install -r requirements.txt
# new pep makes this not always work
# pip install -e .

./clean.sh

python setup.py clean
python setup.py develop
pip install -e .

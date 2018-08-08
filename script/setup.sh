#! /bin/bash

pyenv install 3.6.6

cd ..
pyenv virtualenv 3.6.6 classical-semantics
cd classical-semantics

pip install --upgrade pip

pip install -r requirements.txt

echo "Done"

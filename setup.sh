#! /bin/bash

brew bundle

pipenv install --ignore-pipfile --dev

echo "Done"

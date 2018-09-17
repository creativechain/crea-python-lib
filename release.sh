#!/bin/bash

TAG=$1
MSG="Version ${TAG}"

git add .
git commit -m ${MSG}
git tag v${TAG} -m ${MSG}

rm -rf dist/*

python3 setup.py sdist bdist_wheel

twine upload dist/*
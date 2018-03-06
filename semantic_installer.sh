#!/bin/sh

set -xe

cd arduinozore/static
wget https://github.com/Semantic-Org/Semantic-UI-CSS/archive/master.zip -O semantic.zip
unzip semantic.zip
mv Semantic-UI-* semantic
rm semantic.zip

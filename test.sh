#!/bin/sh

set -xe

isort --recursive .
flake8 .

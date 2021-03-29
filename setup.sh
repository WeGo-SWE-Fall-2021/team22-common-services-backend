#!/bin/bash

BASEDIR=$(dirname "$0");
# Install python dependencies
$BASEDIR/env/bin/python3 -m pip install -r $BASEDIR/requirements.txt;

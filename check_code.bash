#!/bin/bash
echo "Check Python"
pep8 --config=pep8 --exclude='*bin/splunklib*' bin/
echo "Check Javascript"
jshint appserver/static/heremaps/*.js

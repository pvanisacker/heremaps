#!/bin/bash
flake8 .
test=$?
if [ "$test" != 0 ] ; then
    exit 1
fi

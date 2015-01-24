#!/bin/bash -x
pep8 --config=pep8 --exclude='*bin/splunklib*' bin/
code=$?
pep8 --config=pep8 test/integration/search
test=$?
if [ "$code" != 0 ] || [ "$test" != 0 ] ; then
    exit 1
fi
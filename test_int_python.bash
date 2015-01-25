#!/bin/bash
echo "Deleting cached results"
rm -rf bin/lib/*.cache

echo "----------------------------------------"
echo "Running tests without cache"
nosetests-2.7 -s --with-timer --with-html-output --html-out-file=python-int.html test/integration/search/*.py
test_nocache=$?

echo "----------------------------------------"
echo "Running tests with cache"
nosetests-2.7 -s --with-timer --with-html-output --html-out-file=python-int.html test/integration/search/*.py
test_cache=$?

if [ "$test_nocache" != 0 ] || [ "$test_cache" != 0 ] ; then
    exit 1
fi
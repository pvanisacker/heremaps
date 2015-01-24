#!/bin/bash
# Delete cached results
rm -rf bin/lib/*.cache

echo "----------------------------------------"
echo "Running tests without cache"
nosetests-2.7 -s --with-timer --with-html-output --html-out-file=python-int.html test/integration/search/*.py

echo "----------------------------------------"
echo "Running tests with cache"
nosetests-2.7 -s --with-timer --with-html-output --html-out-file=python-int.html test/integration/search/*.py

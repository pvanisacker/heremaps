#!/bin/bash
rm -rf tmp
mkdir -p tmp/heremaps
cp -r bin tmp/heremaps
cp -r appserver tmp/heremaps
cp -r default tmp/heremaps
cp -r django tmp/heremaps
cp -r lookups tmp/heremaps
cd tmp
tar -czvf heremaps.spl heremaps --owner=0 --group=0
cd ..
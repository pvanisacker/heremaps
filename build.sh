#!/bin/bash
# Clean up previous build
rm -rf tmp

# Make new dir
mkdir -p tmp/heremaps

# Copy over all the needed things
cp -r bin tmp/heremaps
cp -r appserver tmp/heremaps
cp -r default tmp/heremaps
cp -r lookups tmp/heremaps
rm -rf tmp/heremaps/bin/reversegeocode.cache
rm -rf tmp/heremaps/bin/reversegeocodeshape-*
rm -rf tmp/heremaps/bin/*.pyc

cd tmp
tar -czvf heremaps.spl heremaps --owner=0 --group=0
cd ..
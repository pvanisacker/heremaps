#!/bin/bash
# Clean up previous build
rm -rf tmp

# Make new dir
mkdir -p tmp/heremaps

# Copy over all the needed things
cp -r bin tmp/heremaps
cp -r appserver tmp/heremaps
cp -r default tmp/heremaps
cp -r django tmp/heremaps
cp -r lookups tmp/heremaps
rm -rf tmp/heremaps/bin/reversegeocode.cache

# Copy over the needed files to make HTML dashboard creation easier
cp -r django/heremaps/static/* tmp/heremaps/appserver/static

# Replace one small line in the copied files
sed -i "s/require('heremaps\/heremap')/require('app\/heremaps\/heremaps\/heremap')/" tmp/heremaps/appserver/static/heremaps/heremarkermap.js
sed -i "s/require('heremaps\/heremap')/require('app\/heremaps\/heremaps\/heremap')/" tmp/heremaps/appserver/static/heremaps/hereclustermap.js
sed -i "s/require('heremaps\/heremap')/require('app\/heremaps\/heremaps\/heremap')/" tmp/heremaps/appserver/static/heremaps/hereshapemap.js
sed -i "s/require('heremaps\/heremap')/require('app\/heremaps\/heremaps\/heremap')/" tmp/heremaps/appserver/static/heremaps/hereheatmap.js

cd tmp
tar -czvf heremaps.spl heremaps --owner=0 --group=0
cd ..
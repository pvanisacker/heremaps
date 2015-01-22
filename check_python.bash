#!/bin/bash
pep8 --config=pep8 --exclude='*bin/splunklib*' bin/
pep8 --config=pep8 test/integration/search
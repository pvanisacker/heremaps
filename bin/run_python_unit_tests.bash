#!/bin/bash
nosetests-2.7 -s --with-html-output --html-out-file=test-result.html --with-coverage3 --cover3-html --cover3-html-dir=coverage --cover3-package=tools $1


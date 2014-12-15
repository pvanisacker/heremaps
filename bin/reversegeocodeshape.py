import os
import sys
import subprocess

python = "/usr/bin/python"
args = [python, os.path.join(os.environ['SPLUNK_HOME'], 'etc/apps/heremaps/bin/reversegeocodeshape_real.py')]
args = args+sys.argv[1:]
subprocess.call(args)

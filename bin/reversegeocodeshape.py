import os
import sys
import subprocess
import platform

python = "/usr/bin/python"
if platform.system() == "Windows":
    python = "C:\Python27\python.exe"

args = [python, os.path.join(os.environ['SPLUNK_HOME'], 'etc/apps/heremaps/bin/reversegeocodeshape_real.py')]
args = args+sys.argv[1:]
subprocess.call(args)

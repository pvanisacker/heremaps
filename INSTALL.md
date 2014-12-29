# Install

## reversegeocodeshape command

To use the reversegeocodeshape command additional installation effort is required.  
For using it you need a seperate python 2.7 runtime that has some more python packages installed.  

### For Windows

Install python 2.7 from https://www.python.org/downloads/windows/

Install the python Shapely package for your python 2.7 from http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely  

Once that is done configure the python path in SPLUNK_HOME/etc/apps/heremaps/bin/reversegeocodeshape.py
<pre><code>
import os
import sys
import subprocess

python = "C:\Python27\python.exe"
args = [python,os.path.join(os.environ['SPLUNK_HOME'], 'etc/apps/heremaps/bin/reversegeocodeshape_real.py')]
args = args+sys.argv[1:]
subprocess.call(args)
</code></pre>

After installing try running SPLUNK_HOME/bin/splunk cmd python SPLUNK_HOME/etc/apps/heremaps/bin/reversegeocodeshape.py __GETINFO__  
It should now throw any exception but show some CSV like content.

### For Linux/OSX
Make sure you have python 2.7 and it's development tools installed.  

Then install the geos library from http://trac.osgeo.org/geos/ for some distributions there might already be packages available.

Then install the Shapely package.
<pre><code>
pip install shapely
</code></pre>

Once that is done configure the python path in SPLUNK_HOME/etc/apps/heremaps/bin/reversegeocodeshape.py
<pre><code>
import os
import sys
import subprocess

python = "/usr/bin/python"
args = [python,os.path.join(os.environ['SPLUNK_HOME'], 'etc/apps/heremaps/bin/reversegeocodeshape_real.py')]
args = args+sys.argv[1:]
subprocess.call(args)
</code></pre>

After installing try running SPLUNK_HOME/bin/splunk cmd python SPLUNK_HOME/etc/apps/heremaps/bin/reversegeocodeshape.py __GETINFO__  
It should now throw any exception but show some CSV like content.
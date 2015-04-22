# Customization using SimpleXML dashboards

## Common config

You need to create one directory in your app to save your html dashboards: default/data/ui/views.  
When done your directory structure should look like this:

<pre><code>
- $SPLUNK_HOME/etc/apps/myspecialapp
  - default
    - data
      - ui
        - nav
        - views
    - app.conf
  - ...
</code></pre>


When creating an SimpleXML dashboards try to use one of the dashboards provided in the app as a base dashboard.  
If that's not possible make sure your dashboard/form includes the following:
 * a "script" argument pointing to "autodiscover.js"
 * an HTML panel containing a div with a specific id
 * the data-require argument & data-options argument should be filled in.

## Marker map

Documentation is not ready yet.

## Cluster map

Documentation is not ready yet.

## Shape map

Documentation is not ready yet.

## Heat map

Documentation is not ready yet.

## Line map

Documentation is not ready yet.
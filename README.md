# Intro

A Splunk app for map visualizations using HERE maps  
It includes 4 different visualizations types, one reverse geocoding custom command and a couple of csv lookups containing example data.

The code is available on github: https://github.com/pvanisacker/heremaps  
For questions about the app, please raise them on http://answers.splunk.com  
When you spot bugs please file an issue on https://github.com/pvanisacker/heremaps/issues

Note this app is not at all supported by HERE.  
And the app is an early state of development so there will be tons of bugs.

Enjoy!

# License

The app itself is distributed under the Creative Commons license.  
Example data is taken from wikipedia wich also uses a Creative Commons license: http://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License  
And the KML files for shape maps were created from data of http://www.naturalearthdata.com/.
The app uses HERE api's, for information see: http://developer.here.com

# Installation & Setup

For installing the app, just follow the standard splunk app procedures.  
Once it is installed, you also have to get free api credentials for using the HERE api.  
Request them on http://developer.here.com.  
Once you have them either use setup screen to configure the app_id and app_code.

Or by configuring it manually in the local/setup.conf:
<pre><code>[heremaps]
app_id=my_app_id
app_code=my_app_code
</code></pre>

Without these settings the app will not work.

# Usage

## reversegeocode command

This command uses the HERE REST api. So you need internet connectivity to get it working.  
It requires a floating point lat and lng field and will add new fields containing the information for this lat/lng.  
The fields that will be added:
  * regeo_country
  * regeo_state
  * regeo_region
  * regeo_county
  * regeo_district
  * regeo_postalcode
  * regeo_city
  * regeo_label

You'll see that not all of these fields are returned.  
The country value is an ISO3166 3 letter code.  

Example:
<pre><code>index=_internal | head 1 | eval lat=51 | eval lng=6 | reversegeocode | fields lat,lng,regeo* | table lat,lng,regeo*</code></pre>

| lat | lng | regeo_city | regeo_country | regeo_county | regeo_district | regeo_label                               | regeo_postalcode | regeo_region | regeo_state |
|-----|-----|------------|---------------|--------------|----------------|-------------------------------------------|------------------|--------------|-------------|
| 51  | 6   | Gangelt    | DEU           | Heinsberg    |                | Gangelt, Nordrhein-Westfalen, Deutschland | 52538            |              | Nordrhein-Westfalen |


By default the command will look for a "lat" and "lng" field in the event and prefix the new fields with "regeo_".  
This behaviour is customizable through the command options:

<pre><code>index=_internal | head 1 | eval latitude=51 | eval longitude=6 | reversegeocode lat=latitude,lng=longitude,prefix=myprefix| fields latitude,longitude,myprefix* | table latitude,longitude,myprefix*</code></pre>

| latitude | longitude | myprefix_city | myprefix_country | myprefix_county | myprefix_district | myprefix_label                               | myprefix_postalcode | myprefix_region | myprefix_state |
|-----|-----|------------|---------------|--------------|----------------|-------------------------------------------|------------------|--------------|-------------|
| 51  | 6   | Gangelt    | DEU           | Heinsberg    |                | Gangelt, Nordrhein-Westfalen, Deutschland | 52538            |              | Nordrhein-Westfalen |

Internally command includes a small cache to avoid calling the HERE api too often.  
By default it stores 1000000 results for 62 days.
The reverse geocode command will internally also round lat/lng combinations to a 5 digit precision to increase the cache hit ratio.

## reversegeocode macro

The ISO3166 3 letter code is not that usefull to work with. The app includes a csv lookup that can be used to get a readable country name.  
Use that lookup throught the `reversegeocode` macro.  

<pre><code>index=_internal | head 1 | eval lat=51 | eval lng=6 | `reversegeocode` | fields lat,lng,regeo* | table lat,lng,regeo*</code></pre>

| lat | lng | regeo_city | regeo_country |regeo_coutnry_iso3166_2 | regeo_country_latitude | regeo_contry_longitude | regeo country_name | regeo_county | regeo_district | regeo_label                               | regeo_postalcode | regeo_region | regeo_state |
|-----|-----|------------|---------------|------------------------|------------------------|------------------------|--------------------|--------------|----------------|-------------------------------------------|------------------|--------------|-------------|
| 51  | 6   | Gangelt    | DEU           | DE                     | 51.165691              | 10.451526              | Germany            | Heinsberg    |                | Gangelt, Nordrhein-Westfalen, Deutschland | 52538            |              | Nordrhein-Westfalen |

## Visualizations

The app contains 4 different map visualizations.
   * Marker map: displaying markers for lat/lng combinations
   * Cluster map: clusters markers together to get a better overview.
   * Shape map: colors shapes depending on the values
     These maps use a KML file to highlight certain areas. The KML files need a specific structure. See the custom.kml file for an example.
   * Heat map: shows density or value heatmaps of your data.
   
Except for the heat map, all of the visualization use v3 of the HERE javascript API.  
The heatmap visualization still uses v2.5.

The app contains examples on how to include them into Django and Javascript based dashboards when you are using the Splunk web framework.

If you're not using the web framework you can still include these visualizations in HTML dashboards. The visualizations cannot be included in simple or advanced XML dashboards.  
For creating an HTML dashboard see the instructions below. (It's rather hard for now :-( )

### Common config

You need to create one directory in your app to save your html dashboards: default/data/ui/html.  
When done your directory structure should look like this:

<pre><code>
- $SPLUNK_HOME/etc/apps/myspecialapp
  - default
    - data
      - ui
        - nav
        - views
        - html
    - app.conf
  - ...
</code></pre>

When creating an HTML dashboard you also need to make sure to include the needed javascript and CSS resources.
<pre><code>
    <script src="https://js.api.here.com/v3/3.0/mapsjs-core.js" type="text/javascript" charset="utf-8"></script>
    <script src="https://js.api.here.com/v3/3.0/mapsjs-service.js" type="text/javascript" charset="utf-8"></script>
    <script src="https://js.api.here.com/v3/3.0/mapsjs-mapevents.js" type="text/javascript" charset="UTF-8"></script>
    <script src="https://js.api.here.com/v3/3.0/mapsjs-ui.js" type="text/javascript"  charset="UTF-8"></script>
    <script src="https://js.api.here.com/v3/3.0/mapsjs-clustering.js" type="text/javascript" charset="utf-8"></script>
    <script src="https://js.api.here.com/v3/3.0/mapsjs-data.js" type="text/javascript" charset="utf-8"></script>
    <link href="https://js.api.here.com/v3/3.0/mapsjs-ui.css" rel="stylesheet" type="text/css" />
    <link href="{{SPLUNKWEB_URL_PREFIX}}/static/app/heremaps/heremaps/heremap.css" rel="stylesheet" type="text/css" />
</pre></code>

Once that's done you can start configuring the visualization.


### Marker map

For using a marker map you need to load the "app/heremaps/heremaps/heremarkermap" dependency.  
And then you can create a new marker map:

<pre><code>
var mymarkermap = new HereMarkerMap({
  id: "markermap1",
  managerid: "search1",
  el: $("#markermap-div"),
  height: "400px",
}).render()
</pre></code>

### Cluster map

For using a marker map you need to load the "app/heremaps/heremaps/hereclustermap" dependency.  
And then you can create a new marker map:

<pre><code>
var myclustermap = new HereClusterMap({
  id: "clustermap1",
  managerid: "search1",
  el: $("#markermap-div"),
  height: "400px",
}).render()
</pre></code>

### Shape map

### Heat map

# Versions
   * 0.1: First version, includes marker map, cluster map and shape map.
   * 0.2: Add more shapemaps. Add heatmaps, fix bug with reverse geocoding command. Make markers clickable.

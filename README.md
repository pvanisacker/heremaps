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
Deleting the cache can be done by deleting the reversegeocode.cache file in the bin directory of the app.

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
For creating an HTML dashboard see the instructions below in the customization part.
And you will find examples in the default/data/ui/html directory.

### Usage

The visualization can render quite some data points/markers. But as these visualizations are rendered on browser side there are limits.  
To avoid your brower from becoming slow when rendering data, try to aggregate as much data as possible already on server side.  
If you have a search that returns tons of data, you could use the following:
<pre><code>
... | eval lat=round(lat,4) | eval lng=round(lng,4) | stats count as value by lat,lng 
</pre></code>

### Marker map

For using a marker map your search needs to return events that contain a "lat" and a "lng" field in a floating point form.  
Optionally the event can also contain a "value" field that is used for displaying in the bubble when a marker is clicked.

### Cluster map

A cluster map requires the same search data as a marker map.

### Shape map

For rendering a shape map your search needs to return events that contain a "key" and "value" field.  
The key needs to match with the description of the KML placemark to make sure it gets colored correctly.  
Out of the box the app provides a couple of KML files:
   * world2.kml: key is the ISO3166 2 letter code code
   * world3.kml: key is the ISO3166 3 letter country code
   * fr.kml: key is the name of the department
   * ...

### Heat map

A heat map requires the same search data as a marker map.

### Customization

#### Common config

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


#### Marker map

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

By default when markers are clicked a small bubble will appear showing the value of that marker.  
If you don't want that create your marker map like this
<pre><code>
var mymarkermap = new HereMarkerMap({
  id: "markermap1",
  managerid: "search1",
  el: $("#markermap-div"),
  height: "400px",
  bubbleContentProvider: undefined
}).render()
</pre></code>

If you like to customize the bubble you can do the following:
<pre><code>
var mymarkermap = new HereMarkerMap({
  id: "markermap1",
  managerid: "search1",
  el: $("#markermap-div"),
  height: "400px",
  bubbleContentProvider: function(data){return "<div style='text-align:center;'>"+data["_time"]+": +data["value"]+"</div>";}
}).render()
</pre></code>
The data passed to the function is the actual event. So you can add any fields of your result to the bubble.

You can customize the vizualization of a marker. See the example below that uses an SVG marker that displays a field from the event.  
More information about creating a marker can be found on http://developer.here.com/javascript-apis/documentation/v3/maps/topics/markers.html
<pre><code>
var svgMarkup='<svg width="26" height="26" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg"><circle opacity="0.9" id="svg_1" r="12" cy="13" cx="13" stroke-width="2" stroke="#333333" fill="#f5f5f5"/><text xml:space="preserve" text-anchor="middle" id="svg_2" y="18.5" x="13" stroke-width="0" font-size="10pt" font-family="Roboto" stroke="#000000" fill="#000000">${TEXT}</text></svg>'
var markerfunction= function(data){
  var value=("value" in data) ? data["value"] : "";
  var svg=svgMarkup.replace('${TEXT}',value);
  var markerIcon = new H.map.Icon(svg,{anchor:{x:12,y:12}});
  return new H.map.Marker({lat:data["lat"],lng:data["lng"]},{icon: markerIcon});
}
            
var mymarkermap = new HereMarkerMap({
  id: "markermap1",
  managerid: "search1",
  el: $("#markermap-div"),
  height: "400px",
  marker: markerfunction,
}).render()
</pre></code>


#### Cluster map

For using a cluster map you need to load the "app/heremaps/heremaps/hereclustermap" dependency.  
And then you can create a new cluster map:

<pre><code>
var myclustermap = new HereClusterMap({
  id: "clustermap1",
  managerid: "search1",
  el: $("#search-map"),
  height: "400px",
}).render()
</pre></code>

Cluster markers can currently not be clicked.  
But you can customize the look of them by creating a theme.  
See the example below and look at http://developer.here.com/javascript-apis/documentation/v3/maps/topics/clustering.html

<pre><code>
var noiseSvgTemplate2 = '<svg width="20" height="20" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg"><circle opacity="0.9" id="svg_1" r="9" cy="10" cx="10" stroke-width="0" fill="${FILL}"/><text xml:space="preserve" text-anchor="middle" id="svg_2" y="15" x="10" stroke-width="0" font-size="8pt" font-family="Roboto" stroke="#000000" fill="#000000">${TEXT}</text></svg>';
var clusterSvgTemplate2 =
    '<svg xmlns="http://www.w3.org/2000/svg" height="50px" width="50px">'+
    '<circle cx="25px" cy="25px" r="${RADIUS}" fill="${FILL}" stroke-dasharray="5,5" stroke-width="6" stroke="#757575"/>'+
    '<text xml:space="preserve" text-anchor="middle" id="svg_2" y="30" x="25" font-size="10pt" font-family="Roboto" stroke="#000000" fill="#000000">${TEXT}</text>'+
    '</svg>';

var theme2={
    getClusterPresentation: function(cluster) {
        // Prepare SVG with correct content
        var max=0
        cluster.forEachDataPoint(function(dataPoint){
            value=parseFloat(dataPoint.getData()["value"]);
            if(max<value){
                max=value;
            }
        });
        var fill = ( max < 5 ? "orange" : "red")
        var svgString = clusterSvgTemplate2.replace('${RADIUS}', max*3.5 );
        var svgString = svgString.replace('${TEXT}',max);
        var svgString = svgString.replace('${FILL}',fill);
        var clusterIcon = new H.map.Icon(svgString, {
            size: { w: 50, h: 50},
            anchor: { x: 25, y: 25}
        });

        // Create a marker for clusters:
        var clusterMarker = new H.map.Marker(
            cluster.getPosition(),
            {icon: clusterIcon, min: cluster.getMinZoom(), max: cluster.getMaxZoom()}
        );

        // Bind cluster data to the marker:
        clusterMarker.setData(cluster);
        return clusterMarker;
    },
    getNoisePresentation: function(noisePoint) {
        // Prepare SVG with correct content
        var fill = ( parseFloat(noisePoint.getData()[value]) < 5 ? "orange" : "red")
        var svgString = noiseSvgTemplate2.replace('${TEXT}',noisePoint.getData()["value"]);
        var svgString = svgString.replace('${FILL}',fill);
        var noiseIcon = new H.map.Icon(svgString, {size: { w: 20, h: 20 },anchor: { x: 10, y: 10}});

        // Create a marker for noise points:
        var noiseMarker = new H.map.Marker(
            noisePoint.getPosition(),
            {icon: noiseIcon,min: noisePoint.getMinZoom()}
        );

        // Bind noise point data to the marker:
        noiseMarker.setData(noisePoint);
        return noiseMarker;
    }
}

// Create the cluster map
var myclustermap2 = new HereClusterMap({
    id: "clustermap2",
    managerid: "search1",
    el: $("#search-map-2"),
    height: "400px",
    zoom: "4",
    center: "60,-160",
    theme: theme2
}).render()
</pre></code>



#### Shape map

For using a cluster map you need to load the "app/heremaps/heremaps/hereshapemap" dependency.  
And then you can create a new shape map:

<pre><code>
var myshapemap = new HereShapeMap({
  id: "shapemap1",
  managerid: "search1",
  el: $("#search-map"),
  height: "400px",
}).render()
</pre></code>

By default a map of the world will be loaded. But you can change that like this:

<pre><code>
var myshapemap = new HereShapeMap({
  id: "shapemap1",
  managerid: "search1",
  el: $("#search-map"),
  height: "400px",
  zoom: "5",
  center: "51,5",
  kmlFile: "de.kml"
}).render()
</pre></code>

You can add your own kml files to the heremaps app in appserver/static/data.  
But they have to follow a certain XML structure. See the custom.kml file.

It's also possible to change the info bubble that pops up for a shape map.  
The function is called with 2 arguments:
   * placemark: an object containing the value and kml nodes
   * data: the event

<pre><code>
var myshapemap = new HereShapeMap({
  id: "shapemap1",
  managerid: "search1",
  el: $("#search-map"),
  height: "400px",
  zoom: "2",
  kmlFile: "custom.kml",
  bubbleContentProvider: function(placemark,data){return "<div style='text-align:center; transform: rotate(7deg);'>"+placemark["name"]+": "+data["result"]["something"]+"</div>";},
}).render()
</pre></code>

If needed you can also change the color range, the example below will change the color range to 6 shades of grey:
<pre><code>
var myshapemap = new HereShapeMap({
  id: "shapemap1",
  managerid: "search1",
  el: $("#search-map"),
  height: "400px",
  colorRange:{"0.0":"rgba(0,0,0,1)","0.2":"rgba(0,0,0,0.8)","0.4":"rgba(0,0,0,0.6)","0.6":"rgba(0,0,0,0.4)","0.7":"rgba(0,0,0,0.3)","0.8":"rgba(0,0,0,0.2)"},
}).render()
</pre></code>

#### Heat map

Creating a heat map is slightly different than the other maps as it still using an older version of the HERE javascript API.  
Therefore you don't need to include all the javascript that was mentioned above.  
But only this:

<pre><code>
<script src="https://js.api.here.com/se/2.5.4/jsl.js?with=all" type="text/javascript" charset="utf-8"></script>
<style>
  .mapcontainer img{
    max-width:none;
  }
</style>
</pre></code>

<pre><code>
var myheatmap = new HereHeatMap({
  id: "heatmap1",
  managerid: "search1",
  el: $("#search-map"),
  height: "400px",
}).render()
</pre></code>

By default a heat map will 'heat' based on the density of your lat/lng combinations.  
But it's also possible to have the map 'heat' based on the value of your lat/lng combinations.  
See the example below that sets type="density" and also sets a different color scheme.

<pre><code>
var myheatmap1 = new HereHeatMap({
  id: "heatmap1",
  managerid: "search1",
  el: $("#search-map1"),
  height: "400px",
  type:"density",
  opacity: "0.95",
  colors: {
      stops: {
          "0": "rgba(0,0,0,0.2)",
          "0.25": "rgba(0,0,0,0.4)",
          "0.5": "rgba(0,0,0,1)",
          "0.75": "rgba(0,0,0,1)",
          "1": "rgba(0,0,0,1)"
      },
      interpolate: true
  }
}).render()
</pre></code>

# Versions
   * 0.1: First version, includes marker map, cluster map and shape map.
   * 0.2: Add more shapemaps. Add heatmaps, fix bug with reverse geocoding command. Make markers clickable.

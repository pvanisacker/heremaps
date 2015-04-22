# Customization using HTML dashboards

## Common config

You need to create one directory in your app to save your html dashboards: default/data/ui/html.  
When done your directory structure should look like this:

<pre><code>
- $SPLUNK_HOME/etc/apps/myspecialapp
  - default
    - data
      - ui
        - nav
        - html
    - app.conf
  - ...
</code></pre>


When creating an HTML dashboard try to use one of the dashboards provided in the app as a base dashboard.  
If that's not possible make sure your html includes the following:
 * correct HTML header including all the require splunk javascript & css resources
 * a body that contains the components to be displayed
 * a piece of JavaScript that initializes all of the components
 
The piece of JavaScript should look like this:
```html
    <script src="{{SPLUNKWEB_URL_PREFIX}}/static/app/heremaps/heremaps/config.js" type="text/javascript"></script>
    <script type="text/javascript">
        require.config({
            baseUrl: "{{SPLUNKWEB_URL_PREFIX}}/static/js",
        });
        
        // here's the rest of the javascript
    </script>
```

Once that's done you can start configuring the visualization.


## Marker map

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
More information about creating a marker can be found on https://developer.here.com/javascript-apis/documentation/v3/maps/topics/markers.html
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


## Cluster map

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
See the example below and look at https://developer.here.com/javascript-apis/documentation/v3/maps/topics/clustering.html

```html
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
```



## Shape map

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

## Heat map

Creating a heat map is similar to the other maps.

Make sure to include the necessary javascript in your dashboard.
And create the heatmap like this:

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
  colors: colors: new H.data.heatmap.Colors(
      {
          "0": "rgba(0,0,0,0.2)",
          "0.25": "rgba(0,0,0,0.4)",
          "0.5": "rgba(0,0,0,1)",
          "0.75": "rgba(0,0,0,1)",
          "1": "rgba(0,0,0,1)"
      },
      true
      )
}).render()
</pre></code>

## Line map

Documentation is not ready yet.
[![Build Status](https://travis-ci.org/pvanisacker/heremaps.svg?branch=master)](https://travis-ci.org/pvanisacker/heremaps)
[![Build Status](https://snap-ci.com/pvanisacker/heremaps/branch/master/build_image)](https://snap-ci.com/pvanisacker/heremaps/branch/master)

# Intro

A Splunk app for map visualizations using HERE maps  
It includes 4 different visualizations types and two reverse geocoding custom commands and a couple of csv lookups containing example data.  
See some screenshots: https://github.com/pvanisacker/heremaps/blob/master/appserver/static

The code is available on github: https://github.com/pvanisacker/heremaps  
For questions about the app, please raise them on https://answers.splunk.com  
When you spot bugs please file an issue on https://github.com/pvanisacker/heremaps/issues

Note this app is not at all supported by HERE.  
And the app is an early state of development so there will be tons of bugs.

Enjoy!

# License

The app itself is distributed under the Creative Commons license.  
Example data is taken from wikipedia wich also uses a Creative Commons license: https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License  
And the KML files for shape maps were created from data of http://www.naturalearthdata.com/.
The app uses HERE api's, for information see: https://developer.here.com

# Installation & Setup

For installing the app, just follow the standard splunk app procedures.  
Once it is installed, you also have to get free api credentials for using the HERE api.  
Request them on https://developer.here.com.  
Once you have them either use setup screen to configure the app_id and app_code.

Or by configuring it manually in the local/setup.conf:
<pre><code>[heremaps]
app_id=my_app_id
app_code=my_app_code
</code></pre>

Without these settings the app will not work.

The reversegeocodeshape command requires further installation effort see [INSTALL.md](INSTALL.md)

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

## reversegeocodeshape command

The reversegeocodeshape command is to be used together with a shape map visualization.  
What the command does is translating the lat/lng combination into key's used for the shape map.  
You can think of it as a splunk internal reverse geocoder as the command does not use any external web services.  
Although it does not require external web services it does require some additional installation effort. See the installation part of the readme for help.  
And because it runs locally it can be rather slow and require lots of CPU power.  

By default the command will translate the lat/lng into a 2 letter ISO3166 key from the world2.geojson file.
<pre><code>index=_internal | head 1 | eval lat=51 | eval lng=6 | reversegeocodeshape | fields lat,lng,key | table lat,lng,key</code></pre>
| lat      | lng       | key |
|----------|-----------|-----|
| 51       | 6         | DE  |

The map that is used can be customized by providing some additional arguments.
<pre><code>index=_internal | head 1 | eval lat=48.853 | eval lng=2.35 | reversegeocodeshape filetype=geojson filename=countries/fr.geojson | table lat,lng,key</code></pre>
| lat      | lng       | key |
|----------|-----------|-----|
| 48.853   | 2.35      | Paris |

And you can also cusomize the input and output fields.
<pre><code>index=_internal | head 1 | eval latitude=48.853 | eval longitude=2.35 | reversegeocodeshape lat=latitude lng=longitude filetype=geojson filename=countries/fr.geojson fieldname=mycustomkey| table latitude,longitude,mycustomkey</code></pre>
| latitude      | longitude       | mycustomkey |
|----------|-----------|-----|
| 48.853   | 2.35      | Paris |

## Visualizations

The app contains 4 different map visualizations.
   * Marker map: displaying markers for lat/lng combinations
   * Cluster map: clusters markers together to get a better overview.
   * Shape map: colors shapes depending on the values
     These maps use a KML or geoJSON files to highlight certain areas. The KML and geoJSON files need a specific structure. See the custom.kml or custom.geojson file for an example.
   * Heat map: shows density or value heatmaps of your data.
   * Line map: shows coords connected by lines
   
Except for the heat map, all of the visualization use v3 of the HERE javascript API.  
The heatmap visualization still uses v2.5.

The app contains examples on how to include the visualizations in HTML dashboards. If you are using the Splunk web framework you should also be able to include the visualizations as well, although I did not test it.

The visualization can render quite some data points/markers. But as these visualizations are rendered on browser side there are limits.  
To avoid your brower from becoming slow when rendering data, try to aggregate as much data as possible already on server side.  
If you have a search that returns tons of data, you could use the following:
```
... | eval lat=round(lat,4) | eval lng=round(lng,4) | stats count as value by lat,lng 
```

### Marker map

For using a marker map your search needs to return events that contain a "lat" and a "lng" field in a floating point form.  
Optionally the event can also contain a "value" field that is used for displaying in the bubble when a marker is clicked.

### Cluster map

A cluster map requires the same search data as a marker map.

### Shape map

For rendering a shape map your search needs to return events that contain a "key" and "value" field.
If you are using KML files the key needs to match with the description of the KML placemark.
If you are using geoJSON file the key needs to match the id of the properties of the geoJSON Feature.  
Out of the box the app provides a couple of KML and geoJSON files:
   * world2.kml or world2.geojson: key is the ISO3166 2 letter code code
   * world3.kml or world3.geojson: key is the ISO3166 3 letter country code
   * fr.kml: key is the name of the department
   * ...

### Heat map

A heat map requires the same search data as a marker map.

### Line map

A line map requires a very specific set of data.  
The search should return events that contain a "coords", "points" and "values" field.  
All these fields should be multi-value fields.  
 - coords: list of coordinates that define the line
 - points: list of values for the coordinates
 - values: list of values for the lines connecting the coordinates

# Customization

See [CUSTOM.md](CUSTOM.md)

# Versions
   * 0.1: First version, includes marker map, cluster map and shape map.
   * 0.2: Add more shapemaps. Add heatmaps, fix bug with reverse geocoding command. Make markers clickable.
   * 0.3: Fix loading of shapemaps, add more documentation, add example HTML dashboards.
   * 0.4: Remove django parts as they were too complicated, add more shape maps, add reversegeocodeshape command, add testcases for custom commands
   * 0.5: Add simple line maps
   * 0.6: Added line map arrows, added more line map examples, added cluster map example
   
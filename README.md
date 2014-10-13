# heremaps


## Intro


A Splunk app for map visualizations using HERE maps  
It includes 3 different visualizations types, one reverse geocoding custom command and a couple of csv lookups.

See a couple of screenshots in:

For questions about the app, please raise them on http://answers.splunk.com

When you spot bugs please file an issue on https://github.com/pvanisacker/heremaps/issues

Note this app is not at all supported by HERE.  
And the app is an early state of development so there will be tons of bugs.

Enjoy!

## Components


### Visualizations

The app contains 3 different map visualizations.
   * Marker map: displaying markers for lat/lng combinations
   * Cluster map: clusters markers
   * Shape map: colors shapes depending on the values
See the examples on how to use them and customize them.

### Reverse geocoding command

This command uses the HERE REST api. So you need internet connectivity to get it working.  
It requires a lat and lng field and will add new fields containing the information for this lat/lng.  
The fields that will be added:
  * regeo_country
  * regeo_state
  * regeo_region
  * regeo_county
  * regeo_district
  * regeo_postalcode
  * regeo_city
  * regeo_label

You'll notice that not all of these fields are returned.  
The country value is an ISO3166 2 letter code.  
Using the 'countries' lookup you can get a country name.  
See:
<pre><code>... | reversegeocode | lookup countries country_iso3166_3 as regeo_country</code></pre>
Or use the `reversegeocode` macro.

The command includes a small cache to avoid calling the HERE api too often.  
By default it stores 1000000 results for 62 days.

## Install

For installing the app, just follow the standard splunk app procedures.

Once it is installed, you also have to get api credentials for using the HERE api.

Request them on http://developer.here.com.

Once you have them either use setup screen to configure the app_id and app_code.

Or by configuring it manually in the local/setup.conf:
<pre><code>[heremaps]
app_id=my_app_id
app_code=my_app_code
</code></pre>

Without these settings lots of the functionality of the app will not work.


## Versions
   * 0.1: First version, includes marker map, cluster map and shape map

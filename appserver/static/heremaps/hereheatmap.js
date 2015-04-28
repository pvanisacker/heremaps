define([
    "app/heremaps/heremaps/heremap",
    "heremapsjsData"
    ],
    function(HereMap) {

    /**
     * A module exposing a heat map
     * @exports heremaps/HereHeatMap
     * @extends module:heremaps/HereMap
     */
    var HereHeatMap = HereMap.extend({
        className: "hereheatmap",

        /**
         * Sets the options for the heat map
         * @property {object} options.colors       - The colors to be used for the heat map
         *                                           See: {@link https://developer.here.com/javascript-apis/documentation/v3/maps/topics_api_nlp/h-data-heatmap-colors.html}
         * @property {integer} options.opacity     - The opacity used for the heatmap overlay
         * @property {string} options.type         - The type of heatmap: "density" or "value".
         *                                           See: {@link https://developer.here.com/javascript-apis/documentation/v3/maps/topics_api_nlp/h-data-heatmap-provider-options.html#h-data-heatmap-provider-options__type}
         * @property {integer} options.coarseness  - The coarseness of the heatmap.
         *                                           See: {@link https://developer.here.com/javascript-apis/documentation/v3/maps/topics_api_nlp/h-data-heatmap-provider-options.html#h-data-heatmap-provider-options__coarseness}
         * @property {integer} options.sampleDepth - An integer in range [1..8] indicating the sample depth. The higher the value the more detailed the maps but that also costs a bit performance.
         *                                           See: {@link https://developer.here.com/javascript-apis/documentation/v3/maps/topics_api_nlp/h-data-heatmap-provider-options.html#h-data-heatmap-provider-options__sampledepth}
         */
        options: {
            colors: undefined,
            opacity: 1,
            type: "density",
            coarseness: 2,
            sampleDepth: 4
        },

        /** This function will read through the result data and update the map
         * @private
         */
        updateView: function(viz, data){
            this.clearView();
            heat_data=[];
            for(var res in data){
                if("lat" in data[res] && "lng" in data[res]){
                    var lat=parseFloat(data[res].lat);
                    var lng=parseFloat(data[res].lng);
                    var value=parseFloat(data[res].value);
                    heat_data.push({"lat":lat,"lng":lng,"value":value});
                }
            }
            this.heatmapProvider=this.getHeatMapProvider();
            this.heatmapProvider.addData(heat_data);
            this.heatmapLayer = new H.map.layer.TileLayer(this.heatmapProvider);
            this.map.addLayer(this.heatmapLayer);
            this._clearMessage();
        },

        /** This function clears up the heatmap overlay from the map
         * @private
         */
        clearView: function(){
            this.map.removeLayer(this.heatmapLayer);
        },

        /** This function creates the heatmap provider
         * @private
         */
        getHeatMapProvider: function(){
            // Creating Heatmap overlay
            var options={
                max:20,
                opacity: this.options.opacity,
                type: this.options.type,
                coarseness: this.options.coarseness,
                sampleDepth: this.options.sampleDepth
            };
            if(this.options.colors){
                options.colors=this.options.colors;
            }

            var heatmapProvider = new H.data.heatmap.Provider(options);
            return heatmapProvider;
        }
    });
    return HereHeatMap;
});
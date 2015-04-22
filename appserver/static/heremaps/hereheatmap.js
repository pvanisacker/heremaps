define([
    "app/heremaps/heremaps/heremap",
    "heremapsjsData"
    ],
    function(HereMap) {

    // Define the custom view class
    var HereHeatMap = HereMap.extend({
        className: "hereheatmap",

        options: {
            colors: undefined,
            opacity: 1,
            type: "density",
            coarseness: "2"
        },

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

        clearView: function(){
            this.map.removeLayer(this.heatmapLayer);
        },

        getHeatMapProvider: function(){
            // Creating Heatmap overlay
            var options={
                max:20,
                opacity: this.options.opacity,
                type: this.options.type,
                coarseness: this.options.coarseness
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
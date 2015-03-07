define(function(require, exports, module) {
    // Load requirements
    var _ = require('underscore');
    var mvc = require('splunkjs/mvc');
    var HereMap = require('app/heremaps/heremaps/heremap');
    var Messages = require("splunkjs/mvc/messages");
    var utils = require('splunkjs/mvc/utils');
    
    // Define the custom view class
    var HereClusterMap = HereMap.extend({
        className: "hereclustermap",

        options: {
            min_weight: 1,
            eps: 32,
            theme: undefined
        },

        clusteringLayer:undefined,

        updateView: function(viz, data) {
            if(this.map){
                this.clearView();

                var dataPoints = [];
                for(var i=0;i<data.length;i++){
                    dataPoints.push(new H.clustering.DataPoint(data[i].lat,data[i].lng,1,data[i]));
                }

                var options={clusteringOptions: {
                        minWeight: this.options.min_weight,
                        eps: this.options.eps
                    }};
                if(this.options.theme){
                    options.theme=this.options.theme;
                }
                this.clusteringProvider = new H.clustering.Provider(dataPoints, options);
                this.clusteringLayer = new H.map.layer.ObjectLayer(this.clusteringProvider);
                this.map.addLayer(this.clusteringLayer);
            }
            this._clearMessage();
        },
        clearView: function(){
            if(this.map && this.clusteringLayer){
                this.map.removeLayer(this.clusteringLayer);
            }
        }
    });

    return HereClusterMap;
});
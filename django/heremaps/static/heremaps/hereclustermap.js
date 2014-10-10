define(function(require, exports, module) {
    // Load requirements
    var _ = require('underscore');
    var mvc = require('splunkjs/mvc');
    var HereMap = require('heremaps/heremap');
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

                var noiseSvg = '<svg xmlns="http://www.w3.org/2000/svg" height="20px" width="20px"><circle cx="5px" cy="5px" r="5px" fill="green" /></svg>';
                var noiseIcon = new H.map.Icon(noiseSvg, {size: { w: 20, h: 20 }, anchor: { x: 10, y: 10}});

                // Create an SVG template for the cluster icon:
                var clusterSvgTemplate =  '<svg xmlns="http://www.w3.org/2000/svg" height="50px" width="50px"><circle cx="25px" cy="25px" r="{radius}" fill="red" /></svg>';

                var dataPoints = [];
                for(var i=0;i<data.length;i++){
                    dataPoints.push(new H.clustering.DataPoint(data[i]["lat"],data[i]["lng"],1,data[i]));
                }

                var options={clusteringOptions: {
                        minWeight: this.min_weight,
                        eps: this.eps
                    }}
                if(this.options.theme){
                    options["theme"]=this.options.theme
                }
                var clusteringProvider = new H.clustering.Provider(dataPoints, options);

                //clustering should be used with ObjectLayer
                this.clusteringLayer = new H.map.layer.ObjectLayer(clusteringProvider);
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
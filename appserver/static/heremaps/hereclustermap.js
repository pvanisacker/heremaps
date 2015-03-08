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
            theme: undefined,
            bubbleContentProvider: function(data){
                var text;
                if(data instanceof H.clustering.NoisePoint){
                    text=data.getData().value.encodeHTML();
                }else if(data instanceof H.clustering.Cluster){
                    var count=0;
                    data.forEachDataPoint(function(dataPoint){
                        count+=1;
                    });
                    text=count
                }
                return "<div style='text-align:center'>"+text+"</div>";
            }
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
                    },
                    theme:{}
                };

                if(this.options.theme){
                    options.theme=this.options.theme;
                }else{
                    options.theme=new H.clustering.DefaultTheme();
                }

                this.clusteringProvider = new H.clustering.Provider(dataPoints, options);
                this.clusteringLayer = new H.map.layer.ObjectLayer(this.clusteringProvider);

                var that=this;
                if(this.options.bubbleContentProvider){
                    this.clusteringProvider.addEventListener('tap', function (evt) {
                        var bubble =  new H.ui.InfoBubble(evt.target.getPosition(), {
                            content: that.options.bubbleContentProvider(evt.target.getData())
                        });
                        that.ui.addBubble(bubble);
                    }, false);
                }


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
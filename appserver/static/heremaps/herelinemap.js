define(function(require, exports, module) {
    // Load requirements
    var _ = require('underscore');
    var mvc = require('splunkjs/mvc');
    var HereMap = require('app/heremaps/heremaps/heremap');
    var Messages = require("splunkjs/mvc/messages");
    var utils = require('splunkjs/mvc/utils');
    
    // Define the custom view class
    var HereMarkerMap = HereMap.extend({
        className: "heremarkermap",

        options: {
            marker:undefined,
            bubbleContentProvider: function(data){return "<div style='text-align:center;'>"+data["value"]+"</div>";}
        },
        group:new H.map.Group(),

        postCreateMap: function(){

        },

        getVisualization: function(event){
            var group = new H.map.Group();
            var strip = new H.geo.Strip();
            if( "coords" in event){
                for(var i=0;i<event["coords"].length;i++){
                    var coord=event["coords"][i].split(",")
                    var coord={lat: parseFloat(coord[0]), lng: parseFloat(coord[1])}
                    strip.pushPoint(coord)
                    if(this.options.marker){
                        var data=undefined
                        if(event["points"].isArray && event["points"][i]!=undefined){
                            data=event["points"][i]
                        }
                        var marker=this.options.marker(coord,data);
                        group.addObject(marker)
                    }
                }
            }
            var polyline = new H.map.Polyline(strip, { style: { lineWidth: 10 }});


            group.addObject(polyline)

            return group;
        },

        updateView: function(viz, data) {
            if(this.map){
                this.clearView();
                for(var i=0;i<data.length;i++){
                    var objects=this.getVisualization(data[i])
                    this.group.addObject(objects);
                }
                this.map.addObject(this.group);
            }
            this._clearMessage();
        },

        clearView: function(){
            if(this.map && this.group){
                this.group.removeAll();
            }
        }
    });

    return HereMarkerMap;
});
define(function(require, exports, module) {
    // Load requirements
    var _ = require('underscore');
    var mvc = require('splunkjs/mvc');
    var HereMap = require('app/heremaps/heremaps/heremap');
    var Messages = require("splunkjs/mvc/messages");
    var utils = require('splunkjs/mvc/utils');
    
    // Define the custom view class
    var HereLineMap = HereMap.extend({
        className: "herelinemap",

        options: {
            marker:undefined,
            bubbleContentProvider: function(data){return "<div style='text-align:center;'>"+data+"</div>";}
        },
        group:new H.map.Group(),

        postCreateMap: function(){

        },

        getVisualization: function(event){
            var group = new H.map.Group();
            var markergroup = new H.map.Group();
            var strip = new H.geo.Strip();

            if( "coords" in event){
                for(var i=0;i<event["coords"].length;i++){
                    var coord=event["coords"][i].split(",")
                    var coord={lat: parseFloat(coord[0]), lng: parseFloat(coord[1])}
                    strip.pushPoint(coord)
                    if(this.options.marker){
                        var data=undefined
                        if(Object.prototype.toString.call( event["points"] ) === '[object Array]'){
                            if(event["points"][i]!=undefined){
                                data=event["points"][i]
                            }
                        } else{
                            data=event["points"]
                        }
                        var marker=this.options.marker(coord,data);
                        marker.setData(data);
                        markergroup.addObject(marker)
                    }
                }
            }

            var that=this;
            markergroup.addEventListener('tap', function (evt) {
                var bubble =  new H.ui.InfoBubble(evt.target.getPosition(), {
                    content: that.options.bubbleContentProvider(evt.target.getData())
                });
                that.ui.addBubble(bubble);
            }, false);

            group.addObject(markergroup);
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

    return HereLineMap;
});
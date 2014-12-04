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
            linemarker:undefined,
            pointmarker:undefined,
            lineBubbleContentProvider: function(data){return "<div style='text-align:center;'>"+data+"</div>";},
            pointBubbleContentProvider: function(data){return "<div style='text-align:center;'>"+data+"</div>";},
            lineStyleProvider: function(coord1,coord2,data){return {lineWidth:5}}
        },
        group:new H.map.Group(),

        postCreateMap: function(){

        },

        getVisualization: function(event){
            var group = new H.map.Group();
            var pointmarkergroup = new H.map.Group();
            var linemarkergroup = new H.map.Group();
            var linegroup = new H.map.Group();

            if( "coords" in event){
                for(var i=0;i<event["coords"].length;i++){
                    var coord=event["coords"][i].split(",")
                    var coord={lat: parseFloat(coord[0]), lng: parseFloat(coord[1])}

                    var nextcoord=undefined
                    var linedata=undefined
                    try{
                        // get the next coord
                        nextcoord=event["coords"][i+1].split(",")
                        nextcoord={lat:parseFloat(nextcoord[0]), lng:parseFloat(nextcoord[1])}

                        // get the data for that line
                        if(Object.prototype.toString.call(event["values"]) === "[object Array]"){
                            if(event["values"][i]!=undefined){
                                linedata=event["values"][i]
                            }
                        }else{
                            linedata=event["values"]
                        }

                        // create a new line
                        var strip=new H.geo.Strip()
                        strip.pushPoint(coord)
                        strip.pushPoint(nextcoord)
                        var line=new H.map.Polyline(strip,this.options.lineStyleProvider(coord,nextcoord,linedata));
                        linegroup.addObject(line)
                    }catch(err){
                        console.log(err);
                        console.log(err.stack);
                    }

                    // Create the marker for a point
                    if(this.options.pointmarker){
                        var data=undefined
                        if(Object.prototype.toString.call( event["points"] ) === '[object Array]'){
                            if(event["points"][i]!=undefined){
                                data=event["points"][i]
                            }
                        } else{
                            data=event["points"]
                        }
                        var marker=this.options.pointmarker(coord,data);
                        marker.setData(data);
                        pointmarkergroup.addObject(marker)
                    }

                    // Create the marker for a line
                    if(this.options.linemarker && nextcoord!=undefined){
                        var marker=this.options.linemarker(coord,nextcoord,linedata)
                        marker.setData(linedata);
                        linemarkergroup.addObject(marker)
                    }
                }
            }

            var that=this;
            if(this.options.pointBubbleContentProvider){
                pointmarkergroup.addEventListener('tap', function (evt) {
                    var bubble =  new H.ui.InfoBubble(evt.target.getPosition(), {
                        content: that.options.pointBubbleContentProvider(evt.target.getData())
                    });
                    that.ui.addBubble(bubble);
                }, false);
            }
            if(this.options.lineBubbleContentProvider){
                linemarkergroup.addEventListener('tap', function (evt) {
                    var bubble =  new H.ui.InfoBubble(evt.target.getPosition(), {
                        content: that.options.lineBubbleContentProvider(evt.target.getData())
                    });
                    that.ui.addBubble(bubble);
                }, false);
            }

            group.addObject(pointmarkergroup);
            group.addObject(linemarkergroup);
            group.addObject(linegroup);
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
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
            pointmarker:function(coord,event,index,data){
                var color="#555555"
                var colorRange={
                    "0"   :"rgb(0,255,64)",
                    "10"   :"rgb(0,255,0)",
                    "20"   :"rgb(64,255,0)",
                    "30"   :"rgb(128,255,0)",
                    "40"   :"rgb(192,255,0)",
                    "50"   :"rgb(255,255,0)",
                    "60"   :"rgb(255,192,0)",
                    "70"   :"rgb(255,128,0)",
                    "80"   :"rgb(255,64,0)",
                    "90"   :"rgb(255,0,0)"
                }
                var size=8
                var halfsize=size/2;
                var svg='<svg width="${SIZE}" height="${SIZE}" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg"><circle opacity="0.9" id="svg_1" r="${HALFSIZE}" cy="${HALFSIZE}" cx="${HALFSIZE}" stroke-width="0" stroke="#000000" fill="${COLOR}"/></svg>';

                for(var colorTreshold in colorRange){
                    if(data>=parseFloat(colorTreshold)){
                        color=colorRange[colorTreshold]
                    }
                }

                svg=svg.replace(/\$\{COLOR\}/g,color)
                svg=svg.replace(/\$\{SIZE\}/g,size)
                svg=svg.replace(/\$\{HALFSIZE\}/g,halfsize)

                var markerIcon = new H.map.Icon(svg,{anchor:{x:halfsize,y:halfsize}});
                return new H.map.Marker(coord,{icon: markerIcon});
            },
            linemarker:function(coord1,coord2,event,index,data){
                var color="#555555"
                var colorRange={
                    "0"   :"rgb(0,255,64)",
                    "10"   :"rgb(0,255,0)",
                    "20"   :"rgb(64,255,0)",
                    "30"   :"rgb(128,255,0)",
                    "40"   :"rgb(192,255,0)",
                    "50"   :"rgb(255,255,0)",
                    "60"   :"rgb(255,192,0)",
                    "70"   :"rgb(255,128,0)",
                    "80"   :"rgb(255,64,0)",
                    "90"   :"rgb(255,0,0)"
                }
                var size=25
                var halfsize=size/2;
                var svg='<svg width="${SIZE}" height="${SIZE}" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg"><text xml:space="preserve" text-anchor="middle" id="svg_2" y="${HALFSIZE}" x="${HALFSIZE}" font-size="7pt" font-family="Roboto" stroke="${COLOR}" fill="${COLOR}">${TEXT}</text></svg>';

                for(var colorTreshold in colorRange){
                    if(data>=parseFloat(colorTreshold)){
                        color=colorRange[colorTreshold]
                    }
                }

                svg=svg.replace(/\$\{COLOR\}/g,color)
                svg=svg.replace(/\$\{SIZE\}/g,size)
                svg=svg.replace(/\$\{HALFSIZE\}/g,halfsize)
                svg=svg.replace(/\$\{TEXT\}/g,data)

                var markerIcon = new H.map.Icon(svg,{anchor:{x:halfsize,y:halfsize}});
                centercoord={lat:(coord1.lat+coord2.lat)/2 , lng:(coord1.lng+coord2.lng)/2}
                return new H.map.Marker(centercoord,{icon: markerIcon});
            },
            lineBubbleContentProvider: function(data){return "<div style='text-align:center;'>"+data["data"]+"</div>";},
            pointBubbleContentProvider: function(data){return "<div style='text-align:center;'>"+data["data"]+"</div>";},
            lineStyleProvider: function(coord1,coord2,event,index,data){
                var color="#555555"
                var colorRange={
                    "0"   :"rgb(0,255,64)",
                    "10"   :"rgb(0,255,0)",
                    "20"   :"rgb(64,255,0)",
                    "30"   :"rgb(128,255,0)",
                    "40"   :"rgb(192,255,0)",
                    "50"   :"rgb(255,255,0)",
                    "60"   :"rgb(255,192,0)",
                    "70"   :"rgb(255,128,0)",
                    "80"   :"rgb(255,64,0)",
                    "90"   :"rgb(255,0,0)"
                }
                for(var colorTreshold in colorRange){
                    if(data>=parseFloat(colorTreshold)){
                        color=colorRange[colorTreshold]
                    }
                }

                return {lineWidth:5,strokeColor:color,fillColor:color}
            }
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
                        var line=new H.map.Polyline(strip);
                        line.setStyle(this.options.lineStyleProvider(coord,nextcoord,event,i,linedata));
                        linegroup.addObject(line)
                    }catch(err){

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

                        var marker=this.options.pointmarker(coord,event,i,data);
                        if(marker){
                            marker.setData({event:event,index:i,data:data});
                            pointmarkergroup.addObject(marker)
                        }
                    }

                    // Create the marker for a line
                    if(this.options.linemarker && nextcoord!=undefined){
                        var marker=this.options.linemarker(coord,nextcoord,event,i,linedata)
                        if(marker){
                            marker.setData({event:event,index:i,data:linedata});
                            linemarkergroup.addObject(marker)
                        }
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
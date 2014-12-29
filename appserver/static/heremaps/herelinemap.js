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
        shapes:[],
        maxLineValue:-Number.MAX_VALUE,
        minLineValue:Number.MAX_VALUE,
        maxPointValue:-Number.MAX_VALUE,
        minPointValue:Number.MAX_VALUE,
        options: {
            pointMarkerSvg:'<svg width="${SIZE}" height="${SIZE}" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg"><circle opacity="0.9" id="svg_1" r="${HALFSIZE}" cy="${HALFSIZE}" cx="${HALFSIZE}" stroke-width="0" stroke="#000000" fill="${COLOR}"/></svg>',
            pointMarkerDefaultColor:"#333333",
            pointMarkerColorRange:{
                "0.0"   :"rgb(0,255,64)",
                "0.1"   :"rgb(0,255,0)",
                "0.2"   :"rgb(64,255,0)",
                "0.3"   :"rgb(128,255,0)",
                "0.4"   :"rgb(192,255,0)",
                "0.5"   :"rgb(255,255,0)",
                "0.6"   :"rgb(255,192,0)",
                "0.7"   :"rgb(255,128,0)",
                "0.8"   :"rgb(255,64,0)",
                "0.9"   :"rgb(255,0,0)"
            },
            pointMarker:undefined,
            lineMarkerSvg:'<svg width="${SIZE}" height="${SIZE}" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg"><text xml:space="preserve" text-anchor="middle" id="svg_2" y="${HALFSIZE}" x="${HALFSIZE}" font-size="7pt" font-family="Roboto" stroke="#000000" stroke-width="1" fill="${COLOR}">${TEXT}</text></svg>',
            lineMarkerDefaultColor:"#333333",
            lineMarkerColorRange:{
                "0.0"   :"rgb(0,255,64)",
                "0.1"   :"rgb(0,255,0)",
                "0.2"   :"rgb(64,255,0)",
                "0.3"   :"rgb(128,255,0)",
                "0.4"   :"rgb(192,255,0)",
                "0.5"   :"rgb(255,255,0)",
                "0.6"   :"rgb(255,192,0)",
                "0.7"   :"rgb(255,128,0)",
                "0.8"   :"rgb(255,64,0)",
                "0.9"   :"rgb(255,0,0)"
            },
            lineMarker:undefined,
            lineStyleDefaultColor:"#333333",
            lineStyleColorRange:{
                "0.0"   :"rgb(0,255,64)",
                "0.1"   :"rgb(0,255,0)",
                "0.2"   :"rgb(64,255,0)",
                "0.3"   :"rgb(128,255,0)",
                "0.4"   :"rgb(192,255,0)",
                "0.5"   :"rgb(255,255,0)",
                "0.6"   :"rgb(255,192,0)",
                "0.7"   :"rgb(255,128,0)",
                "0.8"   :"rgb(255,64,0)",
                "0.9"   :"rgb(255,0,0)"
            },
            lineStyle:undefined,
            lineMarkerBubbleContentProvider: function(data){return "<div style='text-align:center;'>"+data.data+"</div>";},
            lineBubbleContentProvider: function(data){return "<div style='text-align:center;'>"+data.data+"</div>";},
            pointMarkerBubbleContentProvider: function(data){return "<div style='text-align:center;'>"+data.data+"</div>";},
            lineStyleProvider: function(coord1,coord2,event,index,data){
                var color="#555555";
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
                };
                for(var colorTreshold in colorRange){
                    if(data>=Number(colorTreshold)){
                        color=colorRange[colorTreshold];
                    }
                }

                return {lineWidth:5,strokeColor:color,fillColor:color};
            }
        },
        group:new H.map.Group(),

        /*
            Once this map starts loading results the following happens.
            - parse the events into the data structure below. Without creating the map objects
            - read through the data structure below and create all the map objects and set the objects data.

            This two phased approach allows on the fly changes of visualizations, which is needed for the default highlighting.

            This datastructure will contain all the event data an shapes that are placed on a map.
            For each event the following will be stored
            {
                coords:[{
                    raw:"raw coord value",
                    parsed:{lat:"lat",lng:"lng"},
                }],
                points:[{
                    raw:"raw point value",
                    parsed:"float value",
                    marker:"the marker object"
                }],
                values:[{
                    raw:"raw value value",
                    parsed:"float value",
                    marker:"the marker object",
                    line:"the polyline object"
                }],
                event:"raw event"
            }
            And this will all be stored in this.events array.
        */

        defaultPointMarker: function(coord,event,index,data){
            var size=8;
            var halfsize=size/2;
            var color=this.options.pointMarkerDefaultColor;

            try{
                var percent = (Number(data) - this.minPointValue) / (this.maxPointValue - this.minPointValue);
                for(var item in this.options.pointMarkerColorRange){
                    if(percent>=Number(item)){
                        color=this.options.pointMarkerColorRange[item];
                    }
                }
            }catch(err){
                console.error(err);
            }

            svg=this.options.pointMarkerSvg.replace(/\$\{COLOR\}/g,color);
            svg=svg.replace(/\$\{SIZE\}/g,size);
            svg=svg.replace(/\$\{HALFSIZE\}/g,halfsize);
            svg=svg.replace(/\$\{TEXT\}/g,data);

            var markerIcon = new H.map.Icon(svg,{anchor:{x:halfsize,y:halfsize}});
            return new H.map.Marker(coord,{icon: markerIcon});
        },

        defaultLineMarker: function(coord1,coord2,event,index,data){
            var size=40;
            var halfsize=size/2;
            var color=this.options.lineMarkerDefaultColor;

            try{
                var percent = (Number(data) - this.minLineValue) / (this.maxLineValue - this.minLineValue);
                for(var item in this.options.lineMarkerColorRange){
                    if(percent>=Number(item)){
                        color=this.options.lineMarkerColorRange[item];
                    }
                }
            }catch(err){
                console.error(err);
            }

            svg=this.options.lineMarkerSvg.replace(/\$\{COLOR\}/g,color);
            svg=svg.replace(/\$\{SIZE\}/g,size);
            svg=svg.replace(/\$\{HALFSIZE\}/g,halfsize);
            svg=svg.replace(/\$\{TEXT\}/g,data);

            var markerIcon = new H.map.Icon(svg,{anchor:{x:halfsize,y:halfsize}});
            centercoord={lat:(coord1.lat+coord2.lat)/2 , lng:(coord1.lng+coord2.lng)/2};
            return new H.map.Marker(centercoord,{icon: markerIcon});
        },

        defaultLineStyle: function(coord1,coord2,event,index,data){
            var color=this.options.lineStyleDefaultColor;
            try{
                var percent = (Number(data) - this.minLineValue) / (this.maxLineValue - this.minLineValue);
                for(var item in this.options.lineStyleColorRange){
                    if(percent>=Number(item)){
                        color=this.options.lineStyleColorRange[item];
                    }
                }
            }catch(err){
                console.error(err);
            }

            return {lineWidth:5,strokeColor:color,fillColor:color};
        },
        getLineStyle: function(coord,nextcoord,parsed,index,value){
            var style;
            if(this.options.linestyle!==undefined){
                style=this.options.linestyle(coord,nextcoord,parsed.event,index,value);
            }else{
                style=this.defaultLineStyle(coord,nextcoord,parsed.event,index,value);
            }
            return style;
        },
        createLine: function(coord,nextcoord,parsed,index,value){
            var strip=new H.geo.Strip();
            strip.pushPoint(coord);
            strip.pushPoint(nextcoord);
            var line=new H.map.Polyline(strip);
            var style=this.getLineStyle(coord,nextcoord,parsed,index,value);
            line.setStyle(style);
            line.setData({event:parsed.event,index:index,data:value});
            return line
        },
        createPointMarker: function(coord,parsed,index,value){
            var pointmarker;
            if(this.options.pointmarker!==undefined){
                pointmarker=this.options.pointmarker(coord,parsed.event,index,value);
            }else{
                pointmarker=this.defaultPointMarker(coord,parsed.event,index,value);
            }
            if(pointmarker){
                pointmarker.setData({event:parsed.event,index:index,data:value});
            }
            return pointmarker;
        },
        createLineMarker: function(coord,nextcoord,parsed,index,value){
            var linemarker;
            if(this.options.linemarker!==undefined){
                linemarker=this.options.linemarker(coord,nextcoord,parsed.event,index,value);
            }else{
                linemarker=this.defaultLineMarker(coord,nextcoord,parsed.event,index,value);
            }
            if(linemarker){
                linemarker.setData({event:parsed.event,index:index,data:value});

            }
            return linemarker;
        },

        pointMarkerTapEventListener: function(evt){
            var bubble =  new H.ui.InfoBubble(evt.target.getPosition(), {
                content: this.options.pointMarkerBubbleContentProvider(evt.target.getData())
            });
            this.ui.addBubble(bubble);
        },
        lineMarkerTapEventListener: function(evt){
            var bubble =  new H.ui.InfoBubble(evt.target.getPosition(), {
                content: this.options.lineMarkerBubbleContentProvider(evt.target.getData())
            });
            this.ui.addBubble(bubble);
        },
        lineTapEventListener: function(evt){
            var pos=this.map.screenToGeo(evt.currentPointer.viewportX,evt.currentPointer.viewportY);
            var bubble =  new H.ui.InfoBubble(pos, {
                content: this.options.lineBubbleContentProvider(evt.target.getData())
            });
            this.ui.addBubble(bubble);
        },

        createMapVisualization: function(){
            var pointmarkergroup = new H.map.Group();
            var linemarkergroup = new H.map.Group();
            var linegroup = new H.map.Group();

            // iterate over all the data and render it
            for(var i=0;i<this.events.length;i++){
                parsed=this.events[i];

                for(var j=0;j<parsed.coords.length;j++){
                    var point=parsed.points[j];
                    var coord=parsed.coords[j];
                    var value,nextcoord;
                    try{
                        // try to get the value & next coordinate
                        value=parsed.values[j];
                        nextcoord=parsed.coords[j+1];
                    }catch(err){

                    }

                    // render the line
                    if(value && nextcoord){
                        var line=this.createLine(coord,nextcoord,parsed,j,value);
                        /*
                        line.setZIndex(1);
                        var strip=new H.geo.Strip();
            strip.pushPoint(coord);
            strip.pushPoint(nextcoord);
            var borderline=new H.map.Polyline(strip);
            var style=line.getStyle();
            style.lineWidth=style.lineWidth+1
            style.strokeColor="#222222";
            borderline.setStyle(style);
            borderline.setZIndex(0);
*/
                        var that=this;
                        if(this.options.lineBubbleContentProvider){
                            line.addEventListener('tap',function(evt){that.lineTapEventListener(evt)},false);
                        }
                        //linegroup.addObject(borderline);
                        linegroup.addObject(line);

                    }

                    // render the point marker
                    var pointmarker=this.createPointMarker(coord,parsed,j,point);
                    if(pointmarker){
                        pointmarkergroup.addObject(pointmarker);
                    }

                    // render the line marker
                    if(value && nextcoord){
                        var linemarker=this.createLineMarker(coord,nextcoord,parsed,j,value);
                        if(linemarker){
                            linemarkergroup.addObject(linemarker);
                        }
                    }
                }
            }

            // add listeners to point & line markers
            var that=this;
            if(this.options.pointMarkerBubbleContentProvider){
                pointmarkergroup.addEventListener('tap', function (evt) {
                    that.pointMarkerTapEventListener(evt);
                }, false);
            }
            if(this.options.lineMarkerBubbleContentProvider){
                linemarkergroup.addEventListener('tap', function (evt) {
                    that.lineMarkerTapEventListener(evt);
                }, false);
            }

            // add all the needed groups to the main group
            this.group.addObject(pointmarkergroup);
            this.group.addObject(linemarkergroup);
            this.group.addObject(linegroup);
        },

        parseEvent: function(event){
            parsed={"coords":[],"points":[],"values":[]};
            if( "coords" in event){
                // create the event data structure if the needed fields exist
                for(var i=0;i<event.coords.length;i++){
                    // get the coordinate
                    var coord=event.coords[i].split(",");
                    coord={lat: Number(coord[0]), lng: Number(coord[1])};
                    parsed.coords.push(coord);

                    // get the point
                    if("points" in event){
                        if(Object.prototype.toString.call( event.points ) === '[object Array]'){
                            if(event.points[i]!==undefined){
                                point=event.points[i];
                            }
                        } else{
                            point=event.points;
                        }
                        parsed.points.push(point);

                        // check the min/max value for a point
                        try{
                            point=Number(point);
                            if(this.maxPointValue<point) this.maxPointValue=point;
                            if(this.minPointValue>point) this.minPointValue=point;
                        }catch(err){
                            console.debug("Point is not a number");
                        }
                    }
                    if("values" in event){
                        if(Object.prototype.toString.call( event.values ) === '[object Array]'){
                            if(event.values[i]!==undefined){
                                value=event.values[i];
                            }
                        } else{
                            value=event.values;
                        }
                        parsed.values.push(value);

                        // check the min/max value for a line value
                        try{
                            value=Number(value);
                            if(this.maxLineValue<value) this.maxLineValue=value;
                            if(this.minLineValue>value) this.minLineValue=value;
                        }catch(err){
                            console.debug("Value is not a number");
                        }
                    }
                }
            }
            parsed.event=event;
            return parsed;
        },

        updateView: function(viz, data) {
            this.events=[];
            if(this.map){
                this.clearView();

                this.maxLineValue=-Number.MAX_VALUE;
                this.minLineValue=Number.MAX_VALUE;
                this.maxPointValue=-Number.MAX_VALUE;
                this.minPointValue=Number.MAX_VALUE;

                for(var i=0;i<data.length;i++){
                    event=this.parseEvent(data[i]);
                    this.events.push(event);
                }

                this.createMapVisualization();
                this.map.addObject(this.group);
            }
            this._clearMessage();
        },

        clearView: function(){
            if(this.map && this.group){
                this.group.removeAll();
            }
        },

        postCreateMap: function(){
            // Add the getData and setData method to a polyline
            H.map.Polyline.prototype.getData=function(){ return this.data;};
            H.map.Polyline.prototype.setData=function(data){ this.data=data;return this;};
        }
    });

    return HereLineMap;
});
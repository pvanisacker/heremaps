define(function(require, exports, module) {
    // Load requirements
    var _ = require('underscore');
    var mvc = require('splunkjs/mvc');
    var HereMap = require('app/heremaps/heremaps/heremap');
    var Messages = require("splunkjs/mvc/messages");
    var utils = require('splunkjs/mvc/utils');
    
    // Define the custom view class
    var HereShapeMap = HereMap.extend({
        className: "hereshapemap",

        reader: undefined,
        shapes: {},
        maxValue:-Number.MAX_VALUE,
        minValue:Number.MAX_VALUE,
        options:{
            shapeType:"kml",
            kmlFile:"world2.kml",
            colorRange:{
                "0.0"   :"rgba(0,255,64,0.6)",
                "0.1"   :"rgba(0,255,0,0.6)",
                "0.2"   :"rgba(64,255,0,0.6)",
                "0.3"   :"rgba(128,255,0,0.6)",
                "0.4"   :"rgba(192,255,0,0.6)",
                "0.5"   :"rgba(255,255,0,0.6)",
                "0.6"   :"rgba(255,192,0,0.6)",
                "0.7"   :"rgba(255,128,0,0.6)",
                "0.8"   :"rgba(255,64,0,0.6)",
                "0.9"   :"rgba(255,0,0,0.6)"
            },
            defaultStyle: {
                        strokeColor: 'rgba(191,191,191,0.8)',
                        fillColor: 'rgba(255, 255, 255, 0)',
                        lineWidth: 1.5,
                        lineCap: 'square',
                        lineJoin: 'bevel'
            },
            bubbleContentProvider: function(shape,data){return "<div style='text-align:center;'>"+shape.name+": "+data.value+"</div>";}
        },


        updateView: function(viz, data) {
            // remove the existing values
            for(var key in this.shapes){
                if("value" in this.shapes[key]){
                    delete this.shapes[key].value;
                }
            }

            // update the map with the new results
            this.maxValue=-Number.MAX_VALUE;
            this.minValue=Number.MAX_VALUE;
            for(var seq in data){
                var result=data[seq];
                if("key" in result && "value" in result){
                    if(!(result.key in this.shapes)){
                        this.shapes[result.key]={};
                    }
                    value=parseFloat(result.value);
                    if(!isNaN(value)){
                        this.shapes[result.key].value=value;
                        this.shapes[result.key].result=result;
                        if(this.maxValue<value) this.maxValue=value;
                        if(this.minValue>value) this.minValue=value;
                    }
                }
            }
            this.colorShapes();
            this._clearMessage();
        },
        clearView: function(){
            // set all the shapes to the default style
            for(var shape in this.shapes){
                this.colorShape(shape,this.options.defaultStyle);
            }
        },
        postCreateMap: function(){
            // load the map shapes
            if(this.options.shapeType==="kml"){
                this.reader = new H.data.kml.Reader('/static/app/heremaps/data/'+this.options.kmlFile);
            }
            if(this.options.shapeType==="geojson"){
                this.reader = new H.data.geojson.Reader('/static/app/heremaps/data/'+this.options.geoJSONFile);
            }
            var that=this;
            this.reader.addEventListener('statechange', function(evt) {
                if(evt.state == H.data.AbstractReader.State.READY){
                    that._onShapesLoaded();
                }
            });
            this.reader.parse();
            this.layer=this.reader.getLayer();

            // Add listener for info bubble on click
            if(this.options.bubbleContentProvider){
                this.layer.getProvider().addEventListener('tap', function(evt) {
                    var data,shape;
                    if(that.options.shapeType==="kml"){
                        data=that.shapes[evt.target.getData().description];
                        shape=evt.target.getData();
                    }
                    if(that.options.shapeType==="geojson"){
                        data=that.shapes[evt.target.getParentGroup().getData().properties.id];
                        shape=evt.target.getParentGroup().getData().properties;
                    }
                    var bubble =  new H.ui.InfoBubble(that.map.screenToGeo(evt.currentPointer.viewportX, evt.currentPointer.viewportY), {
                        content: that.options.bubbleContentProvider(shape,data)
                    });
                    that.ui.addBubble(bubble);
                });
            }
            this.map.addLayer(this.layer);
        },

        _onShapesLoaded: function(){
            // iterate over all the shapes and add them to as "obj" to this.shapes
            var objs=[];
            if(this.options.shapeType==="kml"){
                objs=this.reader.getParsedObjects();
            }
            if(this.options.shapeType==="geojson"){
                objs=this.reader.getParsedObjects();
                objs=objs[0].getObjects();
            }

            var that=this;
            var enterfunction=function(event){
                            var group=event.target.getParentGroup();
                            if(that.options.shapeType==="kml"){
                                key=group.getData().description;
                            }
                            if(that.options.shapeType==="geojson"){
                                key=group.getData().properties.id;
                            }
                            that.shapes[key].state="enter";
                            that.colorShape(key);
                        };
            var leavefunction=function(event){
                            var group=event.target.getParentGroup();
                            if(that.options.shapeType==="kml"){
                                key=group.getData().description;
                            }
                            if(that.options.shapeType==="geojson"){
                                key=group.getData().properties.id;
                            }
                            that.shapes[key].state="normal";
                            that.colorShape(key);
                        };

            for(var i=0;i<objs.length;i++){
                var obj=objs[i];
                if (obj instanceof H.map.Group){
                    if(this.options.shapeType==="kml"){
                        key=obj.getData().description;
                    }
                    if(this.options.shapeType==="geojson"){
                        key=obj.getData().properties.id;
                    }
                    if (!(key in this.shapes)){
                        this.shapes[key]={};
                    }
                    this.shapes[key].obj=obj;

                    obj.forEach(function(poly){
                        poly.addEventListener('pointerenter',enterfunction);
                        poly.addEventListener('pointerleave',leavefunction);
                    });

                }
            }
            this.colorShapes();
        },

        colorShapes: function(){
            // iterate over all the shapes and trigger the coloring
            for(var key in this.shapes){
                this.colorShape(key);
            }
        },
        colorShape: function(key){
            var style = this.styleProvider(key);
            this.colorShapeStyle(key,style);
        },
        colorShapeStyle: function(key,style){
            // color a certain shape with a certain style
            var shape_group=this.shapes[key].obj;

            if(shape_group){
                var index=0;
                if("state" in this.shapes[key] && this.shapes[key].state=="enter"){
                    index=5;
                }
                shape_group.setZIndex(index);
                shape_group.forEach(function(obj){
                    if(obj instanceof H.map.Polygon){
                        obj.setStyle(style);
                    }
                });
            }
        },
        styleProvider: function(key){
            // clone the style
            var style={
                strokeColor: this.options.defaultStyle.strokeColor,
                fillColor: this.options.defaultStyle.fillColor,
                lineWidth: this.options.defaultStyle.lineWidth,
                lineCap: this.options.defaultStyle.lineCap,
                lineJoin: this.options.defaultStyle.lineJoin
            };
            if("value" in this.shapes[key]){
                value=this.shapes[key].value;
                var percent = (value - this.minValue) / (this.maxValue - this.minValue);
                for(var color in this.options.colorRange){
                    if(percent>=parseFloat(color)){
                        style.fillColor=this.options.colorRange[color];
                    }
                }
            }
            if(key in this.shapes){
                if(("state" in this.shapes[key]) && this.shapes[key].state=="enter"){
                    style.lineWidth=4;
                }
            }
            return style;
        }
    });

    return HereShapeMap;
});
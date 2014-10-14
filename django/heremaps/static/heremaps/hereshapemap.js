define(function(require, exports, module) {
    // Load requirements
    var _ = require('underscore');
    var mvc = require('splunkjs/mvc');
    var HereMap = require('heremaps/heremap');
    var Messages = require("splunkjs/mvc/messages");
    var utils = require('splunkjs/mvc/utils');
    
    // Define the custom view class
    var HereShapeMap = HereMap.extend({
        className: "hereshapemap",

        reader: undefined,
        shapes: {},
        maxValue:0.0,
        options:{
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
        },


        updateView: function(viz, data) {
            for(var seq in data){
                var result=data[seq];
                if("key" in result && "value" in result){
                    if(result["key"] in this.shapes){
                        value=parseFloat(result["value"])
                        if(value!=NaN){
                            this.shapes[result["key"]]["value"]=value
                            if(this.maxValue<result["value"]) this.maxValue=value
                        }
                    }else{
                        console.warn("Could not find result "+result["key"]+" in shape list");
                    }
                }
            }
            this.colorShapes();
            this._clearMessage();
        },
        clearView: function(){
            for(var shape in this.shapes){
                this.colorShape(shape,this.options.defaultStyle)
            }
        },
        postCreateMap: function(){
            this.reader = new H.data.kml.Reader('../../../static/data/'+this.options.kmlFile);
            var that=this
            this.reader.addEventListener('statechange', function(evt) {
                if(evt.state == H.data.AbstractReader.State.READY){
                    that._onDataLoaded();
                }
            });

            this.reader.parse();
            this.map.addLayer(this.reader.getLayer());
        },

        _onDataLoaded: function(){
            objs=this.reader.getParsedObjects();
            for(var i=0;i<objs.length;i++){
                obj=objs[i]
                if (obj instanceof H.map.Group){
                    key=obj.getData()["description"]
                    if (!(key in this.shapes)){
                        this.shapes[key]={}
                    }
                    this.shapes[key]["obj"]=obj
                }
            }
            this.colorShapes()
        },

        colorShapes: function(){
            for(var key in this.shapes){
                var value=0;
                if("value" in this.shapes[key]){
                    value=this.shapes[key]["value"]
                }
                style = this.styleProvider(value);
                // console.log(key)
                // console.log(style.fillColor);
                this.colorShape(key,style);
            }
        },

        colorShape: function(key,style){
            shape_group=this.shapes[key]["obj"]
            if(shape_group){
                shape_group.forEach(function(obj,idx,group){
                    if(obj instanceof H.map.Polygon){
                        obj.setStyle(style);
                    }
                });
            }
        },
        styleProvider: function(value){
            // clone the style
            style={
                strokeColor: this.options.defaultStyle.strokeColor,
                fillColor: this.options.defaultStyle.fillColor,
                lineWidth: this.options.defaultStyle.lineWidth,
                lineCap: this.options.defaultStyle.lineCap,
                lineJoin: this.options.defaultStyle.lineJoin
            }
            if(value && value!=0){
                var percent=value/this.maxValue;
                for(var key in this.options.colorRange){
                    if(percent>=parseFloat(key)){
                        style.fillColor=this.options.colorRange[key];
                    }
                }
            }
            return style;
        }
    });

    return HereShapeMap;
});
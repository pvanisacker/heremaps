define(function(require, exports, module) {
    // Load requirements
    var _ = require('underscore');
    var mvc = require('splunkjs/mvc');
    var SimpleSplunkView = require('splunkjs/mvc/simplesplunkview');
    var Messages = require("splunkjs/mvc/messages");
    var utils = require('splunkjs/mvc/utils');

    Messages.messages['map-error']={icon: "warning-sign",level: "error",message: _("Map loading failed").t()};

    // Define the custom view class
    var HereHeatMap = SimpleSplunkView.extend({
        className: "hereheatmap",
        outputMode: 'json',

        default_options: {
            center: "0,0",
            zoom: 2,
            height: "400px",
            app_id:"",
            app_code:"",
        },

        options: {
            colors: undefined,
            opacity: 1,
            type: "density",
            coarseness: "2"
        },

        initialize: function(){
            this.configure();

            this.$el.html(
                    '<div class="heremapwrapper" style="height:'+this.options.height+'">'+
                    '<div id="'+this.id+'-msg"></div>'+
                    '<div style="height: '+this.options.height+'; min-height:'+this.options.height+'; min-width:100%;" id="'+this.id+'-map" class="mapcontainer"></div>'+
                    '</div>')

            this.message = this.$('#'+this.id+'-msg');

            this._setOptions();

            this._get_app_id();

            this._viz = null;
            this._data = null;
            this.bindToComponentSetting('managerid', this._onManagerChange, this);
            if (!this.manager) {
                this._onManagerChange(mvc.Components, null);
            }
        },

        updateView: function(viz, data){
            this.clearView();
            heat_data=[];
            for(res in data){
                if("lat" in data[res] && "lng" in data[res]){
                    var lat=parseFloat(data[res]["lat"])
                    var lng=parseFloat(data[res]["lng"])
                    var value=parseFloat(data[res]["value"])
                    heat_data.push({"latitude":lat,"longitude":lng,"value":value});
                }
            }
            this.heatmapProvider=this.getHeatMapProvider();
            this.heatmapProvider.addData(heat_data);
            this.map.overlays.add(this.heatmapProvider);
            this._clearMessage();
        },

        clearView: function(){
            this.map.overlays.remove(this.heatmapProvider)
        },

        createView: function(){
            return this;
        },

        displayMessage: function(info){
            if(info=="no-results"){
                this.clearView();
            }else{
                Messages.render(info, this.message);
                this.message.show();
            }
            return this;
        },

        createMap: function(){
            try {
                nokia.Settings.set("app_id", this.options.app_id);
                nokia.Settings.set("app_code", this.options.app_code);

                options={
                    zoomLevel:parseInt(this.options.zoom),
                    components:[new nokia.maps.map.component.Behavior()],
                    center:[parseFloat(this.options.center.split(",")[0]),parseFloat(this.options.center.split(",")[1])]
                }
                console.log(options)
                this.map = new nokia.maps.map.Display(document.getElementById(this.id+'-map'), options);
                this.map.set("baseMapType", nokia.maps.map.Display.TERRAIN);

                if(this.postCreateMap){
                    this.postCreateMap()
                }
            }catch(err){
                this._errorMessage();
                console.error("Error loading map components")
                console.error(err.stack)
            }
        },

        _get_app_id: function(){
            var that=this;
            mvc.createService().get("/servicesNS/nobody/heremaps/configs/conf-setup/heremaps",{},function(err,response) {
                if(err){
                    console.error("Error fetching app_id");
                    return;
                }
                content=response.data.entry[0].content;

                if(content.app_id.trim()=="" || content.app_code.trim()==""){
                    console.error("No app_id & app_code found, make sure to set on in the heremaps setup screen");
                    that._errorMessage();
                }else{
                    that.options.app_id=content.app_id.trim();
                    that.options.app_code=content.app_code.trim();
                    that.createMap();
                }
            });
        },

        _clearMessage: function(){
            if(this.map){
                this.message.hide();
            }else{
                this._errorMessage();
            }
        },

        _errorMessage: function(){
            Messages.render('map-error',this.message);
            this.message.show();
        },

        _setOptions: function(){
            if(!this.options.center || this.options.center.trim()==""){
                this.options.center=this.default_options.center;
            }
            if(!this.options.zoom){
                this.options.zoom=this.default_options.zoom;
            }
            if(!this.options.height || this.options.height.trim()==""){
                this.options.height=this.default_options.height;
            }
        },

        getHeatMapProvider: function(){
            // Creating Heatmap overlay
            var options={
                max:20,
                opacity: this.options.opacity,
                type: this.options.type,
                coarseness: this.options.coarseness
            };
            if(this.options.colors){
                options["colors"]=this.options.colors;
            }
            var heatmapProvider = new nokia.maps.heatmap.Overlay(options);
            return heatmapProvider;
        }
    });
    return HereHeatMap;
});
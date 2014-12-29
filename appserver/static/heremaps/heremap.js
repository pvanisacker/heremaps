define(function(require, exports, module) {
    // Load requirements
    var _ = require('underscore');
    var mvc = require('splunkjs/mvc');
    var SimpleSplunkView = require('splunkjs/mvc/simplesplunkview');
    var Messages = require("splunkjs/mvc/messages");
    var utils = require('splunkjs/mvc/utils');

    Messages.messages['map-error']={icon: "warning-sign",level: "error",message: _("Map loading failed").t()};

    // Define the custom view class
    var HereMap = SimpleSplunkView.extend({
        className: "heremap",
        outputMode: 'json',

        default_options: {
            center: "0,0",
            zoom: 2,
            height: "400px",
            app_id:"",
            app_code:""
        },

        initialize: function(){
            this.configure();

            this.$el.html(
                    '<div class="heremapwrapper" style="height:'+this.options.height+'">'+
                    '<div id="'+this.id+'-msg"></div>'+
                    '<div style="height: '+this.options.height+'; min-height:'+this.options.height+'; min-width:100%;" id="'+this.id+'-map" class="mapcontainer"></div>'+
                    '</div>');

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
                var platform = new H.service.Platform({
                    app_id: this.options.app_id,
                    app_code: this.options.app_code,
                    useHTTPS: true
                });
                // Obtain the default map types from the platform object:
                var defaultLayers = platform.createDefaultLayers();
                // Instantiate (and display) a map object:
                var options={zoom:this.options.zoom};
                try{
                    options.center={lat:parseFloat(this.options.center.split(",")[0]),lng:parseFloat(this.options.center.split(",")[1])};
                }catch(err){
                    console.error("Could not parse center lat,lng combination");
                }
                this.map = new H.Map(document.getElementById(this.id+'-map'),defaultLayers.terrain.map,options);

                var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(this.map));
                this.ui=H.ui.UI.createDefault(this.map,defaultLayers);
                this.ui.removeControl('mapsettings');

                var aerialMapTileService = platform.getMapTileService({type: 'aerial'});
                var terrainMap = aerialMapTileService.createTileLayer('maptile','terrain.day',256,'png8');
                this.map.setBaseLayer(terrainMap);

                if(this.postCreateMap){
                    this.postCreateMap();
                }
            }catch(err){
                this._errorMessage();
                console.error("Error loading map components");
                console.error(err.stack);
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

                if(content.app_id.trim()==="" || content.app_code.trim()===""){
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

        clearView: function(){
            throw new Error("Not implemented error.");
        },

        _setOptions: function(){
            if(!this.options.center || this.options.center.trim()===""){
                this.options.center=this.default_options.center;
            }
            if(!this.options.zoom){
                this.options.zoom=this.default_options.zoom;
            }
            if(!this.options.height || this.options.height.trim()===""){
                this.options.height=this.default_options.height;
            }
        }
    });
    return HereMap;
});
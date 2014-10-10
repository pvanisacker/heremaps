define(function(require, exports, module) {
    // Load requirements
    var _ = require('underscore');
    var mvc = require('splunkjs/mvc');
    var HereMap = require('heremaps/heremap');
    var Messages = require("splunkjs/mvc/messages");
    var utils = require('splunkjs/mvc/utils');
    
    // Define the custom view class
    var HereMarkerMap = HereMap.extend({
        className: "heremarkermap",

        options: {
            marker:undefined
        },

        updateView: function(viz, data) {
            if(this.map){
                this.clearView();
                for(var i=0;i<data.length;i++){
                    if(this.options.marker){
                        var marker=this.options.marker(data[i]);
                    }else{
                        var marker=new H.map.Marker({lat:data[i]["lat"],lng:data[i]["lng"]});
                    }
                    // marker=new H.map.Marker({lat:data[i]["lat"],lng:data[i]["lng"]});

                    viz.map.addObject(marker);
                }
            }
            this._clearMessage();
        },
    });

    return HereMarkerMap;
});
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
            // Add a listener to the group to show the dialog box.
            var that=this;
            if(this.options.bubbleContentProvider){
                this.group.addEventListener('tap', function (evt) {
                    var bubble =  new H.ui.InfoBubble(evt.target.getPosition(), {
                       content: that.options.bubbleContentProvider(evt.target.getData())
                    });
                    that.ui.addBubble(bubble);
                }, false);
            }
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
                    marker.setData(data[i]);
                    // Add marker to group
                    this.group.addObject(marker);
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
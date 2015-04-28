define([
    "app/heremaps/heremaps/heremap",
    ],
    function(HereMap) {

    /**
     * A module exposing a marker map
     * @module heremaps/HereMarkerMap
     * @extends module:heremaps/HereMap
    */
    var HereMarkerMap = HereMap.extend({
        className: "heremarkermap",

         /**
         * Sets the options for the marker map
         * @property {function} options.marker                - Provides the marker to be displayed. The function should return a valid Marker. See: {@link https://developer.here.com/javascript-apis/documentation/v3/maps/topics_api_nlp/h-map-marker.html}
         * @property {function} options.bubbleContentProvider - Provides the content to be show when a marker is clicked.
         */
        options: {
            marker:undefined,
            bubbleContentProvider: function(data){return "<div style='text-align:center;'>"+String(data.value).encodeHTML()+"</div>";}
        },
        group:new H.map.Group(),

        defaultMarker: function(data){
            return new H.map.Marker({lat:data.lat,lng:data.lng});
        },

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
                    var marker;
                    if(this.options.marker){
                        marker=this.options.marker(data[i]);
                    }else{
                        marker=this.defaultMarker(data[i]);
                    }
                    if(marker){
                        marker.setData(data[i]);
                        // Add marker to group
                        this.group.addObject(marker);
                    }
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
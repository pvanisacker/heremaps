define([
    "app/heremaps/heremaps/heremap",
    "heremapsjsClustering"
    ],
    function(HereMap) {

    /**
     * A module exposing a cluster map
     * @module heremaps/HereClusterMap
     * @extends module:heremaps/HereMap
    */
    var HereClusterMap = HereMap.extend({
        className: "hereclustermap",

        /**
         * Sets the options for the cluster map
         * @property {integer} options.min_weight - The minimum weight for a cluster to form
                                                      See: {@link https://developer.here.com/javascript-apis/documentation/v3/maps/topics_api_nlp/h-clustering-provider-clusteringoptions.html#h-clustering-provider-clusteringoptions__minweight}
         * @property {integer} options.eps        - The EPS
         *                                            See: {@link https://developer.here.com/javascript-apis/documentation/v3/maps/topics_api_nlp/h-clustering-provider-clusteringoptions.html#h-clustering-provider-clusteringoptions__eps}
         * @property {object} options.theme       - The cluster theme to be used.
         *                                            See: {@link https://developer.here.com/javascript-apis/documentation/v3/maps/topics_api_nlp/h-clustering-itheme.html}
         * @property {function} options.noiseBubbleContentProvider      - This function returns the HTML content used to fill the InfoBubble that gets shown when a noise point gets clicked.
         * @property {function} options.clusterBubbleContentProvider    - This function returns the HTML content used to fill the InfoBubble that gets shown when a cluster point gets clicked.
         */
        options: {
            min_weight: 1,
            eps: 32,
            theme: undefined,
            noiseBubbleContentProvider: function(data){
                return "<div style='text-align:center'>"+String(data.getData().value).encodeHTML()+"</div>";
            },
            clusterBubbleContentProvider: function(data){
                var count=0;
                data.forEachDataPoint(function(dataPoint){
                    count+=1;
                });
                return "<div style='text-align:center'>"+count+"</div>";
            }
        },

        /**
         * The layer containing the clustering markers
         * @private
         */
        clusteringLayer:undefined,

        /** This function will read through the result data and update the map
         * @private
         */
        updateView: function(viz, data) {
            if(this.map){
                this.clearView();

                var dataPoints = [];
                for(var i=0;i<data.length;i++){
                    dataPoints.push(new H.clustering.DataPoint(data[i].lat,data[i].lng,1,data[i]));
                }

                var options={clusteringOptions: {
                        minWeight: this.options.min_weight,
                        eps: this.options.eps
                    },
                    theme:{}
                };

                if(this.options.theme){
                    options.theme=this.options.theme;
                }else{
                    options.theme=new H.clustering.DefaultTheme();
                }

                this.clusteringProvider = new H.clustering.Provider(dataPoints, options);
                this.clusteringLayer = new H.map.layer.ObjectLayer(this.clusteringProvider);

                var that=this;
                if(this.options.noiseBubbleContentProvider || this.options.clusterBubbleContentProvider){
                    this.clusteringProvider.addEventListener('tap', function (evt) {
                        var data=evt.target.getData();
                        if(data instanceof H.clustering.NoisePoint && that.options.noiseBubbleContentProvider){
                            var bubblenoise =  new H.ui.InfoBubble(evt.target.getPosition(), {
                                content: that.options.noiseBubbleContentProvider(data)
                            });
                            that.ui.addBubble(bubblenoise);
                        }else if(data instanceof H.clustering.Cluster && that.options.clusterBubbleContentProvider){
                            var bubblecluster =  new H.ui.InfoBubble(evt.target.getPosition(), {
                                content: that.options.clusterBubbleContentProvider(data)
                            });
                            that.ui.addBubble(bubblecluster);
                        }

                    }, false);
                }


                this.map.addLayer(this.clusteringLayer);
            }
            this._clearMessage();
        },

        /**
         * This function will remove the cluster markers from the map
         * @private
         */
        clearView: function(){
            if(this.map && this.clusteringLayer){
                this.map.removeLayer(this.clusteringLayer);
            }
        }
    });

    return HereClusterMap;
});
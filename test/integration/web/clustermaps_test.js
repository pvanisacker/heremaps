casper.test.begin('Cluster map loads', function suite(test){
  testMapLoading(heremapshome+"/clustermap",casper,test);
});

casper.test.begin('Custom cluster map loads', function suite(test){
  testMapLoading(heremapshome+"/clustermapcustom",casper,test);
});

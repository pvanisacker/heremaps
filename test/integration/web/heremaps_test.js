/*
  This file will test the basic map loading of the existing dashboards
*/

casper.test.begin('Heremaps loads', function suite(test){
  testMapLoading(heremapshome+"/heremaps",casper,test);
});

casper.test.begin('Heat map loads', function suite(test){
  testMapLoading(heremapshome+"/heatmap",casper,test);
});

casper.test.begin('Custom heat map 1 loads', function suite(test){
  testMapLoading(heremapshome+"/heatmapcustom1",casper,test);
});

casper.test.begin('Custom heat map 2 loads', function suite(test){
  testMapLoading(heremapshome+"/heatmapcustom2",casper,test);
});

casper.test.begin('Marker map loads', function suite(test){
  testMapLoading(heremapshome+"/markermap",casper,test);
});

casper.test.begin('Custom marker map loads', function suite(test){
  testMapLoading(heremapshome+"/markermapcustom",casper,test);
});

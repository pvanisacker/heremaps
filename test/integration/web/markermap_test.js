casper.test.begin('Marker map loads', function suite(test){
  testMapLoading(heremapshome+"/markermap",casper,test);
});

casper.test.begin('Custom marker map loads', function suite(test){
  testMapLoading(heremapshome+"/markermapcustom",casper,test);
});
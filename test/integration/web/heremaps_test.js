casper.test.begin('Heremaps loads', function suite(test){
  testMapLoading(heremapshome+"/heremaps",casper,test);
});

casper.test.begin('Heremaps simple loads', function suite(test){
  testMapLoading(heremapshome+"/map-simple",casper,test);
});
casper.test.begin('Heat map loads', function suite(test){
  testMapLoading(heremapshome+"/heatmap",casper,test);
});

casper.test.begin('Custom heat map 1 loads', function suite(test){
  testMapLoading(heremapshome+"/heatmapcustom1",casper,test);
});

casper.test.begin('Custom heat map 2 loads', function suite(test){
  testMapLoading(heremapshome+"/heatmapcustom2",casper,test);
});

casper.test.begin('Heat map simple loads', function suite(test){
  testMapLoading(heremapshome+"/heatmap-simple",casper,test);
});
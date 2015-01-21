casper.test.begin('Custom line map 1 loads', function suite(test){
  testMapLoading(heremapshome+"/linemap1",casper,test);
});

casper.test.begin('Custom line map 2 loads', function suite(test){
  testMapLoading(heremapshome+"/linemap2",casper,test);
});

casper.test.begin('Custom line map 3 loads', function suite(test){
  testMapLoading(heremapshome+"/linemap3",casper,test);
});
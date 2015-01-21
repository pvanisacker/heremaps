casper.test.begin('Shape map loads', function suite(test){
  testMapLoading(heremapshome+"/shapemap",casper,test);
});

casper.test.begin('Custom shape map 1 loads', function suite(test){
  testMapLoading(heremapshome+"/shapemapcustom1",casper,test);
});

casper.test.begin('Custom shape map 2 loads', function suite(test){
  testMapLoading(heremapshome+"/shapemapcustom2",casper,test);
});

casper.test.begin('Custom shape map 3 loads', function suite(test){
  testMapLoading(heremapshome+"/shapemapcustom3",casper,test);
});

casper.test.begin('Custom shape map 4 loads', function suite(test){
  testMapLoading(heremapshome+"/shapemapcustom4",casper,test);
  casper.then(function(){
    test.assertExists(x("//div[@class='mapcontainer' and @id='map1-map']/div"),"Belgian map loads");
    test.assertExists(x("//div[@class='mapcontainer' and @id='map2-map']/div"),"Spain map loads");
    test.assertExists(x("//div[@class='mapcontainer' and @id='map3-map']/div"),"Russian map loads");
    test.assertExists(x("//div[@class='mapcontainer' and @id='map4-map']/div"),"China map loads");
    test.assertExists(x("//div[@class='mapcontainer' and @id='map5-map']/div"),"Canadian map loads");
    test.assertExists(x("//div[@class='mapcontainer' and @id='map6-map']/div"),"Brazilian map loads");
    test.assertExists(x("//div[@class='mapcontainer' and @id='map7-map']/div"),"Italian map loads");
  });
});

casper.test.begin('Custom shape map 5 loads', function suite(test){
  testMapLoading(heremapshome+"/shapemapcustom5",casper,test);
});

casper.test.begin('Continents shape map loads', function suite(test){
  testMapLoading(heremapshome+"/shapemapcustom_continents",casper,test);
  casper.then(function(){
    test.assertExists(x("//div[@class='mapcontainer' and @id='map1-map']/div"),"European map loads");
    test.assertExists(x("//div[@class='mapcontainer' and @id='map2-map']/div"),"Asian map loads");
    test.assertExists(x("//div[@class='mapcontainer' and @id='map3-map']/div"),"South American map loads");
    test.assertExists(x("//div[@class='mapcontainer' and @id='map4-map']/div"),"North American map loads");
    test.assertExists(x("//div[@class='mapcontainer' and @id='map5-map']/div"),"Oceania map loads");
    test.assertExists(x("//div[@class='mapcontainer' and @id='map6-map']/div"),"African map loads");
  });
});

casper.test.begin('German shape map loads', function suite(test){
  testMapLoading(heremapshome+"/shapemapcustom_de",casper,test);
});

casper.test.begin('French shape map loads', function suite(test){
  testMapLoading(heremapshome+"/shapemapcustom_fr",casper,test);
});

casper.test.begin('Indian shape map loads', function suite(test){
  testMapLoading(heremapshome+"/shapemapcustom_in",casper,test);
});

casper.test.begin('UK shape map loads', function suite(test){
  testMapLoading(heremapshome+"/shapemapcustom_uk",casper,test);
});

casper.test.begin('USA shape map loads', function suite(test){
  testMapLoading(heremapshome+"/shapemapcustom_us",casper,test);
});

casper.test.begin('US counties shape map loads', function suite(test){
  testMapLoading(heremapshome+"/shapemapcustom_us_counties",casper,test,5000);
});

casper.test.begin('Square shape map loads', function suite(test){
  testMapLoading(heremapshome+"/shapemapcustom_square",casper,test);
});

casper.test.begin('Hexagon shape map loads', function suite(test){
  testMapLoading(heremapshome+"/shapemapcustom_hexagon",casper,test);
});
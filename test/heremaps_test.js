var x = require('casper').selectXPath;
var splunkhome="http://localhost:8000/en-US";
casper.test.begin('Heremaps load maps', function suite(test){
  phantom.clearCookies();
  splunkLogin(casper,test);

  casper.thenOpen(splunkhome+"/app/heremaps/heremaps");
  waitForMap(casper,test);
  casper.then(function(){
    test.assertTitle("Heremaps");
  });

  casper.run(function(){
    test.done();
  });
});

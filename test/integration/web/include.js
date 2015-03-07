var x = require("casper").selectXPath;
var splunkurl="http://localhost:8000/en-US";
var splunkhome="/home/pieter/Download/splunk-6.2.0/splunk";
var heremapshome=splunkurl+"/app/heremaps";
var heremapshtmldir=heremapshome+"/default/data/ui/html";


function splunkLogin(casper,test){
  var loginUrl=splunkurl+"/account/login";
  var startUrl=splunkurl+"/app/launcher/home";

  casper.start(loginUrl, function(){});

  casper.waitFor(
    function check(){
      // wait for loginUrl to load
      return (new RegExp(splunkurl)).test(this.getCurrentUrl());
    },
    function then(){},
    function timeout(){
      console.log(this.getCurrentUrl());
      test.fail("Start page loaded");
    }
  );

  casper.then(function(){
    if(casper.getCurrentUrl()==loginUrl){
      // Not logged in, logging in
      casper.waitFor(
        function check() {
          return this.getTitle()=="Login | Splunk";
        },
        function then() {},
        function timeout(){
          test.fail("Login page loaded");
        },
        1000
      );

      casper.thenClick(x("//a[text()='Continue']"));
      casper.waitFor(
        function check(){return this.getCurrentUrl()==splunkurl+"/app/launcher/home";},
        function then(){}
      );
    }else if(casper.getCurrentUrl()==startUrl){
      // already logged in, nothing left to do
    }
  });
}

function waitForMap(casper,test,timeout){
  if(timeout===undefined){
    timeout=2000;
  }
  casper.waitFor(
    function check(){
      return this.exists(x("//div[@class='mapcontainer']/div"));
    },
    function then(){
      test.pass("Map loaded");
    },
    function timeout(){
      console.debug(this.getCurrentUrl());
      test.fail("Map loaded");
    },
    timeout
  );
}

function testMapLoading(page,casper,test){
  casper.start(page);
  waitForMap(casper,test);

  casper.run(function(){
    test.done();
  });
}

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

function waitForMap(casper,test){
  casper.waitFor(
    function check(){
      return this.exists(x("//div[@class='mapcontainer']/div"));
    },
    function then(){
      test.pass("Map loaded");
    },
    function timeout(){
      test.fail("Map loaded");
    },
    2000
  );
}

function testMapLoading(page,casper,test){
  splunkLogin(casper,test);

  casper.thenOpen(page);
  waitForMap(casper,test);

  casper.run(function(){
    test.done();
  });
}

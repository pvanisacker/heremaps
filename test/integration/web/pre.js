var loginUrl=splunkurl+"/account/login";
var startUrl=splunkurl+"/app/launcher/home";

// Don't load CSS it makes phantomjs a lot faster
casper.options.onResourceRequested = function(C, requestData, request) {
  if ((/https?:\/\/.+?\.css/gi).test(requestData.url) || requestData['Content-Type'] == 'text/css') {
    request.abort();
  }
};

  casper.start(loginUrl, function(){});

  casper.waitFor(
    function check(){
      // wait for loginUrl to load
      return (new RegExp(splunkurl)).test(this.getCurrentUrl());
    },
    function then(){
      casper.test.pass("Start page loaded");
    },
    function timeout(){
      console.log(this.getCurrentUrl());
      casper.test.fail("Start page loaded");
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
          casper.test.fail("Login page loaded");
        },
        1000
      );

      casper.thenClick(x("//a[text()='Continue']"));
      casper.waitFor(
        function check(){return this.getCurrentUrl()==splunkurl+"/app/launcher/home";},
        function then(){
          casper.test.pass("Logged in");
        },
        function timeout(){
          casper.test.fail("Logged in");
        }
      );
    }else if(casper.getCurrentUrl()==startUrl){
      // already logged in, nothing left to do
    }
  });

casper.run(function(){
    casper.test.done();
  });
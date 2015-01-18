function splunkLogin(casper,test){
  casper.start(splunkhome+"/account/login", function(){});

  casper.waitFor(
    function check() {
      return this.getTitle()=="Login | Splunk";
      },
      function then() {},
      function timeout(){
      test.fail("Page not loaded");
    },
    1000
  );

  casper.thenClick(x("//a[text()='Continue']"));
  casper.waitFor(function check(){return this.getCurrentUrl()==splunkhome+"/app/launcher/home";});
  return casper;
}

function waitForMap(casper,test){
casper.waitFor(
    function check(){
      return this.exists(x("//div[@class='mapcontainer']/div"));
    },
    function then(){},
    function timeout(){
      test.fail("Map not loaded");
    },
    2000
  );
}

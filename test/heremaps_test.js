var x = require('casper').selectXPath;
casper.test.begin('Heremaps load maps', function suite(test){
	phantom.clearCookies();
	casper.start("http://localhost:8000/en-US/account/login", function(){
	});

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
	casper.waitFor(function check(){return this.getCurrentUrl()=="http://localhost:8000/en-US/app/launcher/home";});

	casper.thenOpen("http://localhost:8000/en-US/app/heremaps/heremaps");
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
	casper.then(function(){
		test.assertTitle("Heremaps");
	});

	casper.run(function(){
		test.done();
	});
});

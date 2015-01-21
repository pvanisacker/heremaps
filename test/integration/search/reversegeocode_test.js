var assert = require("assert");
var splunkjs = require('splunk-sdk');

var service = new splunkjs.Service({
username: "admin",
password: "admin",
scheme: "http",
host: "localhost",
port: "8000",
version: "6.2.0"
});

describe('Reversegeocode', function(){
  describe('execute', function(){
    it('should return exactly one result', function(){
      assert.equal(-1, [1,2,3].indexOf(5));
      assert.equal(-1, [1,2,3].indexOf(0));


// Search everything and return the first 10 results
var searchQuery = "search * | head 1";

// Set the search parameters--specify a time range
var searchParams = {
  earliest_time: "2011-06-19T12:00:00.000-07:00",
  latest_time: "2012-12-02T12:00:00.000-07:00"
};

// Run a oneshot search that returns the job's results
service.oneshotSearch(
  searchQuery,
  searchParams,
  function(err, results) {
    // Display the results
    var fields = results.fields;
    var rows = results.rows;
    assert.equal(0,rows.length);S

    for(var i = 0; i < rows.length; i++) {
      var values = rows[i];
      console.log("Row " + i + ": ");

      for(var j = 0; j < values.length; j++) {
        var field = fields[j];
        var value = values[j];
        console.log("  " + field + ": " + value);
      }
    }
  }
);
    })
  })
})
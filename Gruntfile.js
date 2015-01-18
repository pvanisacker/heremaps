module.exports = function (grunt) {
  "use strict";

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    jshint: {
      all: [
        "Gruntfile.js",
        "appserver/static/heremaps/**/*.js",
        "bin/**/*.js"
      ],
      options: {
        jshintrc: ".jshintrc"
      }
    },
    inlinelint: {
      html: ["default/data/ui/html/**/*.html"]
    },
    casper : {
      options: {
        test: true,
      },
      test : {
        src: ['test/*_test.js']
      }
    }
  });
  
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-lint-inline');
  grunt.loadNpmTasks('grunt-casper');

  grunt.registerTask('test', ['jshint','inlinelint']);
  grunt.registerTask('default', ['test']);
};

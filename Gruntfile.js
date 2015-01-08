module.exports = function (grunt) {
  "use strict";

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    jshint: {
      all: [
        "Gruntfile.js",
        "appserver/static/heremaps/**/*.js",
      ],
      options: {
        jshintrc: ".jshintrc"
      }
    },
    inlinelint: {
      html: ["default/data/ui/html/**/*.html"]
    }
  });
  
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-lint-inline');

  grunt.registerTask('test', ['jshint','inlinelint']);
  grunt.registerTask('default', ['test']);
};

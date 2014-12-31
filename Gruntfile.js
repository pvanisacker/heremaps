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
    }
  });
  
  grunt.loadNpmTasks('grunt-contrib-jshint');

  grunt.registerTask('test', ['jshint']);
  grunt.registerTask('default', ['test']);
};

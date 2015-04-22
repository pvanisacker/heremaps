require.config({
    paths: {
        'heremapsjsCore' : 'https://js.api.here.com/v3/3.0/mapsjs-core',
        'heremapsjsService' : 'https://js.api.here.com/v3/3.0/mapsjs-service',
        'heremapsjsEvents' : 'https://js.api.here.com/v3/3.0/mapsjs-mapevents',
        'heremapsjsUi' : 'https://js.api.here.com/v3/3.0/mapsjs-ui',
        'heremapsjsClustering': 'https://js.api.here.com/v3/3.0/mapsjs-clustering',
        'heremapsjsData': 'https://js.api.here.com/v3/3.0/mapsjs-data',
        'heremapsjsCss':'https://js.api.here.com/v3/3.0/mapsjs-ui',
        'heremapcss':'../app/heremaps/heremaps/heremap',
        'app': '../app'
    },
    shim: {
        'heremapsjsService': {
          deps: ['heremapsjsCore']
        },
        'heremapsjsEvents': {
          deps: ['heremapsjsCore']
        },
        'heremapsjsUi': {
          deps: ['heremapsjsCore','css!heremapcss','css!heremapsjsCss']
        },
        'heremapsjsClustering': {
          deps: ['heremapsjsCore']
        },
        'heremapsjsData':{
          deps: ['heremapsjsCore']
        }
    }
});
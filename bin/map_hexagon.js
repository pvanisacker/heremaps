fs = require('fs');

function createHexagonGeometry(lng,lat,unit,resize){
    if(resize==undefined){
        resize=0;
    }
    var obj={ "type": "MultiPolygon", "coordinates": [ [ [ [lng,lat-resize],[lng-unit+resize,lat-unit],[lng-unit+resize,lat-(2*unit)],[lng,lat-(3*unit)+resize],[lng+unit-resize,lat-(2*unit)],[lng+unit-resize,lat-unit],[lng,lat-resize]]]]};
    return obj;
}
function createFeature(id,geometry){
    return { "type": "Feature", "properties": { "id": id }, "geometry": geometry};
}

var content_regeo='{"type": "FeatureCollection","features": [\r\n';
var content_display='{"type": "FeatureCollection","features": [\r\n';

var id=0
var rowcount=0
unit=2
resize=unit/5
for(var lat=-90;lat<=90;lat=lat+4*unit){
    for(var lng=-180;lng<=180;lng=lng+unit){
        if(rowcount%2==0){
            content_display+=JSON.stringify(createFeature(id.toString(),createHexagonGeometry(lng,lat,unit,resize)))+",\r\n"
            content_regeo+=JSON.stringify(createFeature(id.toString(),createHexagonGeometry(lng,lat,unit)))+",\r\n"
        }else{
            content_display+=JSON.stringify(createFeature(id.toString(),createHexagonGeometry(lng,lat-2*unit,unit,resize)))+",\r\n"
            content_regeo+=JSON.stringify(createFeature(id.toString(),createHexagonGeometry(lng,lat-2*unit,unit)))+",\r\n"
        }
        id++
        rowcount++
    }
    rowcount=0
}

content_display=content_display.slice(0,-3)
content_display+="\r\n]}";

content_regeo=content_regeo.slice(0,-3)
content_regeo+="\r\n]}";

fs.writeFile('../appserver/static/data/hexagonmap_regeo_'+unit+'.geojson', content_regeo, function (err) {
  if (err) throw err;
  console.log('It\'s saved!');
});
fs.writeFile('../appserver/static/data/hexagonmap_display_'+unit+'.geojson', content_display, function (err) {
  if (err) throw err;
  console.log('It\'s saved!');
});

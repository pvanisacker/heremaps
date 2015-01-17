fs = require('fs');

function createHexagonGeometry(lat,lng,unit){
    var obj={ "type": "MultiPolygon", "coordinates": [ [ [ [lat,lng],[lat-unit,lng-unit],[lat-unit,lng-(2*unit)],[lat,lng-(3*unit)],[lat+unit,lng-(2*unit)],[lat+unit,lng-unit],[lat,lng]]]]};
    return obj;
}
function createFeature(id,geometry){
    return { "type": "Feature", "properties": { "id": id }, "geometry": geometry};
}

var content='{"type": "FeatureCollection","features": [';

var id=0
for(var lat=0;lat<180;lat++){
    for(var lng=0;lng<90;lng++){
        content+=JSON.stringify(createFeature(id,createHexagonGeometry(lat,lng,1)))+",\r\n"
        id++
    }
}

content=content.substring(-5)
content+="\r\n]}";

fs.writeFile('../appserver/static/data/hexagonmap_1.geojson', content, function (err) {
  if (err) throw err;
  console.log('It\'s saved!');
});
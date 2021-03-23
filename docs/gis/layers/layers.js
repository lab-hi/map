var wms_layers = [];


        var lyr_OpenStreetMap_0 = new ol.layer.Tile({
            'title': 'OpenStreetMap',
            'type': 'base',
            'opacity': 0.700000,
            
            
            source: new ol.source.XYZ({
    attributions: ' ',
                url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
            })
        });
var lyr_1_modified_1 = new ol.layer.Image({
                            opacity: 1,
                            title: "1_modified",
                            
                            
                            source: new ol.source.ImageStatic({
                               url: "./layers/1_modified_1.png",
    attributions: ' ',
                                projection: 'EPSG:3857',
                                alwaysInRange: true,
                                imageExtent: [14244231.088067, 3122465.147436, 14513805.365465, 3352057.781480]
                            })
                        });

lyr_OpenStreetMap_0.setVisible(true);lyr_1_modified_1.setVisible(true);
var layersList = [lyr_OpenStreetMap_0,lyr_1_modified_1];

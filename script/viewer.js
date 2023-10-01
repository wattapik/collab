const viewer = OpenSeadragon({
     id: "viewer",
     showZoomControl: false,
     showHomeControl: false,
     showFullPageControl: false,
     showRotationControl: false
 });

viewer.smartScrollZoom({
    minScrolls: 1,
    timeThreshold: 0.01,
    zoomIncrement: 1000
});

viewer.viewport.minZoomLevel = 0.001;
viewer.viewport.maxZoomLevel = 2;
viewer.viewport.defaultZoomLevel = 0.05;
viewer.viewport.scrollHandlerSpeed = 1000;
viewer.drawer.context.imageSmoothingEnabled = false;
viewer.gestureSettingsMouse.clickToZoom = false;

viewer.viewport.goHome(true);

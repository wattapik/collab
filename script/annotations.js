const anno = OpenSeadragon.Annotorious(viewer);
anno.readOnly = true;
anno.escape = false;
anno.loadAnnotations('annotations/annotations.w3c.json');
let annotationText = ""



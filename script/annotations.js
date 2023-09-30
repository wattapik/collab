const anno = OpenSeadragon.Annotorious(viewer);
anno.readOnly = true;
anno.escape = false;
anno.loadAnnotations('annotations/annotations.w3c.json');
let annotationText = ""

function renderHTML()
{
    const observer = new MutationObserver(() => {
        const annotationTextElement = document.querySelector('.r6o-readonly-comment');
        if (annotationTextElement) {
            annotationTextElement.innerHTML = annotationText
            observer.disconnect();
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });
}

anno.on('clickAnnotation', function(annotation, element)
{
    annotationText = annotation.body[0].value
    renderHTML()
});

viewer.addHandler('update-viewport', function(event)
{
    renderHTML()
});


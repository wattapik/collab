const anno = OpenSeadragon.Annotorious(viewer);
anno.readOnly = true;
anno.loadAnnotations('annotations/annotations.w3c.json');

function sendMessageToServer(message) {
    return new Promise((resolve, reject) => {
        socket.addEventListener('message', (event) => {
            if (event.data.toString().length > 5) {
                let card = JSON.parse(event.data);
                resolve(card);
            } else {
                reject('Invalid response from server');
            }
        });

        socket.send(message);
    });
}

anno.on('clickAnnotation', async function(annotation) {
    let annotationValue = annotation.body[0].tag;

    let newAnnotation = annotation;
    newAnnotation.body[0].value = "🔁 Downloading label...";
    anno.updateSelected(newAnnotation);

    let response = await sendMessageToServer(annotationValue);

    let trueValueAnnotation = newAnnotation;

    let site = "https://sketchersunited.org";
    try {
        let post_id = response.post.id;
        let post_name = response.post.title;
        let poster_id = response.post.profile.id;
        let poster_name = response.post.profile.username;
        let poster_avatar = response.post.profile.profile_image_url_thumb;
        trueValueAnnotation.body[0].value = `<div class = "profile-container"><div class="profileimg"><img src = "${poster_avatar}"></div><div class="profile"><a href = "${site}/posts/${post_id}" class="rainbow">${post_name}</a><br><a href = "${site}/users/${poster_id}">@${poster_name}</a></div></div>`;
        anno.updateSelected(trueValueAnnotation);
    }
    catch (error) {
        try {
            let poster_id = response.data.id;
            let poster_name = response.data.username;
            let poster_avatar = response.data.profile_image_url.replace("small", "thumb");
            trueValueAnnotation.body[0].value = `<div class = "profile-container"><div class="profileimg"><img src = "${poster_avatar}"></div><div class="profile"><a href = "${site}/users/${poster_id}" class = "rainbow">@${poster_name}</a></div></div>`;
            anno.updateSelected(trueValueAnnotation);
        }
        catch (error) {
            console.log(`Post ${annotationValue} was dead: `, error);
            newAnnotation.body[0].value = "❌ An error occurred downloading the label.";
            anno.updateSelected(newAnnotation);
        }
    }


});

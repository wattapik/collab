let dictionaries = []
const imagePromises = [];
let image_count = 0

function load_image(image) {
    return new Promise((resolve, reject) => {
        viewer.addTiledImage({
            tileSource: image.tileSource,
            x: image.x,
            y: image.y,
            opacity: 1,
            success: () => {
                resolve();
            },
            error: (err) => {
                reject(err);
            },
        });
    });
}

fetch('image/image.txt')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(text => {
        const lines = text.split('\n');
        lines.forEach(line => {
            if (!line.startsWith('#') && line.length > 0) {
                const parts = line.split(' ');

                const dictionary = {
                    imageCount: image_count,
                    tileSource: 'image/dzi_edited/' + parts[0] + '/' + parts[0] + '.dzi',
                    x: parseInt(parts[1]),
                    y: parseInt(parts[2]),
                    red: parseInt(parts[3]),
                    green: parseInt(parts[4]),
                    blue: parseInt(parts[5]),
                };

                const promise = load_image(dictionary);

                dictionaries.push(dictionary);
                imagePromises.push(promise);
                image_count++;
            }
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });

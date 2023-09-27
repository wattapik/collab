let dictionaries = []
const imagePromises = [];
let image_count = 0

Caman.Store.put = function() {};

function load_image(image) {
    return new Promise((resolve, reject) => {
        viewer.addTiledImage({
            tileSource: image.tileSource,
            x: image.x,
            y: image.y,
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
            if (!line.startsWith('#')) {
                const parts = line.split(' ');

                const dictionary = {
                    imageCount: image_count,
                    tileSource: 'image/dzi/' + parts[0] + '/' + parts[0] + '.dzi',
                    x: parseInt(parts[1]),
                    y: parseInt(parts[2]),
                    red: parseInt(parts[3]),
                    blue: parseInt(parts[4]),
                    green: parseInt(parts[5])
                };

                const promise = load_image(dictionary);

                dictionaries.push(dictionary);
                imagePromises.push(promise);
                image_count++;
            }
        });
        return Promise.all(imagePromises);
    })
    .then(() => {
        let all_filters = []
        let all_nav_filters = []
        dictionaries.forEach(image => {
            let filter = {
                items: viewer.world.getItemAt(image.imageCount),
                processors: [
                    function (context, callback) {
                        Caman(context.canvas, function () {
                            this.colorize(image.red, image.green, image.blue, 50);
                            this.render(callback);
                        });
                    }
                    // },
                    // function (context, callback) {
                    //     Caman(context.canvas, function () {
                    //         this.contrast(10);
                    //         this.render(callback);
                    //     });
                    // }
                ]
            }

            let nav_filter = {
                items: viewer.navigator.world.getItemAt(image.imageCount),
                processors: [
                    function (context, callback) {
                        Caman(context.canvas, function () {
                            this.colorize(image.red, image.green, image.blue, 50);
                            this.render(callback);
                        });
                    }
                ]
            }

            all_filters.push(filter)
            all_nav_filters.push(nav_filter)
        });


        viewer.navigator.setFilterOptions = viewer.setFilterOptions;

        viewer.setFilterOptions({
            filters: all_filters
        });

        viewer.navigator.setFilterOptions({
            filters: all_nav_filters
        });



    })
    .catch(error => {
        console.error('Error:', error);
    });
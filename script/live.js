const clientCountElement = document.getElementById('clientCount');
const socket = new WebSocket('ws://localhost:8080/funsocket');

socket.addEventListener('message', (event) => {
    if(event.data.toString().length < 5) {
        const clientCount = parseInt(event.data);

        let append = " Sketchers"
        if (clientCount === 1) {
            clientCountElement.textContent = "Just you!";
        }
        else {
            clientCountElement.textContent = clientCount.toString() + append;
        }
    }
});
const clientCountElement = document.getElementById('clientCount');
const socket = new WebSocket('wss://sketchersunitedcollab.com/funsocket');

socket.addEventListener('message', (event) => {
    const clientCount = parseInt(event.data);
    let append = " people"
    if (clientCount === 1) {
        append = " person"
    }
    clientCountElement.textContent = clientCount.toString() + append;
});

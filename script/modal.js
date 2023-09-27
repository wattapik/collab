const modalOverlay = document.getElementById("modal-overlay");
const modal = document.getElementById("modal");
const openModalBtn = document.getElementById("open-button");
const closeModalBtn = document.getElementById("close-button");

openModalBtn.addEventListener("click", function () {
    modal.style.display = "block";
    modalOverlay.style.display = "block";

    setTimeout(() => {
        modal.style.opacity = "100";
    }, 10);
});

closeModalBtn.addEventListener("click", function () {
    modal.style.display = "none";
    modalOverlay.style.display = "none";

    setTimeout(() => {
        modal.style.opacity = "100";
    }, 300);
});

modalOverlay.addEventListener("click", function () {
    modal.style.display = "none";
    modalOverlay.style.display = "none";

    setTimeout(() => {
        modal.style.opacity = "0";
    }, 300);
});

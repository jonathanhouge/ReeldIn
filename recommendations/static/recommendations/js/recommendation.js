// Adapted from "How to Build a Modal with JavaScript" by Victor Eke
// https://www.freecodecamp.org/news/how-to-build-a-modal-with-javascript/

let modal = document.querySelector(".rec-modal");
let overlay = document.querySelector(".rec-overlay");
let openModalBtn = document.querySelector(".rec-btn-open");
let closeModalBtn = document.querySelector(".rec-btn-close");

// close modal function
let closeModal = function () {
  modal.classList.add("hidden");
  overlay.classList.add("hidden");
};

// close the modal when the close button and overlay is clicked
closeModalBtn.addEventListener("click", closeModal);
overlay.addEventListener("click", closeModal);

// close modal when the Esc key is pressed
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape" && !modal.classList.contains("hidden")) {
    closeModal();
  }
});

// open modal function
let openModal = function () {
  modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
};
// open modal event
openModalBtn.addEventListener("click", openModal);

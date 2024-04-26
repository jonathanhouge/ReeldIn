const recModal = document.querySelector(".rec-modal");
const recOverlay = document.querySelector(".rec-overlay");
const recOpenModalBtn = document.querySelector(".rec-btn-open");
const recCloseModalBtn = document.querySelector(".rec-btn-close");

// close modal function
const recCloseModal = function () {
  recModal.classList.add("hidden");
  recOverlay.classList.add("hidden");
};

// close the modal when the close button and overlay is clicked
recCloseModalBtn.addEventListener("click", recCloseModal);
recOverlay.addEventListener("click", recCloseModal);

// close modal when the Esc key is pressed
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape" && !modal.classList.contains("hidden")) {
    closeModal();
  }
});

// open modal function
const recOpenModal = function () {
  recModal.classList.remove("hidden");
  recOverlay.classList.remove("hidden");
};
// open modal event
recOpenModalBtn.addEventListener("click", recOpenModal);

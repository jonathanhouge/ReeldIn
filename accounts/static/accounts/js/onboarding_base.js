const exit_modal = document.getElementById("confirm_exit_modal");
const overlay = document.getElementById("exit_overlay");
console.log("HELLO");
function redirectToLandingPage() {
  window.location.href = "/";
}

function proceedToOnboardingGenreForm() {
  window.location.href = "genres";
}

function closeExitModal() {
  exit_modal.classList.add("hidden");
  overlay.classList.add("hidden");
}

function openExitModal() {
  exit_modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
}

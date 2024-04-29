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

/*Function from landing_page/js/index.js */
async function getCSRFToken() {
  try {
    const response = await fetch("/get-csrf-token/");
    const data = await response.json();
    const csrfToken = data.csrf_token;

    console.log("CSRF token fetched:", csrfToken);
    return csrfToken;
  } catch (error) {
    console.error("Error fetching CSRF token:", error);
    throw error; // Rethrow the error to propagate it
  }
}

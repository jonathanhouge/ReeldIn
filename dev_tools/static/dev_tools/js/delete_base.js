const overlay = document.getElementById("exit_overlay");
const home_modal = document.getElementById("home_modal");
const exit_modal = document.getElementById("confirm_exit_modal");

overlay.addEventListener("click", closeExitModal);

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

function closeExitModal() {
  exit_modal.classList.add("hidden");
  overlay.classList.add("hidden");
}

function openExitModal() {
  exit_modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
}

function openHomeModal() {
  home_modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
}

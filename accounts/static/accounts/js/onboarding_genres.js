function submitOnboardingGenreForm() {
  var form = document.getElementById("onboarding-form");
  form.action = "/accounts/onboarding/genres/";
  form.submit();
}

const exit_modal = document.getElementById("confirm_exit_modal");

function closeExitModal() {
  exit_modal.classList.add("hidden");
  overlay.classList.add("hidden");
}

function openExitModal() {
  exit_modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
}

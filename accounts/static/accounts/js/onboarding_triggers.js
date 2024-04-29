function redirectToOnboardingMovieForm() {
  window.location.href = "/accounts/onboarding/movies/";
}

function submitTriggerForm() {
  document.getElementById("onboarding-form").submit();
}

function openBackModal() {
  document.getElementById("confirm_back_modal").classList.remove("hidden");
  document.getElementById("exit_overlay").classList.remove("hidden");
}

function closeBackModal() {
  document.getElementById("confirm_back_modal").classList.add("hidden");
  document.getElementById("exit_overlay").classList.add("hidden");
}

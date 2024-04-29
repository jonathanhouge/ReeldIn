function submitOnboardingGenreForm() {
  var form = document.getElementById("onboarding-form");
  form.action = "/accounts/onboarding/genres/";
  form.submit();
}

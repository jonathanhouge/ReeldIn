function submitOnboardingGenreForm() {
  var form = document.getElementById("onboarding-form");
  form.action = "/onboarding/genres/";
  form.submit();
}

function redirectToLandingPage() {
    window.location.href = "/";
}

function submitOnboardingGenreForm(){
    var form = document.getElementById("onboarding-form");
    form.action = "/accounts/onboarding/genres/";
    form.submit();
}

function proceedToOnboardingGenreForm(){
    window.location.href = "genres";

}


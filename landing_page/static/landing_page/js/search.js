function loadDetailsPage(movie) {
    // movie = JSON.parse(jsonMovie);
    console.log(movie);
    window.location.href = window.location.origin + "/movie?movie=" + encodeURIComponent(JSON.stringify(movie));
}

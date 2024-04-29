// Buttons for the movie info page
// context change depending on button clicked, testing visuals
function movieOverview(movie_data) {
  console.log("movie_data: ", movie_data);
  streaming = JSON.parse(movie_data.watch_providers);

  if (streaming.length == 0) {
    streaming = "No streaming options available...";
  } else {
    streaming = streaming.join(", ");
  }

  

  document.getElementById(
    "movie_summary"
  ).innerHTML = `
      <div id="streaming_info">
      <p><strong>Description:</strong> </p>
      <p> ${movie_data.overview} </p>
      </div>
      <div id="streaming_info">
        <strong>Streaming:</strong> <p>${streaming}</p>
      </div>`;
}


function movieDetails(movie_data) {
  movie_genres = JSON.parse(movie_data.genres);
  movie_genres = movie_genres.join(", ");

  

  document.getElementById("movie_summary").innerHTML = `
  <div style="margin-top: 10px;">
    <p><strong>Release Year:</strong> ${movie_data.year} </p> </div>
  <div style="margin-top: 10px;">
    <p><strong>Runtime:</strong> ${movie_data.runtime} minutes</p> </div>
    <div style="margin-top: 10px;">
    <p><strong>Genres:</strong> ${movie_genres} </p> </div>
    <div style="margin-top: 10px;">
    <p><strong>Language:</strong> ${movie_data.language} </p> </div>`;
}

function moviePeople(movie_data) {
  movie_director = JSON.parse(movie_data.director);
  movie_director = movie_director.join(", ");
  if (!movie_director) movie_director = "No director found.";

  movie_starring = JSON.parse(movie_data.starring);
  movie_starring = movie_starring.join(", ");
  if (!movie_starring) movie_starring = "No actors found.";

  movie_writer = JSON.parse(movie_data.writer);
  movie_writer = movie_writer.join(", ");
  if (!movie_writer) movie_writer = "No writer found.";

  movie_composer = JSON.parse(movie_data.composer);
  movie_composer = movie_composer.join(", ");
  if (!movie_composer) movie_composer = "No composer found.";

  movie_cinematographer = JSON.parse(movie_data.cinematographer);
  movie_cinematographer = movie_cinematographer.join(", ");
  if (!movie_cinematographer)
    movie_cinematographer = "No cinematographer found.";

  document.getElementById(
    "movie_summary"
  ).innerHTML = `<p><strong>Director(s):</strong> ${movie_director}</p>
  <div style="margin-top: 10px;">
    <p><strong>Starring: </strong> ${movie_starring} </p> </div>
    <div style="margin-top: 10px;">
    <p><strong>Writer(s): </strong> ${movie_writer} </p> </div>
    <div style="margin-top: 10px;">
    <p><strong>Composer: </strong> ${movie_composer} </p> </div>
    <div style="margin-top: 10px;">
    <p><strong>Cinematographer: </strong> ${movie_cinematographer} </p> </div>
    `;
}

function openTooltip() {
  console.log("openTooltip");
  document.getElementById("tooltiptext").style.display = "block";
}

/**
 * This function updates the buttons with the state of the movie in the user's preferences.
 * It is called when the page is loaded.
 */
async function fetchPreferences(movie_id) {
  const csrfToken = await getCSRFToken();
  fetch("/accounts/preferences/movies/${movie_id}", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      if (data.liked) updateButton(movie_id, "_upvote", "green");
      else if (data.disliked) updateButton(movie_id, "_dislike", "red");

      if (data.watched) updateButton(movie_id, "_seen", "blue");
      else if (data.watchlist)
        updateButton(movie_id, "_watchlist", "cornflowerblue");

      if (data.rewatch) updateButton(movie_id, "_rewatch", "orange");
      if (movies_blocked.has(intID)) updateButton(movie_id, "_exclude", "red");
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
}

function updateButton(id, name, color) {
  document.getElementById(id + name).style.backgroundColor = color;
}

// Hides the tooltip when the user clicks outside of it
document.addEventListener("click", function (event) {
  var tooltiptext = document.getElementById("tooltiptext");
  if (!tooltiptext.contains(event.target)) {
    tooltiptext.style.display = "none";
  }
});

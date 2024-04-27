// Buttons for the movie info page
// context change depending on button clicked, testing visuals
function movieOverview(movie_data) {
  console.log("movie_data: ", movie_data);
  streaming = JSON.parse(movie_data.watch_providers);

  if (streaming.length == 0) {
    streaming = "No streaming options available...";
  } else {
    streaming = streaming.toString();
  }
  document.getElementById(
    "movie_summary"
  ).innerHTML = `<p><strong>Description:</strong> </p>
      <p> ${movie_data.overview} </p>
      <div id="streaming_info">
        <strong>Streaming:</strong> <p>${streaming}</p>
      </div>`;
}

function movieDetails(movie_data) {
  movie_director = JSON.parse(movie_data.director);
  movie_director = movie_director.toString();

  movie_genres = JSON.parse(movie_data.genres);
  movie_genres = movie_genres.toString();

  /* the movie_data has an language section, but is not added to views.py
  movie_language = JSON.parse(movie_data.language);
  movie_language = movie_language.toString(); */

  document.getElementById(
    "movie_summary"
  ).innerHTML = `<p><strong>Director(s):</strong> ${movie_director}</p>
  <div style="margin-top: 10px;">
    <p><strong>Movie Release Year:</strong> ${movie_data.year} </p>
  </div>
  <div style="margin-top: 10px;">
    <p><strong>Movie Runtime:</strong> ${movie_data.runtime} minutes</p>
    </div>
    <div style="margin-top: 10px;">
    <p><strong>Genres:</strong> ${movie_genres} </p> </div>
    <div style="margin-top: 10px;">
    <p><strong>Movie Language:</strong>  </p> </div>
    <div style="margin-top: 10px;">
    <p><strong>Movie MPAA Rating:</strong> ` + String(get_mpaa(movie_id, requests)) + 
    `</p> </div>`;
    
}

function moviePeople(movie_data) {
  movie_starring = JSON.parse(movie_data.starring);
  movie_starring = movie_starring.toString();

  document.getElementById("movie_summary").innerHTML = 
  `<div style="margin-top: 10px;">
    <p><strong>Movie Starring: </strong> ${movie_starring} </p> </div>`;
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

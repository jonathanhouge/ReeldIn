// Button colors
const likeGreen = getComputedStyle(document.documentElement).getPropertyValue(
  "--like-green"
);
const excludeRed = getComputedStyle(document.documentElement).getPropertyValue(
  "--exclude-red"
);
const rewatchOrange = getComputedStyle(
  document.documentElement
).getPropertyValue("--rewatch-orange");

// Page elements
const movieContainer = document.getElementById("movie_container");
const searchbar = document.getElementById("searchbar");
const tooltipBackgroundColor = "#9a8aff"; // Original tooltip button color

// Page variables
var currentTooltiptext = null; // Holds the last tooltip that was clicked on
var isLoading = false; // Prevents multiple movie fetches at once

// Page initialization
loadUserMovies();
fetchMovies(50);

// Debugging functions
function printStatus() {
  console.log("Movies Liked: ", movies_liked);
  console.log("Movies Disliked: ", movies_disliked);
  console.log("Movies Watched: ", movies_watched);
  console.log("Watchlist: ", watchlist);
  console.log("Movies Rewatch: ", movies_rewatch);
  console.log("Movies Blocked: ", movies_blocked);
}

/**
 * This class is used to create the div that holds a movie object.
 * Note that buttons aren't stylized with user preferences until they
 * are clicked on.
 * @param {Movie} movie the movie object to populate
 * @returns
 */
function createMovieDiv(movie) {
  var movieDiv = document.createElement("div");
  movieDiv.classList.add("movie", "tooltip");
  movieDiv.id = movie.id;
  movieDiv.onclick = function () {
    setToRemove(movie.id);
  };
  // Add tooltip content
  var tooltiptext = document.createElement("div");
  tooltiptext.classList.add("tooltiptext");
  tooltiptext.innerHTML = `
  <h3>Name: ${movie.name}</h3>
  <p>Year: ${movie.year}</p>
  <p>Genres: ${movie.genres}</p>
  <p>IMDb Info: ${movie.imdb_rating} / 10  |  ${movie.imdb_votes} votes</p>
  <p>Runtime: ${movie.runtime} minutes</p>
  <br>
  <p>Overview: ${movie.overview}</p>
  
  </div>`;
  movieDiv.appendChild(tooltiptext);
  var poster = document.createElement("img");
  poster.src = "https://image.tmdb.org/t/p/w300" + movie.poster;
  poster.loading = "lazy";
  poster.alt = movie.name;
  movieDiv.appendChild(poster);
  return movieDiv;
}

/**
 * This function reveals the tooltip along with adding the right styling
 * for the tooltip buttons.
 * @param {String} movie_id
 */
function revealDetails(movie_id) {
  if (currentTooltiptext) {
    currentTooltiptext.style.display = "none";
  }
  var tooltip = document.getElementById(movie_id);
  updateButtons(movie_id);

  currentTooltiptext = tooltip;
  currentTooltiptext.style.display = "block";
}

/**
 * This function updates the buttons with the state of the movie in the user's preferences.
 * It is called in the revealDetails function (which is called when the user clicks on a movie)
 * and whenever the user hovers over a movie
 */
function updateButtons(movie_id) {
  intID = parseInt(movie_id);
  if (movies_liked.has(intID)) {
    document.getElementById(movie_id + "_upvote").style.backgroundColor =
      likeGreen;
  } else if (movies_disliked.has(intID)) {
    document.getElementById(movie_id + "_dislike").style.backgroundColor =
      "red";
  }
  if (movies_watched.has(intID)) {
    document.getElementById(movie_id + "_seen").style.backgroundColor = "blue";
  } else if (watchlist.has(intID)) {
    document.getElementById(movie_id + "_watchlist").style.backgroundColor =
      "cornflowerblue";
  }
  if (movies_rewatch.has(intID)) {
    document.getElementById(movie_id + "_rewatch").style.backgroundColor =
      rewatchOrange;
  }
  if (movies_blocked.has(intID)) {
    document.getElementById(movie_id + "_exclude").style.backgroundColor =
      excludeRed;
  }
}

/* Repurposed code from landing_page/js/index.js */
async function searchMovies(event) {
  if (event.key != "Enter") {
    return;
  }

  searchString = searchbar.value.trim();

  if (searchString) {
    const csrfToken = await getCSRFToken();
    fetch("/accounts/onboarding/movies/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },

      body: JSON.stringify({ search: searchString, send_all: true }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        return response.json();
      })
      .then((data) => {
        movieContainer.innerHTML = "";
        data.movies.forEach((movie) => {
          var movieDiv = createMovieDiv(movie);
          movieContainer.appendChild(movieDiv);
        });
      });
  } else {
    movieContainer.innerHTML = ""; //TODO create new div to add response message ("Getting random movies...")
    fetchMovies(50);
  }
}

/**
 * Fetches random movies from the database and adds them to the movie container.
 * @param {int} numMovies the number of movies to fetch
 * @returns
 */
async function fetchMovies(numMovies = 35) {
  // Prevent multiple fetches at once
  if (isLoading) return;
  isLoading = true;

  try {
    const response = await fetch(
      `/accounts/onboarding/movies/random/${numMovies}/`
    );
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    data.movies.forEach((movie) => {
      var movieDiv = createMovieDiv(movie);
      console.log("Adding");
      movieContainer.appendChild(movieDiv);
    });
  } catch (error) {
    console.error("Error fetching movies:", error);
  } finally {
    isLoading = false;
  }
}

/**
 * This function is called when the user clicks the submit button on the onboarding page,
 * if the response is successful, the user is redirected to the triggers page.
 */
async function submitOnboardingMovieForm() {
  const csrfToken = await getCSRFToken();
  const data = {
    movies_liked: Array.from(movies_liked),
    movies_disliked: Array.from(movies_disliked),
    movies_watched: Array.from(movies_watched),
    watchlist: Array.from(watchlist),
    movies_rewatch: Array.from(movies_rewatch),
    movies_blocked: Array.from(movies_blocked),
  };

  fetch("/accounts/onboarding/movies/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      window.location.href = "/accounts/onboarding/triggers/";
    })
    .catch((error) => {
      console.error("Error submitting movie preferences:", error);
    });
}

/**
 * This function is called when the page loads, it populates the user data
 * sets so that the page may be styled accordingly based on current user preferences.
 */
async function loadUserMovies() {
  const csrfToken = await getCSRFToken();
  fetch("/accounts/preferences/movies/", {
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
      movies_liked = extractIds(data.movies_liked);
      movies_disliked = extractIds(data.movies_disliked);
      movies_watched = extractIds(data.movies_watched);
      watchlist = extractIds(data.watchlist);
      movies_rewatch = extractIds(data.movies_rewatch);
      movies_blocked = extractIds(data.movies_excluded);
    });
}

function extractIds(movieList) {
  return new Set(movieList.map((movie) => movie.pk));
}

// Random movie fetch when scrolling past halfway point
document.addEventListener("DOMContentLoaded", function () {
  movieContainer.addEventListener("scroll", () => {
    searchString = searchbar.value.trim();
    threshold = (movieContainer.scrollHeight * 3) / 5;
    console.log(
      "Scroll top: " + movieContainer.scrollTop + " Threshold: " + threshold
    );
    if (!searchString && movieContainer.scrollTop >= threshold) {
      console.log("Fetching more movies...");
      fetchMovies();
    }
  });
});

// Hides the tooltip when the user clicks outside of it
document.addEventListener("click", function (event) {
  if (currentTooltiptext && !currentTooltiptext.contains(event.target)) {
    currentTooltiptext.style.display = "none";
  }
});

/**
 * This function attempts to update the liked status of a movie.
 * @param {String} id the id of the movie to be updated
 */
function addLiked(id) {
  tooltip_message = document.getElementById(id + "_tooltip_message");
  tooltip_message.classList.add("hidden");

  liked_button = document.getElementById(id + "_upvote");
  intID = parseInt(id);

  if (movies_liked.has(intID)) {
    liked_button.style.backgroundColor = tooltipBackgroundColor;
    movies_liked.delete(intID);
    return;
  }

  if (movies_disliked.has(intID)) {
    disliked_button = document.getElementById(id + "_dislike");
    disliked_button.style.backgroundColor = tooltipBackgroundColor;
    movies_disliked.delete(intID);
  } else {
    watched_button = document.getElementById(id + "_seen");
    watched_button.style.backgroundColor = "blue";
    movies_watched.add(intID);
  }

  movies_liked.add(intID);
  liked_button.style.backgroundColor = likeGreen;
}

/**
 * This function attempts to update the dislike status of a movie.
 * @param {String} id the id of the movie to be updated
 */
function addDisliked(id) {
  tooltip_message = document.getElementById(id + "_tooltip_message");
  tooltip_message.classList.add("hidden");

  dislike_button = document.getElementById(id + "_dislike");
  intID = parseInt(id);

  if (movies_disliked.has(intID)) {
    dislike_button.style.backgroundColor = tooltipBackgroundColor;
    movies_disliked.delete(intID);
    return;
  }

  if (movies_liked.has(intID)) {
    liked_button = document.getElementById(id + "_upvote");
    liked_button.style.backgroundColor = tooltipBackgroundColor;
    movies_liked.delete(intID);
  } else {
    watched_button = document.getElementById(id + "_seen");
    watched_button.style.backgroundColor = "blue";
    movies_watched.add(intID);
  }

  movies_disliked.add(intID);
  dislike_button.style.backgroundColor = "red";
}

/**
 * This function attempts to update the watched status of a movie.
 * @param {String} id the id of the movie to be updated
 */
function addSeen(id) {
  tooltip_message = document.getElementById(id + "_tooltip_message");
  tooltip_message.classList.add("hidden");

  seen_button = document.getElementById(id + "_seen");
  intID = parseInt(id);

  if (movies_watched.has(intID)) {
    if (movies_liked.has(intID) || movies_disliked.has(intID)) {
      tooltip_message.classList.remove("hidden");
      tooltip_message.innerHTML =
        "Please remove your rating before marking a movie as un-watched.";

      return;
    }

    if (movies_rewatch.has(intID)) {
      rewatch_button = document.getElementById(id + "_rewatch");
      rewatch_button.style.backgroundColor = tooltipBackgroundColor;
      movies_rewatch.delete(intID);
    }

    seen_button.style.backgroundColor = tooltipBackgroundColor;
    movies_watched.delete(intID);
    return;
  }

  if (watchlist.has(intID)) {
    watchlist_button = document.getElementById(id + "_watchlist");
    watchlist_button.style.backgroundColor = tooltipBackgroundColor;
    watchlist.delete(intID);
  }

  seen_button.style.backgroundColor = "blue";
  movies_watched.add(intID);
}

/**
 * This function attempts to add a movie to the users watchlist.
 * @param {String} id the id of the movie to be updated
 */
function addWatchlist(id) {
  tooltip_message = document.getElementById(id + "_tooltip_message");
  tooltip_message.classList.add("hidden");

  watchlist_button = document.getElementById(id + "_watchlist");
  intID = parseInt(id);

  if (movies_watched.has(intID)) {
    tooltip_message = document.getElementById(id + "_tooltip_message");
    tooltip_message.classList.remove("hidden");
    tooltip_message.innerHTML =
      "You cannot add a movie you have seen to your watchlist, did you mean to select the rewatch button?";
    return;
  }

  if (movies_blocked.has(intID)) {
    tooltip_message = document.getElementById(id + "_tooltip_message");
    tooltip_message.innerHTML =
      "You cannot add a movie you have excluded from recommendations to your watchlist.";
    tooltip_message.classList.remove("hidden");
    return;
  }

  if (watchlist.has(intID)) {
    watchlist_button.style.backgroundColor = tooltipBackgroundColor;
    watchlist.delete(intID);
    return;
  }

  watchlist_button.style.backgroundColor = "cornflowerblue";
  watchlist.add(intID);
}

/**
 * This function attempts to update the rewatch status of a movie.
 * @param {String} id the id of the movie to be updated
 */
function addRewatch(id) {
  tooltip_message = document.getElementById(id + "_tooltip_message");
  tooltip_message.classList.add("hidden");

  rewatch_button = document.getElementById(id + "_rewatch");
  intID = parseInt(id);

  if (movies_blocked.has(intID)) {
    tooltip_message = document.getElementById(id + "_tooltip_message");
    tooltip_message.innerHTML =
      "You cannot rewatch a movie you have excluded from recommendations.";
    tooltip_message.classList.remove("hidden");
    return;
  }

  if (movies_rewatch.has(intID)) {
    rewatch_button.style.backgroundColor = tooltipBackgroundColor;
    movies_rewatch.delete(intID);
    return;
  }

  if (!movies_watched.has(intID)) {
    movies_watched.add(intID);
    rewatch_button.style.backgroundColor = rewatchOrange;
  }
  if (watchlist.has(intID)) {
    watchlist.delete(intID);
    watchlist_button = document.getElementById(id + "_watchlist");
    watchlist_button.style.backgroundColor = tooltipBackgroundColor;
  }

  rewatch_button.style.backgroundColor = rewatchOrange;
  movies_rewatch.add(intID);
}

/**
 * This function attempts to update the block status of a movie.
 * @param {String} id the id of the movie to be updated
 */
function addToExclude(id) {
  tooltip_message = document.getElementById(id + "_tooltip_message");
  tooltip_message.classList.add("hidden");

  exclude_button = document.getElementById(id + "_exclude");
  intID = parseInt(id);

  if (movies_blocked.has(intID)) {
    exclude_button.style.backgroundColor = tooltipBackgroundColor;
    movies_blocked.delete(intID);
    return;
  }

  if (watchlist.has(intID)) {
    watchlist_button = document.getElementById(id + "_watchlist");
    watchlist_button.style.backgroundColor = tooltipBackgroundColor;
    watchlist.delete(intID);
  } else if (movies_watched.has(intID)) {
    rewatch_button = document.getElementById(id + "_rewatch");
    rewatch_button.style.backgroundColor = tooltipBackgroundColor;
    movies_rewatch.delete(intID);
  }

  exclude_button.style.backgroundColor = excludeRed;
  movies_blocked.add(intID);
}

// Added movie removal code
var movies_to_remove = new Set(); // Set of all movies to be removed (may pop in and out of this list)
var movies_fetched = new Set(); // Set of all movies loaded via scrolling due to db sending random ones
const remove_movies_container = document.getElementById(
  "remove_movies_container"
);
const movie_scroll_container = document.getElementById("movie_container");

async function removeMovie() {
  const csrfToken = await getCSRFToken();
  //TODO
}

// Either adds movie to removedDiv or moves it back to pool (top)
function setToRemove(movie_id) {
  movieDiv = document.getElementById(movie_id);
  if (movies_to_remove.has(movie_id)) {
    movies_to_remove.delete(movie_id);
    movie_scroll_container.prepend(movieDiv);
  } else {
    movies_to_remove.add(movie_id);
    remove_movies_container.appendChild(movieDiv);
  }
}

function printRemoved() {
  text = "";
  for (let movie_id of movies_to_remove) {
    text += movie_id + "\n";
  }
  // Create a new Blob (file-like object of immutable, raw data) containing the text data
  const blob = new Blob([text], { type: "text/plain" });

  // Create a link element, use it to create a URL for our Blob, and set it as the link's href attribute
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "ids_to_remove.txt";

  // Append the link to the body, click it, and then remove it
  document.body.appendChild(a);
  a.click();

  URL.revokeObjectURL(a.href);
  document.body.removeChild(a);
}

// Usage example
downloadTextFile("This is the content of the file.", "debug-log.txt");

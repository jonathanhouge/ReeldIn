// Page elements
const movieContainer = document.getElementById("movie-container");
const searchbar = document.getElementById("searchbar");
const tooltipBackgroundColor = "#9a8aff"; // Original tooltip button color

// Page variables
var currentTooltiptext = null; // Holds the last tooltip that was clicked on
var isLoading = false; // Prevents multiple movie fetches at once

// Page initialization
loadUserMovies();
fetchMovies(50);

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
    setToRemove(movie.id, movie.name);
  };

  // Add tooltip content
  var tooltiptext = document.createElement("div");
  tooltiptext.classList.add("tooltiptext");
  tooltiptext.innerHTML = `
  <h3>Name: ${movie.name}</h3>
  <p>Year: ${movie.year}</p>
  <p>Genres: ${movie.genres}</p>
  <p>IMDb Info: ${Number(movie.imdb_rating).toFixed(1)}/10 |  ${
    movie.imdb_votes
  } votes</p>
  <p>Runtime: ${movie.runtime} minutes</p>
  <br>
  <p>Overview: ${movie.overview}</p>
  </div>`;

  var poster = document.createElement("img");
  poster.src = "https://image.tmdb.org/t/p/w300" + movie.poster;
  poster.loading = "lazy";
  poster.alt = movie.name;

  movieDiv.appendChild(tooltiptext);
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
          movie_dict[movie.id] = movie.name;
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
      if (movie.id in movie_dict) return;

      movie_dict[movie.id] = movie.name;
      var movieDiv = createMovieDiv(movie);
      movieContainer.appendChild(movieDiv);
    });
  } catch (error) {
    console.error("Error fetching movies:", error);
  } finally {
    isLoading = false;
  }
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

    if (!searchString && movieContainer.scrollTop >= threshold) {
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

// Movie removal code
var movie_dict = {}; // Dictionary of all movies loaded so far, key is movie_id and value is movie name

var movies_to_remove = new Set(); // Set of all movies to be removed (may pop in and out of this list)
var movies_fetched = new Set(); // Set of all movies loaded via scrolling due to db sending random ones
const removeMoviesContainer = document.getElementById(
  "remove-movies-container"
);
const movie_scroll_container = document.getElementById("movie-container");

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
    removeMoviesContainer.appendChild(movieDiv);
  }
}

function printRemoved() {
  text = "";
  for (let movie_id of movies_to_remove) {
    text += movie_id + "," + movie_dict[movie_id] + "\n";
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

async function deleteMovies() {
  printRemoved();

  const csrfToken = await getCSRFToken();
  var data = {
    movies_to_remove: Array.from(movies_to_remove),
  };

  fetch("/accounts/onboarding/delete/", {
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
      removeMoviesContainer.innerHTML = "";
      closeExitModal();
      return response.text();
    })
    .then((text) => {
      console.log(text);
    });
}

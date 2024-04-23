/**
 * These variables holds the data for the end movie preference POST request content,
 * and also aid in the process of making the site more interactive.
 */
var movies_liked = new Set();
var movies_disliked = new Set();
var movies_watched = new Set();
var watchlist = new Set();
var movies_rewatch = new Set();
var movies_blocked = new Set();

let isLoading = false; // Prevents multiple fetches at once
const movieContainer = document.getElementById("movie_container");
const searchbar = document.getElementById("searchbar");
var currentTooltiptext = null; // Holds the last tooltip that was clicked on

// TODO uncomment these lines when the page is loaded
//fetchMovies(50);
//loadUserMovies();

/*Function from landing_page/js/index.js */
async function getCSRFToken() {
  try {
    const response = await fetch("/get-csrf-token/");
    const data = await response.json();
    const csrfToken = data.csrf_token;

    return csrfToken;
  } catch (error) {
    console.error("Error fetching CSRF token:", error);
    throw error; // Rethrow the error to propagate it
  }
}

/**
 * This function is called when the page loads, it populates the
 * user data sets so that the page may be styled accordingly.
 */
async function loadUserMovies() {
  const csrfToken = await getCSRFToken();
  fetch("/accounts/preferences/movies", {
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
      console.log(data);
      movies_liked = new Set(data.movies_liked);
      movies_disliked = new Set(data.movies_disliked);
      movies_watched = new Set(data.movies_watched);
      watchlist = new Set(data.watchlist);
      movies_rewatch = new Set(data.movies_rewatch);
      movies_blocked = new Set(data.movies_blocked);
    });
}

/**
 * This class is used to create the div that holds a movie. It works by first
 * 1. Creating the div
 * 2. Adding the movie-specific info
 * 3. Adding the shell for user buttons (but doesn't style them until the user interacts with them)
 * @param {Movie} movie the movie object to populate
 * @returns
 */
function createMovieDiv(movie) {
  var movieDiv = document.createElement("div");
  movieDiv.classList.add("movie", "tooltip");
  movieDiv.onclick = function () {
    revealDetails(movie.id);
  };
  // Add tooltip content
  var tooltiptext = document.createElement("div");
  tooltiptext.classList.add("tooltiptext");
  tooltiptext.id = movie.id;
  tooltiptext.innerHTML = `
  <h3>${movie.name}</h3>
  <p>${movie.year}</p>
  <p class ="tooltip_message" id ="${movie.id}_tooltip_message"></p>
  <div class="tooltip_buttons">
    <div class="row1">
      <i class="fa-regular fa-2x fa-thumbs-up" id="${movie.id}_upvote" onclick="addLiked('${movie.id}')"></i>
      <i class="fa-regular fa-2x fa-thumbs-down" id="${movie.id}_dislike"onclick="addDisliked('${movie.id}')"></i>
    </div>
    <div class="row2">
      <i class="fa-regular fa-2x fa-eye" id="${movie.id}_seen" onclick="addSeen('${movie.id}')"></i>
      <i class="fa-solid fa-2x fa-plus" id = "${movie.id}_watchlist" onclick="addWatchlist('${movie.id}')"></i>
    </div>
    <div class="row3">
      <i class="fa-solid fa-2x fa-repeat" id = "${movie.id}_rewatch" onclick ="addRewatch('${movie.id}')"></i>
      <i class="fa-solid fa-2x fa-ban" id = "${movie.id}_exclude" onclick="addToExclude('${movie.id}')"></i>
    </div>
  </div>`;
  movieDiv.appendChild(tooltiptext);
  // Add poster
  var poster = document.createElement("img");
  poster.src = "https://image.tmdb.org/t/p/w300" + movie.poster;
  movieDiv.appendChild(poster);
  return movieDiv;
}

document.addEventListener("click", function (event) {
  if (currentTooltiptext && !currentTooltiptext.contains(event.target)) {
    currentTooltiptext.style.display = "none";
  }
});

/**
 * This function reveals the tooltip along with adding the right styling
 * for the tooltip buttons.
 * @param {*} movie_id
 */
function revealDetails(movie_id) {
  if (currentTooltiptext) {
    currentTooltiptext.style.display = "none";
  }
  console.log("Revealing details for movie: ", movie_id);
  var tooltip = document.getElementById(movie_id);
  // Add styling to the buttons
  if (movies_liked.has(movie_id)) {
    document.getElementById(movie_id + "_upvote").style.backgroundColor =
      "green";
  }
  if (movies_disliked.has(movie_id)) {
    document.getElementById(movie_id + "_dislike").style.backgroundColor =
      "red";
  }
  if (movies_watched.has(movie_id)) {
    document.getElementById(movie_id + "_seen").style.backgroundColor = "blue";
  }
  if (watchlist.has(movie_id)) {
    document.getElementById(movie_id + "_watchlist").style.backgroundColor =
      "cornflowerblue";
  }
  if (movies_rewatch.has(movie_id)) {
    document.getElementById(movie_id + "_rewatch").style.backgroundColor =
      "yellow";
  }
  if (movies_blocked.has(movie_id)) {
    document.getElementById(movie_id + "_exclude").style.backgroundColor =
      "black";
  }
  currentTooltiptext = tooltip;
  currentTooltiptext.style.display = "block";
}

/* Repurposed code from landing_page/js/index.js */
async function searchMovies(event) {
  if (event.key != "Enter") {
    return;
  }
  searchString = searchbar.value.trim();

  // Search movie if there is any string to be searched
  if (searchString) {
    const csrfToken = await getCSRFToken();
    fetch("/api/search/movies", {
      //TODO modify URL to new endpoint that returns ALL search movies instead of top 5
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
        console.log(data); //TODO delete this later
        movieContainer.innerHTML = "";
        // Iterate through results, adding them to the movie container
        data.movies.forEach((movie) => {
          console.log("Movie: ", movie);
          // First make the movie div
          var movieDiv = createMovieDiv(movie);
          movieContainer.appendChild(movieDiv);
        });
      });
  } else {
    // If the search bar is empty, clear the movie container and get random movies
    movieContainer.innerHTML = ""; //TODO create new div to add response message ("Getting random movies...")
    fetchMovies(50);
  }
}

/**
 * Fetches random movies from the database and adds them to the movie container.
 * @param {int} numMovies
 * @returns
 */
async function fetchMovies(numMovies = 35) {
  // Prevent multiple fetches at once
  if (isLoading) return;
  isLoading = true;

  try {
    // Fetch movies from the API
    const response = await fetch(`/api/movies/?amount=${numMovies}`);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    // Load JSON
    const data = await response.json();
    data.movies.forEach((movie) => {
      var movieDiv = createMovieDiv(movieDiv, movie);
      movieContainer.appendChild(movieDiv);
    });
  } catch (error) {
    console.error("Error fetching movies:", error);
  } finally {
    isLoading = false;
  }
}

// Allows movies to be fetched when the page is scrolled halfway
document.addEventListener("DOMContentLoaded", function () {
  movieContainer.addEventListener("scroll", () => {
    searchString = searchbar.value.trim();
    threshold = movieContainer.scrollHeight - movieContainer.clientHeight / 2;
    if (!searchString && movieContainer.scrollTop >= threshold) {
      fetchMovies();
    }
  });
});

/******************
 *  Functionality for user preferences
 */

/**
 * TODO test
 * @param {*} id
 * @returns
 */
function addLiked(id) {
  liked_button = document.getElementById(id + "_liked");

  if (movies_liked.has(id)) {
    // Unliking a movie
    liked_button.style.backgroundColor = "white";
    movies_liked.delete(id);
    return;
  } else if (movies_disliked.has(id)) {
    // Dislike -> Like
    disliked_button = document.getElementById(id + "_disliked");
    disliked_button.style.backgroundColor = "white";

    movies_disliked.delete(id);
    movies_liked.add(id);
  }
  liked_button.style.backgroundColor = "green";
}

/**
 * TODO test
 * @param {*} id
 * @returns
 */
function addDisliked(id) {
  disliked_button = document.getElementById(id + "_disliked");

  if (movies_disliked.has(id)) {
    // Un-dislike a movie
    disliked_button.style.backgroundColor = "white";
    movies_disliked.delete(id);
    return;
  } else if (movies_liked.has(id)) {
    // Like -> Dislike
    liked_button = document.getElementById(id + "_liked");
    liked_button.style.backgroundColor = "white";

    movies_liked.delete(id);
    movies_disliked.add(id);
  }
  disliked_button.style.backgroundColor = "red";
}

//TODO test
function addSeen(id) {
  seen_button = document.getElementById(id + "_seen");

  if (movies_watched.has(id)) {
    // First, check to see that the user has not liked/disliked the movie, as
    // rating a movie auto adds it to the watched list
    if (movies_liked.has(id) || movies_disliked.has(id)) {
      tooltip_message = document.getElementById(id + "_tooltip_message");
      tooltip_message.innerHTML =
        "Please remove your rating before marking a movie as un-watched.";
      return;
    }
    // Remove movie from seen
    seen_button.style.backgroundColor = "white";
    movies_watched.delete(id);
    return;
  }

  if (watchlist.has(id)) {
    // Remove movie from rewatch
    rewatch_button = document.getElementById(id + "_rewatch");
    rewatch_button.style.backgroundColor = "white";
    watchlist.delete(id);
  }
  // Add movie to seen
  seen_button.style.backgroundColor = "blue";
  movies_watched.add(id);
}

//TODO test

function addWatchlist(id) {
  watchlist_button = document.getElementById(id + "_watchlist");

  if (movies_watched.has(id)) {
    tooltip_message = document.getElementById(id + "_tooltip_message");
    tooltip_message.innerHTML =
      "You cannot add a movie you have seen to your watchlist, did you mean to select the rewatch button?";
    return;
  }

  if (watchlist.has(id)) {
    // Remove movie from watchlist
    watchlist_button.style.backgroundColor = "white";
    watchlist.delete(id);
    return;
  }

  // Add movie to watchlist
  watchlist_button.style.backgroundColor = "cornflowerblue";
  watchlist.add(id);
}

//TODO test
function addRewatch(id) {
  rewatch_button = document.getElementById(id + "_rewatch");

  if (!movies_watched.has(id)) {
    tooltip_message = document.getElementById(id + "_tooltip_message");
    tooltip_message.innerHTML = "You cannot rewatch a movie you have not seen.";
    return;
  }

  if (movies_rewatch.has(id)) {
    // Remove movie from rewatch
    rewatch_button.style.backgroundColor = "white";
    movies_rewatch.delete(id);
    return;
  }

  // Add movie to rewatch
  rewatch_button.style.backgroundColor = "yellow";
  movies_rewatch.add(id);
}

//TODO test
function addToExclude(id) {
  exclude_button = document.getElementById(id + "_exclude");

  if (movies_blocked.has(id)) {
    // Remove movie from exclude
    exclude_button.style.backgroundColor = "white";
    movies_blocked.delete(id);
    return;
  }

  if (watchlist.has(id)) {
    // Remove movie from watchlist
    watchlist_button = document.getElementById(id + "_watchlist");
    watchlist_button.style.backgroundColor = "white";
    watchlist.delete(id);
  }

  // Add movie to exclude
  exclude_button.style.backgroundColor = "black";
  movies_blocked.add(id);
}

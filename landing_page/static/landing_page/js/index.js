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

async function searchMovies(event) {
  searchBar = document.getElementById("searchbar");
  searchString = searchbar.value.trim();

  // Enter key
  if ((event.key === "Enter" || event.type === "click") && searchString) {
    // Route to search movies
    window.location.href =
      "/search/movies?query=" + encodeURIComponent(searchString);
  } else if (searchString) {
    const csrfToken = await getCSRFToken(); // Wait until getCSRFToken() resolves
    fetch("/api/search/movies/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({ search: searchString }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        moviesContainer = document.getElementById("searched-movies-container");
        moviesContainer.innerHTML = "";
        searchbar = document.getElementById("searchbar");
        searchbar.style.borderRadius = "12px 12px 0 0";

        data.movies.forEach((movie, index) => {
          // Create a new <div> element to display the movie details
          const movieDiv = document.createElement("div");
          movieDiv.classList.add("searched-movie");
          movieDiv.onclick = () => {
            window.location.href =
              window.location.origin + `/movie/${movie.id}`;
          };

          // Set the content of the movieDiv
          var img = document.createElement("img");
          img.classList.add("suggestions_img");

          img.id = `${movie.id}`;
          img.src = `https://image.tmdb.org/t/p/h100${movie.poster}`;

          var textDiv = document.createElement("div");
          textDiv.classList.add("searched-movie-details");

          var title = document.createElement("h3");
          title.innerHTML = `${movie.name}`;

          var release_date = document.createElement("p");
          release_date.innerHTML = `${movie.year}`;

          var starring = document.createElement("p");
          starring.innerHTML = `${movie.starring.slice(0, 2).join(", ")}`;

          textDiv.appendChild(title);
          textDiv.appendChild(release_date);
          textDiv.appendChild(starring);

          movieDiv.appendChild(img);
          movieDiv.appendChild(textDiv);

          // Check if it's the last iteration
          if (index === data.movies.length - 1) {
            movieDiv.classList.add("last-movie");
          }

          // Append the movieDiv to the moviesContainer
          moviesContainer.appendChild(movieDiv);
        });
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  } else {
    moviesContainer = document.getElementById("searched-movies-container");
    moviesContainer.innerHTML = "";

    searchbar = document.getElementById("searchbar");
    searchbar.style.borderRadius = "12px";
  }
}

function hideSearchResults() {
  moviesContainer = document.getElementById("searched-movies-container");
  moviesContainer.classList.add("hidden");

  searchbar = document.getElementById("searchbar");
  searchbar.style.borderRadius = "12px";
}

function showSearchResults() {
  moviesContainer = document.getElementById("searched-movies-container");
  moviesContainer.classList.remove("hidden");

  searchbar = document.getElementById("searchbar");

  if (searchbar.value.trim() !== "") {
    searchbar.style.borderRadius = "12px 12px 0 0";
  }
}

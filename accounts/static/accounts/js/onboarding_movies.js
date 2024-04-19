movies_liked = [];
movies_disliked = [];
movies_blocked = [];
movies_watched = [];
watchlist = [];
let isLoading = false;
const movieContainer = document.getElementById('movie_container');
const searchbar = document.getElementById("searchbar")

fetchMovies(50);

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

/* Repurposed code from landing_page/js/index.js */
async function searchMovies(event) {
    searchString = searchbar.value.trim()

    // Search movie if there is any string to be searched
    if (searchString) {
        const csrfToken = await getCSRFToken();
        fetch("/api/search/movies", { //TODO modify URL to new endpoint that returns ALL search movies instead of top 5
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ search: searchString })
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json()
        })
        .then((data) => {
            movieContainer.innerHTML = "";
            // Iterate through results, adding them to the movie container
            data.movies.forEach((movie, index) => {
                // First make the movie div
                const movieDiv = document.createElement('div');
                movieDiv.classList.add('movie');
                // Then make the image
                const img = document.createElement('img');
                img.classList.add('poster');
                img.src = `https://image.tmdb.org/t/p/w200${movie.poster}`;
                // Add the image to the movie div and add to container
                movieDiv.appendChild(img);
                movieContainer.appendChild(movieDiv);
            });
        })
    } else {
        // If the search bar is empty, clear the movie container and get random movies
        movieContainer.innerHTML = "";
        fetchMovies(50);
    }
}
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
        data.movies.forEach(movie => {
            const movieDiv = document.createElement('div');
            movieDiv.classList.add('movie');

            const img = document.createElement('img');
            img.classList.add('poster');
            img.src = `https://image.tmdb.org/t/p/w200${movie.poster}`;

            movieDiv.appendChild(img);
            movieContainer.appendChild(movieDiv);
        });
    } catch (error) {
        console.error("Error fetching movies:", error);
    } finally {
        isLoading = false;
    }
}

document.addEventListener("DOMContentLoaded", function() {
    searchString = searchbar.value.trim()
    movieContainer.addEventListener('scroll', () => {
        // Trigger halfway through the scrollable content
        if (!searchString && movieContainer.scrollTop >= (movieContainer.scrollHeight - movieContainer.clientHeight) / 2) {
            fetchMovies();  // Load more movies earlier in the scroll
        }
    });
});


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
    searchString = event.target.value.trim()

    // Enter key
    if (event.key === "Enter" && searchString) {
        // Route to search movies
        window.location.href = window.location.origin + "/search/movies?query=" + encodeURIComponent(searchString)
    } else if (event.key !== "Backspace" && searchString) {
        try {
            const csrfToken = await getCSRFToken(); // Wait until getCSRFToken() resolves
            const response = await fetch("/api/search/movies", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({ search: searchString })
            });
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            const data = await response.json();
            console.log(data)
        } catch (error) {
            console.error("Fetch error:", error);
        }
    }
}
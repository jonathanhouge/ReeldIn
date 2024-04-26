
// Buttons for the movie page's 
// context change depending on button clicked, testing visuals
function movieOverview(movie_name, movie_overview){
    document.getElementById("movie_summary").innerHTML = 
    `<p>Description of <strong>${movie_name}</strong> Movie: </p>
    <p> ${movie_overview} </p>`;
}
function movieDetails(movie_director, movie_year, movie_runtime, movie_genres1, movie_genres2, movie_genres3){
    document.getElementById("movie_summary").innerHTML = 
    `<p><strong>Director:</strong> ${movie_director}</p>
    <p><strong>Movie Release Year:</strong> ${movie_year} </p>
    <p><strong>Movie Runtime:</strong> ${movie_runtime} minutes</p>
    <p><strong>Genres:</strong> ${movie_genres1}, ${movie_genres2}, ${movie_genres3} </p>`;
}
// movie available to watch 
function movieWatching(){
    document.getElementById("movie_summary").innerHTML = 
    `<div>Streaming: 
    </div>
    <div>Buy: 
    </div>
    <div>Rent: 
    </div>
    `;
}
function movieOptions(){
    document.getElementById("movie_summary").innerHTML = 
    `<div>
    Movie Comments: 
    </div>
    <div>
    Movie Ratings:
    </div>
    `;
}
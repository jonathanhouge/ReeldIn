
// Buttons for the movie page's 
// context change depending on button clicked, testing visuals
function movieOverview(movie_name, movie_overview){
    document.getElementById("movie_summary").innerHTML = 
    `<p>Description of <strong>${movie_name}</strong> Movie: 
    ${movie_overview} </p>`;
}
function movieDetails(movie_director, movie_year, movie_runtime){
    document.getElementById("movie_summary").innerHTML = 
    `<p><strong>Director:</strong> ${movie_director}</p>
    <p><strong>Movie Release Year:</strong> ${movie_year} </p>
    <p><strong>Movie Runtime:</strong> ${movie_runtime} minutes</p>
    <p><strong>Genre(s):</strong> </p>`;
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
    Movie Comment(s): 
    </div>
    <div>
    Movie Rating(s):
    </div>
    `;
}
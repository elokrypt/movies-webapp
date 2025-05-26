function searchMovies(evt) {
    let textData = "";
    let filter = evt.target.value.toUpperCase();
    console.log(filter);
    let moviesGrid = document.getElementById("movies");
    let cells = moviesGrid.getElementsByClassName("cell");
    for (let i = 0; i < cells.length; i++) {
        textData = cells[i].textContent.trim().toUpperCase();
        if (textData.indexOf(filter) > -1) {
            cells[i].classList.remove("is-hidden");
        } else {
            cells[i].classList.add("is-hidden");
        }
    }
}

(function () {
    document.getElementById("search").addEventListener("keyup", searchMovies);
})();

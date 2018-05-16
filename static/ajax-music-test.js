function replaceMusic(results) {
    $("#music-text").innerHTML("hello");
}

function showMusic(evt) {
    $.get('/ajax/test-result', replaceMusic);
}

$('#get-music-button').on('click', showMusic);

function replaceFortune(results) {
    $("#music-text").innerHTML("hello");
}

function showFortune(evt) {
    $.get('/ajax/test-result', replaceFortune);
}

$('#get-music-button').on('click', showFortune);

$(document).ready(function(){
    $('.filter-button').click(function(){
        var filter = $(this).data('filter');
        var query = $("input[name='q']").val();
        window.location.href = "?q=" + query + "&filter=" + filter;
    });
    
    $('.song-item').click(function() {
        var songId = $(this).data('song-id');
        var songTitle = $(this).data('song-title');
        var songArtist = $(this).data('song-artist');
        var audioUrl = $(this).data('audio-url');

        $('#player-song-title').text(songTitle);
        $('#player-song-artist').text(songArtist);
        $('#player-bar').show();

        $('#player-play-button').data('audio', audioUrl).data('song-id', songId);
        $('#player-stop-button').data('audio', audioUrl);
    });

    var audioElement = new Audio();

    $('#player-play-button').click(function() {
        audioElement.src = $(this).data('audio');
        audioElement.play();
        // Increment play count via AJAX
        var incrementUrl = $('#increment-url-' + $(this).data('song-id')).val();
        $.post(incrementUrl, function(data) {
            console.log('Play count incremented.');
        });
    });

    $('#player-stop-button').click(function() {
        audioElement.pause();
        audioElement.currentTime = 0;
    });
});
    

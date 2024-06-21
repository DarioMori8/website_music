document.addEventListener('DOMContentLoaded', function () {
    let playedSongsCount = 0;

    function incrementPlaylistPlayCount() {
        const playlistId = document.getElementById('playlist-id').value;
        const incrementPlaylistUrl = `/increment_playlist_play_count/${playlistId}/`;
        const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        const csrfToken = csrfTokenElement.value;

        console.log('Sending played songs count:', playedSongsCount);
        
        fetch(incrementPlaylistUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ 'listened_songs_count': playedSongsCount })
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }).then(data => {
            console.log('Playlist play count incremented:', data);
            playedSongsCount = 0; 
        }).catch((error) => {
            console.error('Error:', error);
        });
    }

    document.addEventListener('playCountIncremented', function () {
        playedSongsCount++;
        console.log('Played songs count:', playedSongsCount); 
        if (playedSongsCount >= 3) {
            incrementPlaylistPlayCount();
        }
    });
});
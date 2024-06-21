$(document).ready(function() {

    function userAuthenticated(callback) {
        $.ajax({
            url: '/check_authentication/',
            type: 'GET',
            success: function(response) {
                if (response.authenticated) {
                    console.log('User is authenticated');  
                    callback(true);  
                } else {
                    callback(false);  
                }
            },
            error: function(xhr, status, error) {
                console.error('Error checking authentication status:', error);
                callback(false); 
            }
        });
    }

    function handleLoginUpdate() {
        userAuthenticated(function(authenticated) {
            if (authenticated) {
                console.log('Handling login update - user is authenticated');  
                loadUserPlaylists(); // Caricare le playlist dell'utente
            } 
        });
    }

    // Chiamare handleLoginUpdate all'avvio della pagina
    handleLoginUpdate();

    // Listener per l'evento di login completato
    $(document).on('loginSuccess', function() {
        console.log('Login success event triggered');  // Log dell'evento di login completato
        handleLoginUpdate();
    });

    // Toggle favorite song
    $('.favorite-button').click(function() {
        var button = $(this); // Salvare il riferimento al pulsante dei preferiti
        var songId = button.data('song-id');

        userAuthenticated(function(authenticated) {
            if (authenticated) {
                $.ajax({
                    url: '/toggle_favorite/' + songId + '/',
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': '{{ csrf_token }}'
                    },
                    success: function(response) {
                        if (response.is_favorite) {
                            button.find('i').addClass('favorite-heart');
                            addSongToFavoritesList(songId);
                        } else {
                            button.find('i').removeClass('favorite-heart');
                            removeSongFromFavoritesList(songId);
                        }
                    },
                    error: function(xhr, status, error) {
                        console.error('Error toggling favorite status:', error);
                    }
                });
            } else {
                showLoginPrompt();
            }
        });
    });

    // Check initial favorite status
    $('.favorite-button').each(function() {
        var button = $(this);
        var songId = button.data('song-id');
        userAuthenticated(function(authenticated) {
            if (authenticated) {
                $.ajax({
                    url: '/check_favorite/' + songId + '/',
                    success: function(response) {
                        if (response.is_favorite) {
                            button.find('i').addClass('favorite-heart');
                        }
                    },
                    error: function(xhr, status, error) {
                        console.error('Error checking favorite status:', error);
                    }
                });
            }
        });
    });

    function addSongToFavoritesList(songId) {
        var songDetails = $('#song-details-' + songId).clone();
        songDetails.attr('id', 'fav-song-details-' + songId);
        $('#favorite-songs-list').append(songDetails);
    }

    function removeSongFromFavoritesList(songId) {
        $('#fav-song-details-' + songId).remove();
    }

    function loadUserPlaylists() {
        userAuthenticated(function(authenticated) {
            if (authenticated) {
                $.ajax({
                    url: '/get_user_playlists/',
                    type: 'GET',
                    success: function(response) {
                        var dropdownMenu = $('.dropdown-menu');
                        dropdownMenu.empty();
                        if (response.playlists && response.playlists.length > 0) {
                            response.playlists.forEach(function(playlist) {
                                dropdownMenu.append(`<a class="dropdown-item" href="#" data-playlist-id="${playlist.id}">${playlist.name}</a>`);
                            });
                        }
                        dropdownMenu.append('<a class="dropdown-item" href="#" id="new-playlist">New Playlist</a>');
                    },
                    error: function(xhr, status, error) {
                        console.error('Error loading playlists:', error);
                    }
                });
            }
        });
    }

    // Function to add a song to the selected playlist
    function addToPlaylist(songId, playlistId) {
        $.ajax({
            url: `/add_to_playlist/${songId}/${playlistId}/`,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function(response) {
                if (response.message) {
                    alert(response.message);
                } else {
                    alert('Song added to playlist successfully!');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error adding song to playlist:', error);
            }
        });
    }

    // Handle click on add to playlist button
    $('.add-to-playlist-button').on('click', function(e) {
        var button = $(this);
        userAuthenticated(function(authenticated) {
            if (authenticated) {
                var songId = button.data('song-id');
                var dropdownMenu = button.next('.dropdown-menu');
                dropdownMenu.data('song-id', songId);  // Store song ID in the dropdown menu
                $('.dropdown-menu').not(dropdownMenu).hide();
                dropdownMenu.toggle();
                e.stopPropagation();
            } else {
                showLoginPrompt();
            }
        });
    });

    // Close dropdown when clicked outside
    $(document).on('click', function(e) {
        if (!$(e.target).closest('.add-to-playlist-button').length) {
            $('.dropdown-menu').hide();
        }
    });

    // Handle click on a playlist item
    $('.dropdown-menu').on('click', '.dropdown-item', function(e) {
        e.preventDefault();
        var item = $(this);
        userAuthenticated(function(authenticated) {
            if (authenticated) {
                var songId = item.closest('.dropdown-menu').data('song-id');  // Retrieve song ID from dropdown menu
                var playlistId = item.data('playlist-id');
                if (playlistId) {
                    addToPlaylist(songId, playlistId);
                } else {
                    // Handle creating a new playlist
                    alert('New Playlist feature not implemented yet');
                }
            } else {
                showLoginPrompt();
            }
        });
    });

    function showLoginPrompt() {
        alert('Please log in to perform this action.');
    }
});

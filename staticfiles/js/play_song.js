document.addEventListener('DOMContentLoaded', function () {
    const playButtons = document.querySelectorAll('.play-button');
    const stopButtons = document.querySelectorAll('.stop-button');
    let playTimeout;
    let currentAudio = null;
    let currentProgressBar = null;
    let currentTimeDisplay = null;
    let audioData = {}; // Oggetto per memorizzare i dati audio di ogni traccia

    function updatePlayCount(songId, incrementUrl, csrfToken) {
        const now = Date.now();
        const twoMinutes = 120000;

        const lastIncrementTime = localStorage.getItem(`lastIncrementTime_${songId}`);
        
        if (!lastIncrementTime || now - lastIncrementTime > twoMinutes) {
            localStorage.setItem(`lastIncrementTime_${songId}`, now);

            fetch(incrementUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ song_id: songId })
            }).then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            }).then(data => {
                console.log('Success:', data);
                const event = new CustomEvent('playCountIncremented', { detail: { songId: songId } });
                document.dispatchEvent(event);
            }).catch((error) => {
                console.error('Error:', error);
            });
        } else {
            console.debug(`Play count increment skipped for song ID ${songId}`);
        }
    }

    function formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    }

    function createAudio(url) {
        const audio = new Audio(url);
        audio.addEventListener('timeupdate', function() {
            if (audioData[url]) {
                audioData[url].currentTime = audio.currentTime;
                updateProgress(audio);
            }
        });
        return audio;
    }

    function stopCurrentAudio() {
        if (currentAudio && !currentAudio.paused) {
            currentAudio.pause();
            if (audioData[currentAudio.src]) {
                audioData[currentAudio.src].currentTime = currentAudio.currentTime;
            } else {
                audioData[currentAudio.src] = { currentTime: currentAudio.currentTime };
            }
            resetProgress();
        }
    }

    function updateProgress(audio) {
        if (currentProgressBar && currentTimeDisplay) {
            const percentage = (audio.currentTime / audio.duration) * 100;
            currentProgressBar.value = percentage;
            currentTimeDisplay.textContent = formatTime(audio.currentTime);
        }
    }

    function resetProgress() {
        if (currentProgressBar) {
            currentProgressBar.value = 0;
        }
        if (currentTimeDisplay) {
            currentTimeDisplay.textContent = '0:00';
        }
    }

    playButtons.forEach(button => {
        button.addEventListener('click', function() {
            const audioUrl = this.getAttribute('data-audio');
            const songId = this.getAttribute('data-song-id');
            const incrementUrlElement = document.querySelector(`#increment-url-${songId}`);
            const progressBar = document.querySelector(`#progress-bar-${songId}`);
            const currentTimeDisplayElement = document.querySelector(`#current-time-${songId}`);
    
            // Ferma l'audio corrente e reimposta il progresso
            stopCurrentAudio();
    
            if (!audioData[audioUrl]) {
                audioData[audioUrl] = { currentTime: 0 };
            }
    
            currentAudio = createAudio(audioUrl);
            currentProgressBar = progressBar;
            currentTimeDisplay = currentTimeDisplayElement;
    
            // Se l'audio è già in riproduzione, reimposta il tempo corrente a 0 e riparti dall'inizio
            if (!currentAudio.paused) {
                currentAudio.currentTime = 0;
            }
    
            // Aggiungi un gestore per l'evento di errore
            currentAudio.addEventListener('error', function(event) {
                console.error('Error playing audio:', event);
            });
    
            // Avvia la riproduzione solo se l'elemento audio è pronto
            if (currentAudio.readyState >= currentAudio.HAVE_ENOUGH_DATA) {
                currentAudio.play().then(() => {
                    console.debug(`Playing new audio for song ID ${songId}`);
                }).catch(error => {
                    console.error('Error playing audio:', error);
                });
            } else {
                // Aspetta il caricamento completo dell'elemento audio
                currentAudio.addEventListener('canplaythrough', function() {
                    currentAudio.play().then(() => {
                        console.debug(`Playing new audio for song ID ${songId}`);
                    }).catch(error => {
                        console.error('Error playing audio:', error);
                    });
                });
            }
    
            clearTimeout(playTimeout);
            playTimeout = setTimeout(() => {
                const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    
                if (csrfTokenElement) {
                    const csrfToken = csrfTokenElement.value;
    
                    console.debug(`CSRF Token found: ${csrfToken}`);
                    updatePlayCount(songId, incrementUrlElement.value, csrfToken);
                } else {
                    console.error('CSRF token not found.');
                }
            }, 10000);
    
            // Reimposta il tempo corrente dell'audio delle canzoni precedenti
            playButtons.forEach(otherButton => {
                if (otherButton !== button) {
                    const otherSongId = otherButton.getAttribute('data-song-id');
                    const otherAudioUrl = otherButton.getAttribute('data-audio');
                    if (audioData[otherAudioUrl]) {
                        audioData[otherAudioUrl].currentTime = 0;
                    }
                    const otherProgressBar = document.querySelector(`#progress-bar-${otherSongId}`);
                    const otherCurrentTimeDisplay = document.querySelector(`#current-time-${otherSongId}`);
                    if (otherProgressBar) {
                        otherProgressBar.value = 0;
                    }
                    if (otherCurrentTimeDisplay) {
                        otherCurrentTimeDisplay.textContent = '0:00';
                    }
                }
            });
        });
    });
    


    stopButtons.forEach(button => {
        button.addEventListener('click', function() {
            stopCurrentAudio();
        });
    });

    document.querySelectorAll('.progress-bar').forEach(progressBar => {
        progressBar.addEventListener('input', function() {
            if (currentAudio) {
                const newTime = (currentAudio.duration * progressBar.value) / 100;
                currentAudio.currentTime = newTime;
                updateProgress(currentAudio);
            }
        });
    });
});
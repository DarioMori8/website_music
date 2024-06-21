
var carousel = document.querySelector('#playlistCarousel');
var carouselInstance = new bootstrap.Carousel(carousel, {
    interval: false, // Disabilita lo scorrimento automatico
    wrap: false, // Disabilita il ciclo continuo
});

// Rendi le slide scorrevoli con il touch
carousel.addEventListener('touchstart', handleTouchStart, false);
carousel.addEventListener('touchmove', handleTouchMove, false);

var xDown = null;
var yDown = null;

function handleTouchStart(evt) {
    const firstTouch = evt.touches[0];
    xDown = firstTouch.clientX;
    yDown = firstTouch.clientY;
};

function handleTouchMove(evt) {
    if (!xDown || !yDown) {
        return;
    }

    var xUp = evt.touches[0].clientX;
    var yUp = evt.touches[0].clientY;
    var xDiff = xDown - xUp;
    var yDiff = yDown - yUp;

    if (Math.abs(xDiff) > Math.abs(yDiff)) { // Movimento orizzontale maggiore di quello verticale
        if (Math.abs(xDiff) > 10) { // Se il movimento orizzontale è significativo
            if (xDiff > 0) {
                carouselInstance.next(); // Scorri a destra
            } else {
                carouselInstance.prev(); // Scorri a sinistra
            }
        }
    }

    xDown = null; // Resetta le variabili per il prossimo touch
    yDown = null;
};



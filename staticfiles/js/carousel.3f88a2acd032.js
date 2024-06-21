
var carousel = document.querySelector('#playlistCarousel');
var carouselInstance = new bootstrap.Carousel(carousel, {
    interval: false, 
    wrap: false, 
});

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

    if (Math.abs(xDiff) > Math.abs(yDiff)) { 
        if (Math.abs(xDiff) > 10) { 
            if (xDiff > 0) {
                carouselInstance.next(); 
            } else {
                carouselInstance.prev(); 
            }
        }
    }

    xDown = null; 
    yDown = null;
};



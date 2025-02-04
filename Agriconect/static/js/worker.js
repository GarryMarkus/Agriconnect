// Typing effect for loader
const loaderText = document.getElementById('loader');
const welcomeMessage = "Welcome to Agriconnect";
let index = 0;

function type() {
    if (index < welcomeMessage.length) {
        loaderText.innerHTML += welcomeMessage.charAt(index);
        index++;
        setTimeout(type, 100);
    } else {
        setTimeout(() => {
            loaderText.style.display = 'none'; // Hide loader after typing
            document.querySelector('main').style.display = 'block'; // Show main content
        }, 500); // Delay before showing main content
    }
}

type();

// Image slider functionality
let currentIndex = 0;
const images = document.querySelectorAll('.slider img');

function showNextImage() {
    images[currentIndex].classList.remove('active'); // Remove active class from current image
    currentIndex = (currentIndex + 1) % images.length;
    images[currentIndex].classList.add('active'); // Add active class to next image
}

setInterval(showNextImage, 4000); // Change image every 4 seconds

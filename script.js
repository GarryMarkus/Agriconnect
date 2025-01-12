window.addEventListener('load', function() {
    const loader = document.querySelector('.loader');
    
    setTimeout(() => {
        loader.style.opacity = '0';
        setTimeout(() => {
            loader.style.display = 'none';
        }, 500);
    }, 3500); 
});


const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');
const body = document.body;

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navLinks.classList.toggle('active');
    body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : 'auto';
});

document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navLinks.classList.remove('active');
        body.style.overflow = 'auto';
    });
});

document.addEventListener('click', (e) => {
    if (!hamburger.contains(e.target) && 
        !navLinks.contains(e.target) && 
        navLinks.classList.contains('active')) {
        hamburger.classList.remove('active');
        navLinks.classList.remove('active');
        body.style.overflow = 'auto';
    }
});

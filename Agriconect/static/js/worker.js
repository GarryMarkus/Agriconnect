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


document.querySelectorAll('.start-button').forEach(button => {
    button.addEventListener('click', function() {
        const courseName = this.closest('.course-card').querySelector('.course-title').textContent;
        alert(`Enrolling in: ${courseName}`);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Handle close button click
    const closeButtons = document.querySelectorAll('.close-button');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const notification = this.closest('.notification');
            notification.style.opacity = '0';
            setTimeout(() => {
                notification.style.display = 'none';
            }, 300);
        });
    });

    // Handle mark all as read
    const markReadButton = document.querySelector('.mark-read');
    markReadButton.addEventListener('click', function(e) {
        e.preventDefault();
        const notifications = document.querySelectorAll('.notification');
        notifications.forEach(notification => {
            notification.style.borderLeftColor = '#ccc';
        });
        const badges = document.querySelectorAll('.notification-badge');
        badges.forEach(badge => {
            badge.style.backgroundColor = '#f0f0f0';
            badge.style.color = '#666';
        });
    });

    // Function to update notification descriptions
    function updateNotificationDescriptions() {
        
        const notifications = document.querySelectorAll('.notification');
        notifications.forEach(notification => {
            const notificationId = notification.getAttribute('data-id'); // Assuming each notification has a unique ID
            // Fetch new content from backend (this is a placeholder for actual fetch logic)
            fetch(`/api/notifications/${notificationId}`)
                .then(response => response.json())
                .then(data => {
                    const description = notification.querySelector('.notification-description');
                    description.textContent = data.description; 
                })
                .catch(error => console.error('Error fetching notification:', error));
        });
    }

    updateNotificationDescriptions();
});


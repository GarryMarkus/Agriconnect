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

document.addEventListener('DOMContentLoaded', function () {
    const notificationContainer = document.querySelector('.notifications-container');
    
    // Function to fetch and display notifications
    function fetchNotifications() {
        fetch('/notifications/')
            .then(response => response.json())
            .then(data => {
                notificationContainer.innerHTML = ''; // Clear previous notifications
                
                if (data.notifications.length === 0) {
                    notificationContainer.innerHTML = "<p>No new notifications</p>";
                    return;
                }

                data.notifications.forEach(notif => {
                    const notifElement = document.createElement('div');
                    notifElement.classList.add('notification');
                    notifElement.setAttribute('data-id', notif.id);
                    notifElement.innerHTML = `
                        <span class="notification-badge">${notif.type}</span>
                        <span class="notification-time">${notif.created_at}</span>
                        <button class="close-button">×</button>
                        <h2 class="notification-title">${notif.message}</h2>
                    `;
                    notificationContainer.appendChild(notifElement);
                });

                addCloseEventListeners();
            })
            .catch(error => console.error('Error fetching notifications:', error));
    }

    // Function to mark all notifications as read
    function markAllAsRead() {
        fetch('/mark_notifications_read/', { 
            method: 'POST', 
            credentials: 'same-origin' 
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                document.querySelectorAll('.notification').forEach(notif => notif.remove());
            }
        })
        .catch(error => console.error('Error marking notifications as read:', error));
    }

    // fOR CLOSE BUTTON
    function addCloseEventListeners() {
        document.querySelectorAll('.close-button').forEach(button => {
            button.addEventListener('click', function () {
                const notification = this.closest('.notification');
                notification.style.opacity = '0';
                setTimeout(() => {
                    notification.remove();
                }, 300);
            });
        });
    }

    // Event listener for "Mark all as read" button
    document.querySelector('.mark-read').addEventListener('click', function (e) {
        e.preventDefault();
        markAllAsRead();
    });
    fetchNotifications();
});


    // Navigation functionality
    const navLinks = document.querySelectorAll('.profile-nav a');
    const sections = document.querySelectorAll('.main-content section');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            
            // Update active states
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            sections.forEach(section => {
                section.classList.add('hidden');
                if (section.id === targetId) {
                    section.classList.remove('hidden');
                }
            });
        });
    });

    // Logout functionality
    // document.getElementById('logout-btn').addEventListener('click', () => {
    //     localStorage.removeItem('loggedInUser');
    //     window.location.href = 'index.html';
    // });

    // Personal info form submission
    // document.getElementById('personal-info-form').addEventListener('submit', (e) => {
    //     e.preventDefault();
        
    //     const updatedInfo = {
    //         studentMobile: document.getElementById('student-mobile').value,
    //         email: document.getElementById('email').value,
    //         room: document.getElementById('room').value
    //     };

    //     alert('Personal information updated successfully!');
    // });

    document.getElementById('password-form').addEventListener('submit', (e) => {
        e.preventDefault();
        // Add functionality to change password
        alert('Password updated successfully!');
    });

    // History tabs functionality
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            // Add functionality to load different history content
        });
    });
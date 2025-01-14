// Function to toggle fields based on user type
function toggleFields() {
    const userType = document.getElementById('userType').value;
    const aadharField = document.getElementById('aadharField');
    const gstField = document.getElementById('gstField');

    // Reset fields
    if (aadharField && gstField) {
        aadharField.classList.add('hidden');
        gstField.classList.add('hidden');
        
        // Reset required attribute
        document.getElementById('aadhar').required = false;
        document.getElementById('gst').required = false;

        if (userType === 'worker' || userType === 'provider') {
            aadharField.classList.remove('hidden');
            document.getElementById('aadhar').required = true;
        } else if (userType === 'buyer') {
            gstField.classList.remove('hidden');
            // GST is optional for retail buyers
        }
    }
}

// Call toggleFields when the page loads
document.addEventListener('DOMContentLoaded', function() {
    const userTypeSelect = document.getElementById('userType');
    if (userTypeSelect) {
        userTypeSelect.addEventListener('change', toggleFields);
        // Initialize fields based on default selection
        toggleFields();
    }
});

document.getElementById('registerForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Basic validation
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }

    // Get form data
    const formData = new FormData(this);
    const jsonData = {};
    
    // Convert FormData to JSON
    for (const [key, value] of formData.entries()) {
        jsonData[key] = value;
    }

    try {
        const response = await fetch('/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(jsonData)
        });

        const data = await response.json();
        console.log('Response:', data);

        if (data.status === 'success') {
            window.location.href = '/login/';
        } else {
            alert(data.message || 'Registration failed');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during registration');
    }
});

document.getElementById('loginForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const loginData = {
        userType: document.getElementById('userType').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };

    console.log('Login attempt:', loginData);
}); 
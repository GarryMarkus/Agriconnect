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

document.getElementById('registerForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Basic validation
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }

    const formData = {
        userType: document.getElementById('userType').value,
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        password: password
    };

    if (formData.userType === 'worker' || formData.userType === 'provider') {
        formData.aadhar = document.getElementById('aadhar').value;
    } else if (formData.userType === 'buyer') {
        formData.gst = document.getElementById('gst').value;
    }

    console.log('Registration data:', formData);
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
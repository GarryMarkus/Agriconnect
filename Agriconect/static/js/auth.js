
function toggleFields() {
    const userType = document.getElementById('userType').value;
    const aadharField = document.getElementById('aadharField');
    const gstField = document.getElementById('gstField');

   
    if (aadharField && gstField) {
        aadharField.classList.add('hidden');
        gstField.classList.add('hidden');
        
       
        document.getElementById('aadhar').required = false;
        document.getElementById('gst').required = false;

        if (userType === 'worker' || userType === 'provider') {
            aadharField.classList.remove('hidden');
            document.getElementById('aadhar').required = true;
        } else if (userType === 'buyer') {
            gstField.classList.remove('hidden');
       
        }
    }
}


document.addEventListener('DOMContentLoaded', function() {
    const userTypeSelect = document.getElementById('userType');
    if (userTypeSelect) {
        userTypeSelect.addEventListener('change', toggleFields);
        
        toggleFields();
    }
});

document.getElementById('registerForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    

    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }

    const formData = new FormData(this);
    const jsonData = {};
    

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
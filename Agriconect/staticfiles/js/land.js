document.addEventListener('DOMContentLoaded', function() {
    feather.replace();

    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            document.querySelectorAll('.nav-item').forEach(navItem => {
                navItem.classList.remove('active');
            });
            e.currentTarget.classList.add('active');
        });
    });

    initializeFormHandlers();
    initializeMessages();
});

function resetForm() {
    document.getElementById('landSubmissionForm').reset();
}

function viewLandDetails(landId) {
    console.log('Viewing land:', landId);
    // Add your view implementation here
}

function editLand(landId) {
    console.log('Editing land:', landId);
    // Add your edit implementation here
}

function handleFileUpload(event) {
    const files = event.target.files;
    const uploadedDocumentsContainer = document.getElementById('uploaded-documents');
    uploadedDocumentsContainer.innerHTML = '';
    Array.from(files).forEach(file => {
        const documentElement = createDocumentElement(file);
        uploadedDocumentsContainer.appendChild(documentElement);
    });
}

function createDocumentElement(file) {
    const documentElement = document.createElement('div');
    documentElement.classList.add('document-item');

    const fileName = document.createElement('span');
    fileName.textContent = file.name;

    const viewButton = document.createElement('button');
    viewButton.textContent = 'View';
    viewButton.onclick = () => viewDocument(file);

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.onclick = () => deleteDocument(documentElement);

    documentElement.append(fileName, viewButton, deleteButton);
    return documentElement;
}

function viewDocument(file) {
    const url = URL.createObjectURL(file);
    window.open(url);
}

function deleteDocument(documentElement) {
    documentElement.remove();
}

function redirectToForm() {
    document.querySelector('#submit-land').scrollIntoView({ 
        behavior: 'smooth' 
    });
}

function initializeFormHandlers() {
    const form = document.getElementById('landSubmissionForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }

    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', handleFileUpload);
    });
}

async function handleFormSubmit(event) {
    const form = event.target;
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value) {
            isValid = false;
            showError(field, 'This field is required');
        }
    });

    if (!isValid) {
        event.preventDefault();
    }
}

function showError(field, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    const existingError = field.parentElement.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    field.parentElement.appendChild(errorDiv);
    field.classList.add('error');
}

function initializeMessages() {
    const messages = document.querySelectorAll('.messages .alert');
    messages.forEach(message => {
        const closeButton = document.createElement('button');
        closeButton.innerHTML = '&times;';
        closeButton.className = 'close-message';
        closeButton.onclick = () => message.remove();
        message.appendChild(closeButton);
        setTimeout(() => message.remove(), 5000);
    });
}

function updateWeather(data) {
    const weatherCard = document.querySelector('.weather-card');
    if (weatherCard && data) {
        weatherCard.querySelector('.temperature').textContent = `${data.temperature}°C`;
        weatherCard.querySelector('.condition').textContent = data.condition;
        weatherCard.querySelector('.humidity .value').textContent = `${data.humidity}%`;
        weatherCard.querySelector('.wind .value').textContent = `${data.windSpeed} km/h`;
        weatherCard.querySelector('.rainfall .value').textContent = `${data.rainfall} mm`;
    }
}

function updateStatistics(data) {
    if (data) {
        const elements = {
            totalArea: document.querySelector('.stat-card .value[data-stat="total-area"]'),
            activePlots: document.querySelector('.stat-card .value[data-stat="active-plots"]'),
            pendingApprovals: document.querySelector('.stat-card .value[data-stat="pending-approvals"]'),
            monthlyRevenue: document.querySelector('.stat-card .value[data-stat="monthly-revenue"]')
        };

        for (const [key, element] of Object.entries(elements)) {
            if (element && data[key] !== undefined) {
                element.textContent = data[key];
            }
        }
    }
}

// Make functions available globally
window.resetForm = resetForm;
window.viewLandDetails = viewLandDetails;
window.editLand = editLand;
window.redirectToForm = redirectToForm;

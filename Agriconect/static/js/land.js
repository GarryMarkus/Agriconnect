// Initialize Feather Icons
feather.replace();

// Add click handlers for navigation
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', (e) => {
        // Remove active class from all items
        document.querySelectorAll('.nav-item').forEach(navItem => {
            navItem.classList.remove('active');
        });
        // Add active class to clicked item
        e.currentTarget.classList.add('active');
    });
});


function cancelForm() {
    
    const form = document.querySelector('.submit-land form');
    form.reset(); 
}
let totalLandArea = 0;
let activePlots = 0;
let pendingApprovals = 0;

// Function to handle file uploads
function handleFileUpload(event) {
    const files = event.target.files; // Get the uploaded files
    const uploadedDocumentsContainer = document.getElementById('uploaded-documents');

    // Clear previous documents
    uploadedDocumentsContainer.innerHTML = '';

    // Loop through the files and create elements for each
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const documentElement = document.createElement('div');
        documentElement.classList.add('document-item');

        // Create a span for the file name
        const fileName = document.createElement('span');
        fileName.textContent = file.name;

        // Create a view button
        const viewButton = document.createElement('button');
        viewButton.textContent = 'View';
        viewButton.onclick = function() {
            viewDocument(file);
        };

        // Create a delete button
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = function() {
            deleteDocument(documentElement);
        };

        // Append elements to the document item
        documentElement.appendChild(fileName);
        documentElement.appendChild(viewButton);
        documentElement.appendChild(deleteButton);

        // Append the document item to the container
        uploadedDocumentsContainer.appendChild(documentElement);
    }
}

// Function to handle form submission
async function handleFormSubmit(event) {
    event.preventDefault(); // Prevent the default form submission

    // Get the total area from the form input
    const totalAreaInput = document.getElementById('total-area');
    const totalArea = parseFloat(totalAreaInput.value) || 0;

    // Prepare the data to be sent as JSON
    const formData = {
        totalArea: totalArea,
        // Add other form fields as needed
    };

    try {
        // Simulate sending data to a server and receiving a JSON response
        const response = await simulateServerResponse(formData);
        
        // Process the JSON response
        updateStatistics(response);

        // Optionally, reset the form after submission
        const form = document.querySelector('.submit-land form');
        form.reset(); // Reset the form fields
    } catch (error) {
        console.error('Error submitting form:', error);
    }
}

// Simulate a server response
function simulateServerResponse(data) {
    return new Promise((resolve) => {
        setTimeout(() => {
            // Simulate a JSON response
            const response = {
                totalLandArea: data.totalArea, // Example response
                activePlots: 1, // Increment active plots
                pendingApprovals: 1 // Increment pending approvals
            };
            resolve(response);
        }, 1000); // Simulate a delay
    });
}

// Function to update statistics based on the JSON response
function updateStatistics(response) {
    // Update statistics
    totalLandArea += response.totalLandArea; // Add the total area from the response
    activePlots += response.activePlots; // Increment active plots
    pendingApprovals += response.pendingApprovals; // Increment pending approvals

    // Update the stats grid
    document.getElementById('total-land-area').textContent = totalLandArea.toFixed(2); // Update total land area
    document.getElementById('active-plots').textContent = activePlots; // Update active plots
    document.getElementById('pending-approvals').textContent = pendingApprovals; // Update pending approvals
}

// Function to view the document (for demonstration purposes)
function viewDocument(file) {
    const url = URL.createObjectURL(file);
    window.open(url); // Open the file in a new tab
}

// Function to delete the document
function deleteDocument(documentElement) {
    documentElement.remove(); // Remove the document element from the DOM
}

// Function to redirect to the form
function redirectToForm() {
    window.location.href = '#submit-land'; // Replace with the actual ID or URL of your form section
}

// Attach the form submit handler
document.querySelector('.submit-land form').addEventListener('submit', handleFormSubmit);
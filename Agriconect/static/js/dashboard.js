function showAssignmentModal(orderId) {
    document.getElementById('orderId').value = orderId;
    document.getElementById('assignmentModal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('assignmentModal').classList.add('hidden');
}

document.getElementById('assignmentForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const data = {
        order_id: document.getElementById('orderId').value,
        land_id: document.getElementById('landId').value,
        worker_id: document.getElementById('workerId').value
    };

    try {
        const response = await fetch('/admin-assign-land/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        if (result.status === 'success') {
            closeModal();
            location.reload();
        } else {
            alert(result.message);
        }
    } catch (error) {
        alert('Error assigning land and worker');
    }
});

async function completeAssignment(assignmentId) {
    if (!confirm('Are you sure you want to mark this assignment as complete?')) {
        return;
    }

    try {
        const response = await fetch(`/admin-complete-assignment/${assignmentId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        const result = await response.json();
        if (result.status === 'success') {
            location.reload();
        } else {
            alert(result.message);
        }
    } catch (error) {
        alert('Error completing assignment');
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
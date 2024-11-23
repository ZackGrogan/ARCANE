// Toast notification function
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();

    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

// HTMX after request handling
document.body.addEventListener('htmx:afterRequest', function(event) {
    if (event.detail.successful) {
        showToast('Action completed successfully', 'success');
    } else if (event.detail.failed) {
        showToast('Action failed. Please try again.', 'danger');
    }
});

// Initialize Bootstrap tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Handle form validation
document.addEventListener('submit', function(event) {
    if (!event.target.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
        showToast('Please check the form for errors', 'warning');
    }
    event.target.classList.add('was-validated');
});

// Persist dark mode preference
if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
} else {
    document.documentElement.classList.remove('dark');
}

// Listen for dark mode changes
window.addEventListener('dark-mode-toggle', function(e) {
    localStorage.theme = e.detail.darkMode ? 'dark' : 'light';
});

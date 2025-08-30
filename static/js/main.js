// Main JavaScript for Mental Health Prediction App

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initFormValidation();
    initSmoothScrolling();
    initAnimations();
    initTooltips();
    
    console.log('Mental Health Prediction App initialized');
});

// Form Validation
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Show first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
            form.classList.add('was-validated');
        });
    });
    
    // Real-time validation feedback
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.checkValidity()) {
                this.classList.add('is-valid');
                this.classList.remove('is-invalid');
            } else {
                this.classList.add('is-invalid');
                this.classList.remove('is-valid');
            }
        });
    });
}

// Smooth Scrolling (only for anchor links)
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Debug: Log all links on the page
    console.log('All links found:', document.querySelectorAll('a').length);
    document.querySelectorAll('a').forEach((link, index) => {
        console.log(`Link ${index + 1}: ${link.href} - ${link.textContent.trim()}`);
    });
}

// Animation on Scroll
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.feature-card, .step-card, .card').forEach(el => {
        observer.observe(el);
    });
}

// Initialize Tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Form Progress Indicator
function updateFormProgress() {
    const form = document.getElementById('predictionForm');
    if (!form) return;
    
    const requiredFields = form.querySelectorAll('[required]');
    const filledFields = Array.from(requiredFields).filter(field => field.value.trim() !== '');
    const progress = (filledFields.length / requiredFields.length) * 100;
    
    const progressBar = document.getElementById('formProgress');
    if (progressBar) {
        progressBar.style.width = progress + '%';
        progressBar.setAttribute('aria-valuenow', progress);
    }
}

// Age Input Enhancement
function setupAgeInput() {
    const ageInput = document.getElementById('age');
    if (ageInput) {
        ageInput.addEventListener('input', function() {
            const age = parseInt(this.value);
            const feedback = document.getElementById('ageFeedback');
            
            if (age < 18) {
                this.setCustomValidity('Age must be at least 18');
                if (feedback) feedback.textContent = 'Minimum age is 18 years';
            } else if (age > 80) {
                this.setCustomValidity('Age must be less than 80');
                if (feedback) feedback.textContent = 'Maximum age is 80 years';
            } else {
                this.setCustomValidity('');
                if (feedback) feedback.textContent = 'Valid age range';
            }
        });
    }
}

// Form Auto-save (to localStorage)
function initAutoSave() {
    const form = document.getElementById('predictionForm');
    if (!form) return;
    
    const formData = JSON.parse(localStorage.getItem('predictionFormData') || '{}');
    
    // Restore form data
    Object.keys(formData).forEach(key => {
        const field = form.querySelector(`[name="${key}"]`);
        if (field && formData[key]) {
            field.value = formData[key];
        }
    });
    
    // Save form data on input
    form.addEventListener('input', function(e) {
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        localStorage.setItem('predictionFormData', JSON.stringify(data));
    });
    
    // Clear saved data on successful submission
    form.addEventListener('submit', function() {
        if (form.checkValidity()) {
            localStorage.removeItem('predictionFormData');
        }
    });
}

// Error Handling
function handleError(error, userMessage = 'An error occurred') {
    console.error('Error:', error);
    
    // Show user-friendly error message
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${userMessage}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
    }
}

// API Helper Functions
async function makeAPICall(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        handleError(error, 'Failed to connect to the prediction service');
        throw error;
    }
}

// Form Enhancement for Better UX
function enhanceFormUX() {
    const form = document.getElementById('predictionForm');
    if (!form) return;
    
    // Add loading state to submit button
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
        form.addEventListener('submit', function() {
            submitBtn.innerHTML = `
                <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                Processing...
            `;
            submitBtn.disabled = true;
        });
    }
    
    // Add form section indicators
    const sections = document.querySelectorAll('.form-section');
    sections.forEach((section, index) => {
        const title = section.querySelector('.section-title');
        if (title) {
            const badge = document.createElement('span');
            badge.className = 'badge bg-secondary ms-2';
            badge.textContent = `${index + 1}/${sections.length}`;
            title.appendChild(badge);
        }
    });
}

// Initialize all enhancements when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    setupAgeInput();
    initAutoSave();
    enhanceFormUX();
    updateFormProgress();
    
    // Update progress on form changes
    const form = document.getElementById('predictionForm');
    if (form) {
        form.addEventListener('input', updateFormProgress);
    }
});

// Utility Functions
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove from DOM after hiding
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

// Performance monitoring
function trackPerformance() {
    if ('performance' in window) {
        window.addEventListener('load', function() {
            const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
            console.log(`Page load time: ${loadTime}ms`);
        });
    }
}

// Initialize performance tracking
trackPerformance();

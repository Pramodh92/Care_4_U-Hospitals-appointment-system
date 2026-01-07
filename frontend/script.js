// ============================================
// API CONFIGURATION
// ============================================

// Update this URL when deploying to EC2
// For local testing: http://localhost:5000
// For EC2: http://YOUR_EC2_PUBLIC_IP:5000
const API_BASE_URL = 'http://100.27.210.130:5000';

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Check if user is authenticated
 * @returns {boolean}
 */
function isAuthenticated() {
    return localStorage.getItem('user_id') !== null;
}

/**
 * Get current user data
 * @returns {Object|null}
 */
function getCurrentUser() {
    if (!isAuthenticated()) {
        return null;
    }

    return {
        user_id: localStorage.getItem('user_id'),
        name: localStorage.getItem('user_name'),
        email: localStorage.getItem('user_email')
    };
}

/**
 * Logout user and redirect to login page
 */
function logout() {
    localStorage.clear();
    window.location.href = 'index.html';
}

/**
 * Redirect to login if not authenticated
 */
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'index.html';
    }
}

/**
 * Format date to readable string
 * @param {string} dateString - Date in YYYY-MM-DD format
 * @returns {string}
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', options);
}

/**
 * Format time to 12-hour format
 * @param {string} timeString - Time in HH:MM format
 * @returns {string}
 */
function formatTime(timeString) {
    const [hours, minutes] = timeString.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
}

/**
 * Validate email format
 * @param {string} email
 * @returns {boolean}
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validate phone number (10 digits)
 * @param {string} phone
 * @returns {boolean}
 */
function isValidPhone(phone) {
    const phoneRegex = /^[0-9]{10}$/;
    return phoneRegex.test(phone);
}

/**
 * Show error message in a div
 * @param {string} elementId - ID of the error message div
 * @param {string} message - Error message to display
 */
function showError(elementId, message) {
    const errorDiv = document.getElementById(elementId);
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }
}

/**
 * Show success message in a div
 * @param {string} elementId - ID of the success message div
 * @param {string} message - Success message to display
 */
function showSuccess(elementId, message) {
    const successDiv = document.getElementById(elementId);
    if (successDiv) {
        successDiv.textContent = message;
        successDiv.style.display = 'block';
    }
}

/**
 * Clear all messages
 * @param {string[]} elementIds - Array of element IDs to clear
 */
function clearMessages(...elementIds) {
    elementIds.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = '';
            element.style.display = 'none';
        }
    });
}

// ============================================
// API HELPER FUNCTIONS
// ============================================

/**
 * Make API request
 * @param {string} endpoint - API endpoint
 * @param {string} method - HTTP method
 * @param {Object|null} data - Request body data
 * @returns {Promise<Object>}
 */
async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };

    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('API request error:', error);
        throw new Error('Unable to connect to server');
    }
}

/**
 * Signup user
 * @param {Object} userData - User data {name, email, phone, password}
 * @returns {Promise<Object>}
 */
async function signupUser(userData) {
    return await apiRequest('/signup', 'POST', userData);
}

/**
 * Login user
 * @param {string} email
 * @param {string} password
 * @returns {Promise<Object>}
 */
async function loginUser(email, password) {
    return await apiRequest('/login', 'POST', { email, password });
}

/**
 * Get all doctors
 * @returns {Promise<Object>}
 */
async function getDoctors() {
    return await apiRequest('/doctors', 'GET');
}

/**
 * Book appointment
 * @param {Object} appointmentData - {user_id, doctor_id, date, time}
 * @returns {Promise<Object>}
 */
async function bookAppointment(appointmentData) {
    return await apiRequest('/book-appointment', 'POST', appointmentData);
}

// ============================================
// INITIALIZATION
// ============================================

// Log API base URL for debugging
console.log('API Base URL:', API_BASE_URL);
console.log('Update API_BASE_URL in script.js when deploying to EC2');

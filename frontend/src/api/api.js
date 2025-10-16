// frontend/src/api/api.js
const API_BASE = 'http://localhost:8000/api';

// Helper function for API calls
async function apiCall(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` }),
            ...options.headers,
        },
        ...options,
    };

    if (config.body && typeof config.body === 'object') {
        config.body = JSON.stringify(config.body);
    }

    try {
        const FULL_URL = `${API_BASE}${endpoint}`;
        console.log('🚀 Making API call to:', FULL_URL);
        
        const response = await fetch(FULL_URL, config);
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || `HTTP error! status: ${response.status}`);
        }
        
        return response.json();
    } catch (error) {
        console.error('❌ API call failed:', error);
        throw error;
    }
}

// Auth API
export const authAPI = {
    login: (email, password) => 
        apiCall('/auth/login', {
            method: 'POST',
            body: { email, password }
        }),

    register: (name, email, password) => 
        apiCall('/auth/register', {
            method: 'POST',
            body: { name, email, password }
        }),
};

// Projects API
export const projectsAPI = {
    create: (projectData) => 
        apiCall('/projects/', {
            method: 'POST',
            body: projectData
        }),

    getAll: () => 
        apiCall('/projects/'),
};

// Chat API
export const chatAPI = {
    sendMessage: (projectId, message) => 
        apiCall('/chat/send', {
            method: 'POST',
            body: { project_id: projectId, message }
        }),
};

// Files API
export const filesAPI = {
    upload: (projectId, file) => 
        apiCall(`/files/${projectId}/upload`, {
            method: 'POST',
            body: file
        }),
};

export default apiCall;
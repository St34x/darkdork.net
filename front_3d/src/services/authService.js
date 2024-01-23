// src/services/authService.js
const login = async (username, password) => {
    try {
        const response = await fetch('http://localhost:5000/auth/login', {  // Replace with your Flask API URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
            credentials: 'include', // if using cookies for session management
        });
        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('Authenticated', data.authenticated);
            return data.user;
        } else {
            // Handle errors
            throw new Error(data.message || 'Login failed');
        }
    } catch (error) {
        throw error;
    }
};

export { login };


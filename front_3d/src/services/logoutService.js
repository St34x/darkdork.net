// authService.js
const logout = async () => {
    try {
        const response = await fetch('api/session/logout', 
            { 
                method: 'POST', 
                credentials: 'include'
            }
        );
        localStorage.removeItem('Authenticated');
        return response.json(); // or handle response as needed
    } catch (error) {
        console.error('Logout failed:', error);
    }
};

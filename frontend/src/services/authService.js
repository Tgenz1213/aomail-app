// authService.js

export function isUserAuthenticated() {
    const token = localStorage.getItem('userToken');
    return !!token; // returns true if the token exists, false otherwise
}

// You can also add other authentication-related functions here in the future.

// authService.js

export function isUserAuthenticated() {
    const token = localStorage.getItem('access_token');
    // returns true if the token exists, false otherwise
    return !!token;
}
import { fetchWithToken } from '../router/index.js';
import { API_BASE_URL } from '@/main';


export async function isUserAuthenticated() {
    // Checks if the user is authenticated. Returns true if authenticated, false otherwise.

    const access_token = localStorage.getItem('access_token');

    // Check if access token is still valid
    try {
        const requestOptions = {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${access_token}`
            },
        };
        let response = await fetch(`${API_BASE_URL}api/is_authenticated/`, requestOptions);

        if (response.status === 200) {
            // Check if email is in localStorage
            const email = localStorage.getItem('email');

            if (!email) {
                try {
                    const data = await fetchWithToken(`${API_BASE_URL}api/get_first_email/`);
                    localStorage.setItem('email', data.email);
                } catch (error) {
                    console.error("Error fetching email:", error);
                }
            }

            return true;
        } else {
            return false;
        }
    } catch (error) {
        console.error("Error checking authentication:", error);
        return false;
    }
}

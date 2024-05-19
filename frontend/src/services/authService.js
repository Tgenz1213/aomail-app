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
        let response = await fetchWithToken(`${API_BASE_URL}api/is_authenticated/`, requestOptions);

        if (response.isAuthenticated === true) {
            return true;
        } else {
            return false;
        }
    } catch (error) {
        console.error('Error isUserAuthenticated =====>', error);
        return false;
    }
}

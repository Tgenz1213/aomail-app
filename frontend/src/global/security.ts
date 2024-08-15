import router from "@/router/router";
import { API_BASE_URL, BASE_URL } from "./const";

interface AuthResponse {
    isAuthenticated: boolean;
}

interface RefreshTokenResponse {
    accessToken: string;
}

export async function isUserAuthenticated(): Promise<boolean> {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
        return false;
    }

    try {
        const requestOptions: RequestInit = {
            method: "GET",
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        };

        const response = await fetchWithToken(`${API_BASE_URL}api/is_authenticated/`, requestOptions);
        if (!response) {
            return false;
        }

        const data: AuthResponse = await response.json();
        return data.isAuthenticated === true;
    } catch (error) {
        return false;
    }
}

export async function fetchWithToken(url: string, options: RequestInit = {}): Promise<Response | void> {
    const accessToken = localStorage.getItem("accessToken");

    if (!options.headers) {
        options.headers = {};
    }

    if (accessToken) {
        (options.headers as Record<string, string>)["Authorization"] = `Bearer ${accessToken}`;
    } else {
        window.location.href = `${BASE_URL}`;
        return;
    }

    try {
        let response = await fetch(url, options);

        if (response.status === 401) {
            const refreshResponse = await fetch(`${API_BASE_URL}api/token/refresh/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ accessToken: accessToken }),
            });

            if (refreshResponse.ok) {
                const refreshData: RefreshTokenResponse = await refreshResponse.json();
                const newAccessToken = refreshData.accessToken;
                localStorage.setItem("accessToken", newAccessToken);
                (options.headers as Record<string, string>)["Authorization"] = `Bearer ${newAccessToken}`;
                response = await fetch(url, options);
            } else {
                router.push({ name: "not-authorized" });
            }
        }

        return response;
    } catch (error) {
        if (error instanceof Error) {
            console.error("An error occurred when fetching data from the API:", error.message);
        }
        return;
    }
}

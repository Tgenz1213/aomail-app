/* TODO:
// VERY IMPORTANT: for opti and scalabilty
// We MUST change fetchWithToken to return the complete result of the fetch
// it will allow to check the status code instead of if response.message == "aLongStringThatMayChange"
// EDIT: done => must change everywhere we use the function fetchWithToken

EXPORT redirection function after 5sec for 401 & 404 (if possible)
*/

import router from "@/router/router"
import { API_BASE_URL, BASE_URL } from "./const"

interface AuthResponse {
    isAuthenticated: boolean
}

interface RefreshTokenResponse {
    access_token: string
}

export async function isUserAuthenticated(): Promise<boolean> {
    const access_token = localStorage.getItem("access_token")
    if (!access_token) {
        return false
    }

    try {
        const requestOptions: RequestInit = {
            method: "GET",
            headers: {
                Authorization: `Bearer ${access_token}`,
            },
        }

        const response = await fetchWithToken(`${API_BASE_URL}api/is_authenticated/`, requestOptions)
        if (!response) {
            return false
        }

        const data: AuthResponse = await response.json()
        return data.isAuthenticated === true
    } catch (error) {
        return false
    }
}

export async function fetchWithToken(url: string, options: RequestInit = {}): Promise<Response | void> {
    const accessToken = localStorage.getItem("access_token")

    if (!options.headers) {
        options.headers = {}
    }

    if (accessToken) {
        (options.headers as Record<string, string>)["Authorization"] = `Bearer ${accessToken}`
    } else {
        window.location.href = `${BASE_URL}`
        return
    }

    try {
        let response = await fetch(url, options)

        if (response.status === 401) {
            const refreshResponse = await fetch(`${API_BASE_URL}api/token/refresh/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ access_token: accessToken }),
            })

            if (refreshResponse.ok) {
                const refreshData: RefreshTokenResponse = await refreshResponse.json()
                const newAccessToken = refreshData.access_token
                localStorage.setItem("access_token", newAccessToken)
                ;(options.headers as Record<string, string>)["Authorization"] = `Bearer ${newAccessToken}`
                response = await fetch(url, options)
            } else {
                router.push({ name: "not-authorized" })
            }
        }

        return response
    } catch (error) {
        if (error instanceof Error) {
            console.error("An error occurred when fetching data from the API:", error.message)
        }
        return
    }
}

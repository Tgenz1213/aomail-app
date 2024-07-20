/* TODO:
// VERY IMPORTANT: for opti and scalabilty
// We MUST change fetchWithToken to return the complete result of the fetch
// it will allow to check the status code instead of if response.message == "aLongStringThatMayChange"
// EDIT: done => must change everywhere we use the function fetchWithToken

EXPORT redirection function after 5sec
*/

import router from "@/router" // TODO: replace with the good import after refactor
import { API_BASE_URL, BASE_URL } from "./const"

export async function isUserAuthenticated() {
    const access_token = localStorage.getItem("access_token")
    try {
        const requestOptions = {
            method: "GET",
            headers: {
                Authorization: `Bearer ${access_token}`,
            },
        }
        let response = await fetchWithToken(`${API_BASE_URL}api/is_authenticated/`, requestOptions)
        const data = await response.json()

        if (data.isAuthenticated === true) {
            return true
        } else {
            return false
        }
    } catch (error) {
        return false
    }
}

export async function fetchWithToken(url: string, options: RequestInit = {}) {
    const accessToken = localStorage.getItem("access_token")

    if (!options.headers) {
        options.headers = {}
    }
    if (accessToken) {
        ;(options.headers as HeadersInit)["Authorization"] = `Bearer ${accessToken}`
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
                const refreshData = await refreshResponse.json()
                const newAccessToken = refreshData.access_token
                localStorage.setItem("access_token", newAccessToken)
                ;(options.headers as HeadersInit)["Authorization"] = `Bearer ${newAccessToken}`
                response = await fetch(url, options)
            } else {
                router.push({ name: "not-authorized" })
            }
        }

        return response
    } catch (error) {
        throw error
    }
}

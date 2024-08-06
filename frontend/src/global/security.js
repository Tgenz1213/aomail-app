/* TODO:
// VERY IMPORTANT: for opti and scalabilty
// We MUST change fetchWithToken to return the complete result of the fetch
// it will allow to check the status code instead of if response.message == "aLongStringThatMayChange"
// EDIT: done => must change everywhere we use the function fetchWithToken
*/

import router from "@/router/router.js"
import { API_BASE_URL, BASE_URL } from "./const.js"
import { ref } from "vue"

export function useRedirectCountdown(routeName, countdownTime = 5) {
    const countdown = ref(countdownTime)

    const updateCountdown = () => {
        countdown.value--

        if (countdown.value < 0) {
            router.push({ name: routeName })
        } else {
            setTimeout(updateCountdown, 1000)
        }
    }

    const startCountdown = () => {
        updateCountdown()
    }

    return {
        countdown,
        startCountdown,
    }
}

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

export async function fetchWithToken(url, options = {}) {
    const accessToken = localStorage.getItem("access_token")

    if (!options.headers) {
        options.headers = {}
    }
    if (accessToken) {
        options.headers["Authorization"] = `Bearer ${accessToken}`
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
                options.headers["Authorization"] = `Bearer ${newAccessToken}`
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

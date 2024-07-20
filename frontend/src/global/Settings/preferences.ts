import { API_BASE_URL } from "../const"
import { fetchWithToken } from "../security"

/*
TODO: export function to fetchUserPreference
+ create a function that return i18n object
*/
const fetchUserPreference = async (endpoint: string, key: string, allowedValues: Array<string>) => {
    const storedValue = localStorage.getItem(key)

    if (storedValue && allowedValues.includes(storedValue)) {
        return storedValue
    }

    const requestOptions = {
        headers: { "Content-Type": "application/json" },
        method: "GET",
    }

    try {
        const url = `${API_BASE_URL}${endpoint}`
        const response = await fetchWithToken(url, requestOptions)
        const data = await response.json()

        if (data.error) {
            return null
        } else if (response[key]) {
            localStorage.setItem(key, response[key])
            return response[key]
        }
    } catch (error) {
        console.log(error.message)
        return null
    }
}

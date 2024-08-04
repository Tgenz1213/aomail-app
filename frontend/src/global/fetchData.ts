I have these 2 funtions to get and post data to my API. Use them to refactor the script setup code.


import { API_BASE_URL } from "./const"
import { fetchWithToken } from "./security"

interface FetchDataResult {
    success: boolean
    data?: any
}

export async function getData(path: string): Promise<FetchDataResult> {
    const requestOptions = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    }

    try {
        const response = await fetchWithToken(`${API_BASE_URL}${path}`, requestOptions)

        if (!response) {
            return {
                success: false,
            }
        }

        const data = await response.json()

        return {
            success: true,
            data: data,
        }
    } catch (error: unknown) {
        return {
            success: false,
        }
    }
}

export async function postData(path: string, body: Record<string, any>): Promise<FetchDataResult> {
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    }

    try {
        const response = await fetchWithToken(`${API_BASE_URL}${path}`, requestOptions)

        if (!response) {
            return {
                success: false,
            }
        }

        const data = await response.json()

        return {
            success: true,
            data: data,
        }
    } catch {
        return {
            success: false,
        }
    }
}

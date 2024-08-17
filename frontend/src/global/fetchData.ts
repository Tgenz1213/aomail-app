import { API_BASE_URL } from "./const";
import { fetchWithToken } from "./security";
import { FetchDataResult } from "./types";

export async function getData(path: string, headers?: Record<string, string>): Promise<FetchDataResult> {
    const requestOptions = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            ...headers,
        },
    };

    try {
        const response = await fetchWithToken(`${API_BASE_URL}${path}`, requestOptions);

        if (!response) {
            return {
                success: false,
                error: "No server response",
            };
        }

        const data = await response.json();

        if (200 <= response.status && response.status <= 299) {
            return {
                success: true,
                data: data,
            };
        } else {
            return {
                success: false,
                error: data.error ? data.error : "",
            };
        }
    } catch (error) {
        return {
            success: false,
            error: error instanceof Error ? error.message : String(error),
        };
    }
}

export async function postData(path: string, body: Record<string, any>): Promise<FetchDataResult> {
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    };

    try {
        const response = await fetchWithToken(`${API_BASE_URL}${path}`, requestOptions);

        if (!response) {
            return {
                success: false,
                error: "No server response",
            };
        }

        const data = await response.json();
        if (200 <= response.status && response.status <= 299) {
            return {
                success: true,
                data: data,
            };
        } else {
            return {
                success: false,
                error: data.error ? data.error : "",
            };
        }
    } catch (error) {
        return {
            success: false,
            error: error instanceof Error ? error.message : String(error),
        };
    }
}

export async function deleteData(path: string, body?: any): Promise<FetchDataResult> {
    const requestOptions: RequestInit = {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        },
    };

    if (body) {
        requestOptions.body = JSON.stringify(body);
    }

    try {
        const response = await fetchWithToken(`${API_BASE_URL}${path}`, requestOptions);

        if (!response) {
            return {
                success: false,
                error: "No server response",
            };
        }

        const data = await response.json();

        if (200 <= response.status && response.status <= 299) {
            return {
                success: true,
                data: data,
            };
        } else {
            return {
                success: false,
                error: data.error ? data.error : "",
            };
        }
    } catch (error) {
        return {
            success: false,
            error: error instanceof Error ? error.message : String(error),
        };
    }
}

export async function putData(path: string, body: Record<string, any>): Promise<FetchDataResult> {
    const requestOptions = {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    };

    try {
        const response = await fetchWithToken(`${API_BASE_URL}${path}`, requestOptions);

        if (!response) {
            return {
                success: false,
                error: "No server response",
            };
        }

        const data = await response.json();

        if (200 <= response.status && response.status <= 299) {
            return {
                success: true,
                data: data,
            };
        } else {
            return {
                success: false,
                error: data.error ? data.error : "",
            };
        }
    } catch (error) {
        return {
            success: false,
            error: error instanceof Error ? error.message : String(error),
        };
    }
}

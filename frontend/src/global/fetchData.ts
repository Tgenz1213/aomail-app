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

    const response = await fetchWithToken(`${API_BASE_URL}${path}`, requestOptions);

    if (!response) {
        return {
            success: false,
            error: "No server response",
        };
    }

    const data = await response.json();

    if (response.ok) {
        return {
            success: true,
            data: data,
        };
    } else if (response.status === 403) {
        if (data.allowedPlans) {
            return {
                success: false,
                error: "Plan not allowed. Allowed plans: " + data.allowedPlans,
            };
        } else {
            return {
                success: false,
                error: "Subscription is inactive",
            };
        }
    } else {
        return {
            success: false,
            error: data.error ? data.error : "Unknown error",
        };
    }
}

export async function getDataRawResponse(
    path: string,
    headers?: Record<string, string>
): Promise<Response | FetchDataResult> {
    const requestOptions = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            ...headers,
        },
    };

    const response = await fetchWithToken(`${API_BASE_URL}${path}`, requestOptions);

    if (!response) {
        return {
            success: false,
            error: "No server response",
        };
    }

    if (response.ok) {
        return response;
    }

    const data = await response.json();

    if (response.status === 403) {
        if (data.allowedPlans) {
            return {
                success: false,
                error: "Plan not allowed. Allowed plans: " + data.allowedPlans,
            };
        } else {
            return {
                success: false,
                error: "Subscription is inactive",
            };
        }
    } else {
        return {
            success: false,
            error: data.error ? data.error : "Unknown error",
        };
    }
}


export async function postData(path: string, body: Record<string, any> | FormData, isFormData = false): Promise<FetchDataResult> {
    const requestOptions: RequestInit = {
        method: "POST",
        headers: !isFormData
            ? {
                "Content-Type": "application/json",
            }
            : {},
        body: isFormData ? body as FormData : JSON.stringify(body),
    };

    const response = await fetchWithToken(`${API_BASE_URL}${path}`, requestOptions);

    if (!response) {
        return {
            success: false,
            error: "No server response",
        };
    }

    const data = await response.json();

    if (response.ok) {
        return {
            success: true,
            data: data,
        };
    } else if (response.status === 403) {
        if (data.allowedPlans) {
            return {
                success: false,
                error: "Plan not allowed. Allowed plans: " + data.allowedPlans,
            };
        } else {
            return {
                success: false,
                error: "Subscription is inactive",
            };
        }
    } else {
        return {
            success: false,
            error: data.error ? data.error : "Unknown error",
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

    const response = await fetchWithToken(`${API_BASE_URL}${path}`, requestOptions);

    if (!response) {
        return {
            success: false,
            error: "No server response",
        };
    }

    const data = await response.json();

    if (response.ok) {
        return {
            success: true,
            data: data,
        };
    } else if (response.status === 403) {
        if (data.allowedPlans) {
            return {
                success: false,
                error: "Plan not allowed. Allowed plans: " + data.allowedPlans,
            };
        } else {
            return {
                success: false,
                error: "Subscription is inactive",
            };
        }
    } else {
        return {
            success: false,
            error: data.error ? data.error : "Unknown error",
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

    const response = await fetchWithToken(`${API_BASE_URL}${path}`, requestOptions);

    if (!response) {
        return {
            success: false,
            error: "No server response",
        };
    }

    const data = await response.json();

    if (response.ok) {
        return {
            success: true,
            data: data,
        };
    } else if (response.status === 403) {
        if (data.allowedPlans) {
            return {
                success: false,
                error: "Plan not allowed. Allowed plans: " + data.allowedPlans,
            };
        } else {
            return {
                success: false,
                error: "Subscription is inactive",
            };
        }
    } else {
        return {
            success: false,
            error: data.error ? data.error : "Unknown error",
        };
    }
}

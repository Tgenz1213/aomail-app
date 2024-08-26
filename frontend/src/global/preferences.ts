import { ALLOWED_LANGUAGES, ALLOWED_THEMES, API_BASE_URL, BASE_URL } from "./const";
import { fetchWithToken } from "./security";
import { ref } from "vue";
import { createI18n, I18n } from "vue-i18n";
import messages from "@/i18n";

type UserPreferenceResponse = {
    language?: string;
    theme?: string;
    timezone?: string;
    error?: string;
};

const fetchUserPreference = async (
    endpoint: string,
    key: keyof UserPreferenceResponse,
    allowedValues?: string[]
): Promise<string | null> => {
    const storedValue = localStorage.getItem(key);

    if (storedValue && allowedValues?.includes(storedValue)) {
        return storedValue;
    }

    const requestOptions: RequestInit = {
        headers: { "Content-Type": "application/json" },
        method: "GET",
    };

    try {
        const url = `${API_BASE_URL}${endpoint}`;
        const response = await fetchWithToken(url, requestOptions);

        if (!response || !(response instanceof Response)) {
            return null;
        }

        const data: UserPreferenceResponse = await response.json();

        if (data.error) {
            return null;
        } else if (data[key] !== undefined) {
            const value = data[key];
            if (typeof value === "string") {
                localStorage.setItem(key, value);
                return value;
            }
        }

        return null;
    } catch (error) {
        return null;
    }
};

export const initializePreferences = async (i18n: I18n) => {
    const currentUrl = window.location.href;

    if (
        currentUrl !== `${BASE_URL}` &&
        currentUrl !== `${BASE_URL}signup` &&
        currentUrl !== `${BASE_URL}signup_part2`
    ) {
        const language = await fetchUserPreference("user/preferences/language/", "language", [...ALLOWED_LANGUAGES]);
        if (language) {
            languageSelected.value = language;
            i18n.global.locale = language;
        }
        const theme = await fetchUserPreference("user/preferences/theme/", "theme", ALLOWED_THEMES);
        if (theme) {
            themeSelected.value = theme;
        }
        const timezone = await fetchUserPreference("user/preferences/timezone/", "timezone");
        if (timezone) {
            timezoneSelected.value = timezone;
        }
    }
};

export const languageSelected = ref("american");
export const themeSelected = ref("light");
export const timezoneSelected = ref("UTC");
export const i18n = createI18n({ legacy: true, locale: languageSelected.value, fallbackLocale: "american", messages });

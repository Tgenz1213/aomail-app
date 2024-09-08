import { ALLOWED_LANGUAGES, ALLOWED_THEMES, UNAUTHENTICATED_URLS } from "./const";
import { ref } from "vue";
import { createI18n, I18n } from "vue-i18n";
import messages from "@/i18n";
import { getData } from "./fetchData";

type UserPreferenceResponse = {
    language?: string;
    theme?: string;
    timezone?: string;
    error?: string;
};

const languageSelected = ref("american");
export const themeSelected = ref("light");
export const timezoneSelected = ref("UTC");

const fetchUserPreference = async (
    endpoint: string,
    key: keyof UserPreferenceResponse,
    allowedValues?: string[]
): Promise<string | null> => {
    const storedValue = localStorage.getItem(key);

    if (storedValue && allowedValues?.includes(storedValue)) {
        return storedValue;
    }

    const result = await getData(`${endpoint}`);

    if (!result.success) {
        return null;
    }

    if (result.data[key] !== undefined) {
        const value = result.data[key];
        if (typeof value === "string") {
            localStorage.setItem(key, value);
            return value;
        }
    }

    return null;
};

const isUnAuthenticatedUrl = (url: string) => {
    return UNAUTHENTICATED_URLS.some((baseUrl) => url === baseUrl);
};

export const initializePreferences = async (i18n: I18n) => {
    const currentUrl = window.location.href;

    if (!isUnAuthenticatedUrl(currentUrl)) {
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

export const i18n = createI18n({ legacy: true, locale: languageSelected.value, fallbackLocale: "american", messages });

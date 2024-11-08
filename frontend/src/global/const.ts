export const VERSION = "v 1.0.1"
export const BASE_URL = `https://${process.env.VUE_APP_ENV}.aomail.ai/`;
export const API_BASE_URL = `https://${process.env.VUE_APP_ENV}.aomail.ai/aomail/`;
export const MICROSOFT = "microsoft";
export const GOOGLE = "google";
export const YAHOO = "yahoo";
export const APPLE = "apple";
export const IMPORTANT = "important";
export const INFORMATIVE = "informative";
export const USELESS = "useless";
export const POP_UP_ERROR_COLOR = "bg-red-200/[.89] border border-red-400";
export const POP_UP_SUCCESS_COLOR = "bg-green-200/[.89] border border-green-400";
export const ALLOWED_THEMES = ["light", "dark"];
export const ALLOWED_LANGUAGES = ["french", "american", "german", "russian", "spanish", "chinese", "indian"] as const;
export type AllowedLanguageType = (typeof ALLOWED_LANGUAGES)[number];
export const UNAUTHENTICATED_URLS = [
    `${BASE_URL}`,
    `${BASE_URL}signup`,
    `${BASE_URL}signup-link`,
    `${BASE_URL}password-reset-link`,
    `${BASE_URL}reset-password-form`,
    `${BASE_URL}not-authorized`,
];
export const STRIPE_PUBLISHABLE_KEY =
    "pk_test_51Q9kHvK8H3QtVm1pWD1x67C6lQXl8D6EmD4vaEQowjTyrCbnbk0sJt3S4va5ErH7BEvJOuFlQMqxvuIHLshrc6zx00CUKTvZgX";
export const SUBSCRIPTION_MANAGEMENT_URL = "https://billing.stripe.com/p/login/test_9AQ6rvghmeKZ90Y288";

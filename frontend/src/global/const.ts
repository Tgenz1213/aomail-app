export const VERSION = "v 1.3";
export const BASE_URL = process.env.VUE_APP_BASE_URL;
export const API_BASE_URL = process.env.VUE_APP_API_BASE_URL;
export const MICROSOFT = "microsoft";
export const GOOGLE = "google";
export const YAHOO = "yahoo";
export const APPLE = "apple";
export const IMPORTANT = "important";
export const INFORMATIVE = "informative";
export const USELESS = "useless";
export const DEFAULT_CATEGORY = "Others";
export const ANSWER_REQUIRED = "Answer Required";
export const MIGHT_REQUIRE_ANSWER = "Might Require Answer";
export const NO_ANSWER_REQUIRED = "No Answer Required";
export const HIGHLY_RELEVANT = "Highly Relevant";
export const POSSIBLY_RELEVANT = "Possibly Relevant";
export const NOT_RELEVANT = "Not Relevant";
export const SPAM = "spam";
export const SCAM = "scam";
export const NEWSLETTER = "newsletter";
export const NOTIFICATION = "notification";
export const MEETING = "meeting";
export const POP_UP_ERROR_COLOR = "bg-red-200/[.89] border border-red-400";
export const POP_UP_SUCCESS_COLOR = "bg-green-200/[.89] border border-green-400";
export const AOMAIL_SEARCH_KEY = "aomail";
export const API_SEARCH_KEY = "api";
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
    "pk_live_51Q9kHvK8H3QtVm1poy56IRXxMg7VUycAoIz7v6WWS1RoupyTQjO1MvNt1o6H3xAHW9fylKUyEFbnJgB5KYhuKDra00ob4EvFBO";
export const SUBSCRIPTION_MANAGEMENT_URL = "https://billing.stripe.com/p/login/6oE9AK5iOe0ycs8fYY";

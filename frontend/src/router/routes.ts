import Login from "@/pages/Login/Login.vue";
import SignUp from "@/pages/Signup/SignUp.vue";
import SignupLink from "@/pages/Signup/SignUpLink.vue";
import AiAssistant from "@/pages/AiAssistant/AiAssistant.vue";
import Inbox from "@/pages/Inbox/Inbox.vue";
import New from "@/pages/New/New.vue";
import Answer from "@/pages/Answer/Answer.vue";
import Transfer from "@/pages/Transfer/Transfer.vue";
import Rules from "@/pages/Rules/Rules.vue";
import Settings from "@/pages/Settings/Settings.vue";
import Search from "@/pages/Search/Search.vue";
import ReplyLater from "@/pages/ReplyLater/ReplyLater.vue";
import NotFound from "@/pages/Errors/404NotFound.vue";
import NotAuthorized from "@/pages/Errors/401NotAuthorized.vue";
import PasswordResetLink from "@/pages/ResetPassword/PasswordResetLink.vue";
import ResetPasswordForm from "@/pages/ResetPassword/ResetPasswordForm.vue";
import { Component } from "vue";
import Labels from "@/pages/Labels/Labels.vue";
import Logout from "@/pages/Logout/Logout.vue";
import CustomCategorization from "@/pages/CustomCategorization/CustomCategorization.vue";
import Subscription from "@/pages/Subscription/Subscription.vue";
import Analytics from "@/pages/Analytics/Analytics.vue";

export interface RouteConfig {
    path: string;
    name: string;
    meta?: {
        requiresAuth?: boolean;
        allowInactive?: boolean;
    };
    component: Component;
}

const login: RouteConfig = {
    path: "/",
    name: "login",
    component: Login,
};

const logout: RouteConfig = {
    path: "/logout",
    name: "logout",
    meta: { requiresAuth: true },
    component: Logout,
};

const signUp: RouteConfig = {
    path: "/signup",
    name: "signup",
    component: SignUp,
};

const signUpLink: RouteConfig = {
    path: "/signup-link",
    name: "signupLink",
    component: SignupLink,
};

const aiAssistant: RouteConfig = {
    path: "/ai-assistant",
    name: "aiAssistant",
    meta: { requiresAuth: true },
    component: AiAssistant,
};

const inbox: RouteConfig = {
    path: "/inbox",
    name: "inbox",
    meta: { requiresAuth: true },
    component: Inbox,
};

const newRoute: RouteConfig = {
    path: "/new",
    name: "new",
    meta: { requiresAuth: true },
    component: New,
};

const answer: RouteConfig = {
    path: "/answer",
    name: "answer",
    meta: { requiresAuth: true },
    component: Answer,
};

const transfer: RouteConfig = {
    path: "/transfer",
    name: "transfer",
    meta: { requiresAuth: true },
    component: Transfer,
};

const search: RouteConfig = {
    path: "/search",
    name: "search",
    meta: { requiresAuth: true },
    component: Search,
};

const replyLater: RouteConfig = {
    path: "/reply-later",
    name: "reply-later",
    meta: { requiresAuth: true },
    component: ReplyLater,
};

const rules: RouteConfig = {
    path: "/rules",
    name: "rules",
    meta: { requiresAuth: true },
    component: Rules,
};

const settings: RouteConfig = {
    path: "/settings",
    name: "settings",
    meta: { requiresAuth: true, allowInactive: true },
    component: Settings,
};

const passwordResetLink: RouteConfig = {
    path: "/password-reset-link",
    name: "password-reset-link",
    component: PasswordResetLink,
};

const resetPasswordForm: RouteConfig = {
    path: "/reset-password-form",
    name: "reset-password-form",
    component: ResetPasswordForm,
};

const labels: RouteConfig = {
    path: "/labels",
    name: "labels",
    meta: { requiresAuth: true },
    component: Labels,
};

const customCategorization: RouteConfig = {
    path: "/custom-categorization",
    name: "customCategorization",
    meta: { requiresAuth: true },
    component: CustomCategorization,
};

const notAuthorized: RouteConfig = {
    path: "/not-authorized",
    name: "not-authorized",
    component: NotAuthorized,
};

const notFound: RouteConfig = {
    path: "/:catchAll(.*)",
    name: "not-found",
    component: NotFound,
};

const subscription: RouteConfig = {
    path: "/subscription",
    name: "subscription",
    meta: { requiresAuth: true, allowInactive: true },
    component: Subscription,
};

const analytics: RouteConfig = {
    path: "/analytics",
    name: "analytics",
    meta: { requiresAuth: true },
    component: Analytics,
};

const routes: RouteConfig[] = [
    login,
    logout,
    signUp,
    signUpLink,
    aiAssistant,
    inbox,
    newRoute,
    answer,
    transfer,
    search,
    replyLater,
    rules,
    settings,
    passwordResetLink,
    resetPasswordForm,
    labels,
    customCategorization,
    notAuthorized,
    notFound,
    subscription,
    analytics,
];

export default routes;

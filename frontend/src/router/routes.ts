import Login from "@/pages/Login/Login.vue";
import SignUp from "@/pages/Signup/SignUp.vue";
import SignupLink from "@/pages/Signup/SignUpLink.vue";
import Home from "@/pages/Home/Home.vue";
import New from "@/pages/New/New.vue";
import Answer from "@/pages/Answer/Answer.vue";
import Transfer from "@/pages/Transfer/Transfer.vue";
import Rules from "@/pages/Rules/Rules.vue";
import Settings from "@/pages/Settings/Settings.vue";
import StripePaymentFailed from "@/pages/Stripe/PaymentFailed.vue";
import StripePaymentSuccess from "@/pages/Stripe/PaymentSuccess.vue";
import Search from "@/pages/Search/Search.vue";
import ReplyLater from "@/pages/ReplyLater/ReplyLater.vue";
import NotFound from "@/pages/Errors/404NotFound.vue";
import NotAuthorized from "@/pages/Errors/401NotAuthorized.vue";
import PasswordResetLink from "@/pages/ResetPassword/PasswordResetLink.vue";
import ResetPasswordForm from "@/pages/ResetPassword/ResetPasswordForm.vue";
import { Component } from "vue";
import Labels from "@/pages/Labels/Labels.vue";

export interface RouteConfig {
    path: string;
    name: string;
    meta?: {
        requiresAuth?: boolean;
    };
    component: Component;
}

const login: RouteConfig = {
    path: "/",
    name: "login",
    component: Login,
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

const home: RouteConfig = {
    path: "/home",
    name: "home",
    meta: { requiresAuth: true },
    component: Home,
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
    meta: { requiresAuth: true },
    component: Settings,
};

const stripePaymentFailed: RouteConfig = {
    path: "/stripe/payment-failed/",
    name: "stripe-payment-failed",
    meta: { requiresAuth: true },
    component: StripePaymentFailed,
};

const stripePaymentSuccess: RouteConfig = {
    path: "/stripe/payment-successful/",
    name: "stripe-payment-successful",
    meta: { requiresAuth: true },
    component: StripePaymentSuccess,
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

const routes: RouteConfig[] = [
    login,
    signUp,
    signUpLink,
    home,
    newRoute,
    answer,
    transfer,
    search,
    replyLater,
    rules,
    settings,
    stripePaymentFailed,
    stripePaymentSuccess,
    passwordResetLink,
    resetPasswordForm,
    labels,
    notAuthorized,
    notFound,
];

export default routes;

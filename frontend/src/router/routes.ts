// TODO: REPLACE with good imports
import Login from "@/views/UserLogin.vue"
import SignUp from "@/views/SignUpV1.vue"
import SignupLink from "@/pages/Signup/SignUpLink.vue"
import Home from "@/views/HomeV15.vue"
import New from "@/views/NewV4.vue"
import Answer from "@/views/AnswerV1.vue"
import Transfer from "@/views/TransferV1.vue"
import Rules from "@/views/RulesV2.vue"
import Settings from "@/views/SettingsV1.vue"
import StripePaymentFailed from "@/pages/Stripe/StripePaymentFailed.vue"
import StripePaymentSuccess from "@/pages/Stripe/StripePaymentSuccess.vue"
import Search from "@/views/SearchV2.vue"
import ReplyLater from "@/views/ReplyLaterV1.vue"
import NotFound from "@/views/404NotFound.vue"
import NotAuthorized from "@/views/401NotAuthorized.vue"
import PasswordResetLink from "@/views/PasswordResetLink.vue"
import ResetPasswordForm from "@/views/ResetPasswordForm.vue"

export const login = {
    path: "/",
    name: "login",
    component: Login,
}

export const signUp = {
    path: "/signup",
    name: "signup",
    component: SignUp,
}

export const signUpLink = {
    path: "/signup_part2", // TODO: (only Augustin & Théo): rename as signup-link (but not now because we also need to change in Google Project & Azure)
    name: "signupLink",
    component: SignupLink,
}

export const home = {
    path: "/home",
    name: "home",
    meta: { requiresAuth: true },
    component: Home,
}

export const newRoute = {
    path: "/new",
    name: "new",
    meta: { requiresAuth: true },
    component: New,
}

export const answer = {
    path: "/answer",
    name: "answer",
    meta: { requiresAuth: true },
    component: Answer,
}

export const transfer = {
    path: "/transfer",
    name: "transfer",
    meta: { requiresAuth: true },
    component: Transfer,
}

export const search = {
    path: "/search",
    name: "search",
    meta: { requiresAuth: true },
    component: Search,
}

export const replyLater = {
    path: "/reply-later",
    name: "reply-later",
    meta: { requiresAuth: true },
    component: ReplyLater,
}

export const rules = {
    path: "/rules",
    name: "rules",
    meta: { requiresAuth: true },
    component: Rules,
}

export const settings = {
    path: "/settings",
    name: "settings",
    meta: { requiresAuth: true },
    component: Settings,
}

export const stripePaymentFailed = {
    path: "/stripe/payment-failed/",
    name: "stripe-payment-failed",
    meta: { requiresAuth: true },
    component: StripePaymentFailed,
}

export const stripePaymentSuccess = {
    path: "/stripe/payment-successful/",
    name: "stripe-payment-successful",
    meta: { requiresAuth: true },
    component: StripePaymentSuccess,
}

export const passwordResetLink = {
    path: "/password-reset-link",
    name: "password-reset-link",
    component: PasswordResetLink,
}

export const resetPasswordForm = {
    path: "/reset-password-form",
    name: "reset-password-form",
    component: ResetPasswordForm,
}

export const notAuthorized = {
    path: "/not-authorized",
    name: "not-authorized",
    component: NotAuthorized,
}

export const notFound = {
    path: "/:catchAll(.*)",
    name: "not-found",
    component: NotFound,
}

const routes = [
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
    notAuthorized,
    notFound,
]

export default routes

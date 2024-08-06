import Login from "@/pages/Login/Login.vue"
import SignUp from "@/pages/Signup/SignUp.vue"
import SignupLink from "@/pages/Signup/SignUpLink.vue"
import Home from "@/pages/Home/Home.vue"
import New from "@/pages/New/New.vue"
import Answer from "@/pages/Answer/Answer.vue"
import Transfer from "@/pages/Transfer/Transfer.vue"
import Rules from "@/pages/Rules/Rules.vue"
import Settings from "@/pages/Settings/Settings.vue"
import StripePaymentFailed from "@/pages/Stripe/StripePaymentFailed.vue"
import StripePaymentSuccess from "@/pages/Stripe/StripePaymentSuccess.vue"
import Search from "@/pages/Search/Search.vue"
import ReplyLater from "@/pages/ReplyLater/ReplyLater.vue"
import NotFound from "@/pages/Errors/404NotFound.vue"
import NotAuthorized from "@/pages/Errors/401NotAuthorized.vue"
import PasswordResetLink from "@/pages/ResetPassword/PasswordResetLink.vue"
import ResetPasswordForm from "@/pages/ResetPassword/ResetPasswordForm.vue"

const login = {
    path: "/",
    name: "login",
    component: Login,
}

const signUp = {
    path: "/signup",
    name: "signup",
    component: SignUp,
}

const signUpLink = {
    path: "/signup_part2", // TODO: (only Augustin & Théo): rename as signup-link (but not now because we also need to change in Google Project & Azure)
    name: "signupLink",
    component: SignupLink,
}

const home = {
    path: "/home",
    name: "home",
    meta: { requiresAuth: true },
    component: Home,
}

const newRoute = {
    path: "/new",
    name: "new",
    meta: { requiresAuth: true },
    component: New,
}

const answer = {
    path: "/answer",
    name: "answer",
    meta: { requiresAuth: true },
    component: Answer,
}

const transfer = {
    path: "/transfer",
    name: "transfer",
    meta: { requiresAuth: true },
    component: Transfer,
}

const search = {
    path: "/search",
    name: "search",
    meta: { requiresAuth: true },
    component: Search,
}

const replyLater = {
    path: "/reply-later",
    name: "reply-later",
    meta: { requiresAuth: true },
    component: ReplyLater,
}

const rules = {
    path: "/rules",
    name: "rules",
    meta: { requiresAuth: true },
    component: Rules,
}

const settings = {
    path: "/settings",
    name: "settings",
    meta: { requiresAuth: true },
    component: Settings,
}

const stripePaymentFailed = {
    path: "/stripe/payment-failed/",
    name: "stripe-payment-failed",
    meta: { requiresAuth: true },
    component: StripePaymentFailed,
}

const stripePaymentSuccess = {
    path: "/stripe/payment-successful/",
    name: "stripe-payment-successful",
    meta: { requiresAuth: true },
    component: StripePaymentSuccess,
}

const passwordResetLink = {
    path: "/password-reset-link",
    name: "password-reset-link",
    component: PasswordResetLink,
}

const resetPasswordForm = {
    path: "/reset-password-form",
    name: "reset-password-form",
    component: ResetPasswordForm,
}

const notAuthorized = {
    path: "/not-authorized",
    name: "not-authorized",
    component: NotAuthorized,
}

const notFound = {
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

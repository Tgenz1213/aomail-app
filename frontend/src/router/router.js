import { createRouter, createWebHistory } from "vue-router"
import { isUserAuthenticated } from "@/global/security.ts"
import routes from "./routes.ts"

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach(async (to, _, next) => {
    try {
        if (to.matched.some((record) => record.meta.requiresAuth)) {
            const isAuthenticated = await isUserAuthenticated()
            if (!isAuthenticated) {
                next({ name: "not-authorized" })
            } else {
                next()
            }
        } else {
            next()
        }
    } catch (error) {
        next({ name: "login" })
    }
})

export default router

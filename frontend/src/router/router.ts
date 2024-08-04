import { createRouter, createWebHistory, RouteLocationNormalized, NavigationGuardNext } from "vue-router";
import routes from "./routes";
import { isUserAuthenticated } from "@/global/security";

const router = createRouter({
    history: createWebHistory(),
    routes: routes,
});

router.beforeEach(async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
    try {
        const requiresAuth = (to.meta as { requiresAuth?: boolean }).requiresAuth;
        if (requiresAuth) {
            const isAuthenticated = await isUserAuthenticated();
            if (!isAuthenticated) {
                next({ name: "not-authorized" });
            } else {
                next();
            }
        } else {
            next();
        }
    } catch (error) {
        next({ name: "login" });
    }
});

export default router;

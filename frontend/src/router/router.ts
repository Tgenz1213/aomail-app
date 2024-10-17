import { createRouter, createWebHistory, RouteLocationNormalized, NavigationGuardNext } from "vue-router";
import routes from "./routes";
import { isUserAuthenticated } from "@/global/security";

const router = createRouter({
    history: createWebHistory(),
    routes: routes,
});

router.beforeEach(async (to: RouteLocationNormalized, _from: RouteLocationNormalized, next: NavigationGuardNext) => {
    try {
        const requiresAuth = (to.meta as { requiresAuth?: boolean }).requiresAuth;
        if (requiresAuth) {
            const authCheck = await isUserAuthenticated();

            if (!authCheck || typeof authCheck !== "object" || !authCheck.isAuthenticated) {
                next({ name: "not-authorized" });
                return;
            }

            if (!authCheck.isActive && to.meta.allowInactive) {
                next();
                return;
            }

            if (!authCheck.isActive) {
                next({ name: "settings" });
                return;
            }

            next();
        } else {
            next();
        }
    } catch (error) {
        next({ name: "login" });
    }
});

export default router;

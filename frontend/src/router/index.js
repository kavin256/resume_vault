import { createRouter, createWebHistory } from "vue-router";
import { useAuth } from "@clerk/vue";
import LandingView from "../views/LandingView.vue";
import HomeView from "../views/HomeView.vue";
import ProfileView from "../views/ProfileView.vue";
import GenerateView from "../views/GenerateView.vue";
import BillingView from "../views/BillingView.vue";
import SignInView from "../views/SignInView.vue";
import SignUpView from "../views/SignUpView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "landing",
      component: LandingView,
      meta: { public: true },
    },
    {
      path: "/sign-in",
      name: "sign-in",
      component: SignInView,
      meta: { public: true },
    },
    {
      path: "/sign-up",
      name: "sign-up",
      component: SignUpView,
      meta: { public: true },
    },
    {
      path: "/home",
      name: "home",
      component: HomeView,
      meta: { requiresAuth: true },
    },
    {
      path: "/profile",
      name: "profile",
      component: ProfileView,
      meta: { requiresAuth: true },
    },
    {
      path: "/generate",
      name: "generate",
      component: GenerateView,
      meta: { requiresAuth: true },
    },
    {
      path: "/billing",
      name: "billing",
      component: BillingView,
      meta: { requiresAuth: true },
    },
  ],
});

// Navigation guard to protect routes
router.beforeEach(async (to, from, next) => {
  // Allow public routes immediately without waiting for auth
  if (to.meta.public) {
    next();
    return;
  }

  // For protected routes, check authentication
  const { isSignedIn, isLoaded } = useAuth();

  // Wait for Clerk to load
  if (!isLoaded.value) {
    await new Promise((resolve) => {
      const interval = setInterval(() => {
        if (isLoaded.value) {
          clearInterval(interval);
          resolve();
        }
      }, 100);
      // Timeout after 5 seconds
      setTimeout(() => {
        clearInterval(interval);
        resolve();
      }, 5000);
    });
  }

  // If route requires auth and user is not signed in, redirect to sign-in
  if (to.meta.requiresAuth && !isSignedIn.value) {
    next({ name: "sign-in" });
  } else {
    next();
  }
});

export default router;

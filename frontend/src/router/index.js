import { createRouter, createWebHistory } from "vue-router";
import LandingView from "../views/LandingView.vue";
import HomeView from "../views/HomeView.vue";
import ProfileView from "../views/ProfileView.vue";
import GenerateView from "../views/GenerateView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "landing",
      component: LandingView,
    },
    {
      path: "/home",
      name: "home",
      component: HomeView,
    },
    {
      path: "/profile",
      name: "profile",
      component: ProfileView,
    },
    {
      path: "/generate",
      name: "generate",
      component: GenerateView,
    },
  ],
});

export default router;

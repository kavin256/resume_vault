import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import router from "./router";
import { clerkPlugin } from "@clerk/vue";

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

if (!PUBLISHABLE_KEY) {
  throw new Error("Add your Clerk Publishable Key to the .env file");
}

createApp(App)
  .use(clerkPlugin, { publishableKey: PUBLISHABLE_KEY })
  .use(router)
  .mount("#app");

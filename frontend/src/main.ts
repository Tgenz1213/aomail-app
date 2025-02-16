import { createApp } from "vue";
import App from "./App.vue";
import "./assets/css/tailwind.css";
import "./assets/css/fonts.css";
import "./assets/css/quill.css";
import { I18n } from "vue-i18n";
import { i18n, initializePreferences } from "./global/preferences";
import router from "./router/router";
import FlagIcon from "vue-flag-icon";

const app = createApp(App);
app.use(router);
app.use(FlagIcon);
app.use(i18n);

initializePreferences(i18n as I18n).then(() => {
    app.mount("#app");
});

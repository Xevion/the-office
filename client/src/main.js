import '@/scss/main.scss';
import Vue from "vue";
import {BootstrapVue, BootstrapVueIcons} from "bootstrap-vue";
import InstantSearch from "vue-instantsearch";
import VueClipboard from 'vue-clipboard2'
import VueScrollTo from "vue-scrollto";
import App from "./App.vue";
import router from "./router";
import store from "./store";

Vue.use(VueScrollTo);
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(InstantSearch);
Vue.use(VueClipboard)

Vue.config.productionTip = false;

router.beforeEach((to, from, next) => {
    // eslint-disable-next-line no-constant-condition
    if (from.name !== null && to.name === "Character" && false) next(false);
    else next();
});

new Vue({
    router,
    store,
    render: (h) => h(App),
}).$mount("#app");

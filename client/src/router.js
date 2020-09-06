import Vue from "vue";
import Router from "vue-router";
import Home from "./components/Home.vue";
import Episode from "./components/Episode.vue";
import SearchResults from "./components/SearchResults.vue";
import Character from "./components/Character.vue";

Vue.use(Router);

export default new Router({
    mode: "history",
    base: process.env.VUE_APP_BASE_URL,
    routes: [
        {
            path: "/",
            name: "Home",
            component: Home,
        },
        {
            path: "/character/:character",
            name: "Character",
            component: Character,
        },
        {
            path: "/:season/:episode",
            name: "Episode",
            component: Episode,
        },
        {
            path: "/search_results",
            name: "SearchResults",
            component: SearchResults,
        },
        {
            path: "*",
        },
    ],
    scrollBehavior(to, from, savedPosition) {
        // https://router.vuejs.org/guide/advanced/scroll-behavior.html
        if (to.hash) {
            return {selector: to.hash};
        }
        if (savedPosition) {
            return savedPosition;
        }
        return {
            x: 0,
            y: 0,
        };
    },
});

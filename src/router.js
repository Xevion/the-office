import Vue from "vue";
import Router from "vue-router";
import Home from "@/components/Home.vue";
import Episode from "@/components/Episode.vue";
import SearchResults from "@/components/SearchResults.vue";
import Character from "@/components/Character.vue";
import Season from "@/components/Season.vue";
import Characters from "@/components/Characters";
import About from "@/components/About";

Vue.use(Router);

export default new Router({
    mode: "history",
    routes: [
        {
            path: "/",
            name: "Home",
            component: Home,
        },
        {
            path: "/about/",
            name: "About",
            component: About,
        },
        {
            path: "/characters/",
            name: "Characters",
            component: Characters,
        },
        {
            path: "/search_results",
            name: "SearchResults",
            component: SearchResults,
        },
        {
            path: "/character/:character",
            name: "Character",
            component: Character,
        },
        {
            path: "/:season/",
            name: "Season",
            component: Season,
        },
        {
            path: "/:season/:episode",
            name: "Episode",
            component: Episode,
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

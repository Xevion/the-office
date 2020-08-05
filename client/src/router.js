import Vue from 'vue';
import Router from 'vue-router';
import Home from './components/Home.vue';
import Episode from './components/Episode.vue';
import SearchResults from './components/SearchResults.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/:season/:episode',
      name: 'Episode',
      component: Episode,
    },
    {
      path: '/search_results',
      name: 'SearchResults',
      component: SearchResults,
    },
  ],
});

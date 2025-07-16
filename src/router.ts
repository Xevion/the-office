import Home from '@/views/Home.vue';
import Episode from '@/views/Episode.vue';
import SearchResults from '@/views/SearchResults.vue';
import Character from '@/views/Character.vue';
import Season from '@/views/Season.vue';
import Characters from '@/views/Characters.vue';
import About from '@/views/About.vue';

import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/about/',
      name: 'About',
      component: About,
    },
    {
      path: '/characters/',
      name: 'Characters',
      component: Characters,
    },
    {
      path: '/search_results',
      name: 'SearchResults',
      component: SearchResults,
    },
    {
      path: '/character/:character',
      name: 'Character',
      component: Character,
    },
    {
      path: '/:season/',
      name: 'Season',
      component: Season,
    },
    {
      path: '/:season/:episode',
      name: 'Episode',
      component: Episode,
    },
    { path: '/:pathMatch(.*)*', name: 'NotFound', redirect: '/' }, // catch all
  ],
  scrollBehavior(to, from, savedPosition) {
    // https://router.vuejs.org/guide/advanced/scroll-behavior.html
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' };
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

export default router;

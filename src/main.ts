import '@fontsource/open-sans';
import '@fontsource-variable/roboto-slab';

import './index.css';
import { createApp } from 'vue';
import App from '@/App.vue';
import router from '@/router.ts';
import { createPinia } from 'pinia';
// import { createBootstrap, vBToggle   } from 'bootstrap-vue-next';

// Add the necessary CSS
// import 'bootstrap/dist/css/bootstrap.css';
// import 'bootstrap-vue-next/dist/bootstrap-vue-next.css';

// Prevent invalid episodes, seasons and characters from being accessed
router.beforeEach((to, from, next) => {
  if (from.name !== null && to.name === 'Character' && false) {
  } else next();
});

const pinia = createPinia();
const app = createApp(App);

app.use(router);
app.use(pinia);
app.mount('#app');

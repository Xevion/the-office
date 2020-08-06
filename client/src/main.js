import 'bootstrap/dist/css/bootstrap.css';
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import InstantSearch from 'vue-instantsearch';
import App from './App.vue';
import router from './router';

Vue.use(BootstrapVue);
Vue.use(InstantSearch);

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');

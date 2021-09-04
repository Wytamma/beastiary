import store from '@/store';
import '@babel/polyfill';
import Vue from 'vue';
import App from './App.vue';
// Import Component hooks before component definitions
import './component-hooks';
import './plugins/vee-validate';
import vuetify from './plugins/vuetify';
import router from './router';

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');

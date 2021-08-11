import Vue from 'vue';
import Router from 'vue-router';

import RouterComponent from './components/RouterComponent.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      component: () => import(/* webpackChunkName: "start" */ './views/main/Start.vue'),
      children: [
        {
          path: 'login',
          // route level code-splitting
          // this generates a separate chunk (about.[hash].js) for this route
          // which is lazy-loaded when the route is visited.
          component: () => import(/* webpackChunkName: "login" */ './views/Login.vue'),
        },
        {
          path: '404',
          component: () => import(/* webpackChunkName: "reset-password" */ './views/404.vue'),
        },
        {
          path: 'main',
          component: () => import(/* webpackChunkName: "main" */ './views/main/Main.vue'),
          children: [
            {
              path: 'dashboard',
              component: () => import(/* webpackChunkName: "main-dashboard" */ './views/main/Dashboard.vue'),
            },
          ],
        },
      ],
    },
    {
      path: '/*', redirect: '/404',
    },
  ],
});

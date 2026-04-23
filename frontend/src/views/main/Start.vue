<template>
  <router-view></router-view>
</template>

<script lang="ts">
import { runtimeCapabilities } from '@/runtime';
import { store } from '@/store';
import { dispatchCheckLoggedIn } from '@/store/main/actions';
import { readIsLoggedIn, readSupportsAuth } from '@/store/main/getters';
import { Component, Vue } from 'vue-property-decorator';

const startRouteGuard = async (to, from, next) => {
  await dispatchCheckLoggedIn(store);
  if (!readSupportsAuth(store)) {
    if (to.path === '/' || to.path === '/login') {
      next(runtimeCapabilities.defaultRoute);
    } else {
      next();
    }
    return;
  }
  if (readIsLoggedIn(store)) {
    if (to.path === '/login' || to.path === '/') {
      next('/main');
    } else {
      next();
    }
  } else if (readIsLoggedIn(store) === false) {
    if (to.path === '/' || (to.path as string).startsWith('/main')) {
      next({ path: '/login' });
    } else {
      next();
    }
  }
};

@Component
export default class Start extends Vue {
  public beforeRouteEnter(to, from, next) {
    startRouteGuard(to, from, next);
  }

  public beforeRouteUpdate(to, from, next) {
    startRouteGuard(to, from, next);
  }
}
</script>

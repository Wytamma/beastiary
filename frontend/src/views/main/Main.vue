<template>
<v-content fill-height>
  <v-layout fill-height >
    <v-navigation-drawer persistent v-model="showDrawer" fixed app>
      <v-layout column fill-height>
        <v-list nav>
          <v-subheader>Main menu</v-subheader>
          <v-list-item to="/main/dashboard">
            <v-list-item-action>
              <v-icon>web</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Dashboard</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item href="https://beastiary.wytamma.com" target="_blank">
            <v-list-item-action>
              <v-icon>mdi-file-document-multiple</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Docs</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item href="https://github.com/Wytamma/beastiary" target="_blank">
            <v-list-item-action>
              <v-icon>mdi-github</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Github</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <v-divider></v-divider>
        <v-spacer></v-spacer>
        <v-list>
          <v-list-item @click="logout">
            <v-list-item-action>
              <v-icon>close</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-layout>
    </v-navigation-drawer>
    <v-app-bar dark color="primary" app>
      <v-app-bar-nav-icon @click.stop="switchShowDrawer"></v-app-bar-nav-icon>
      <v-app-bar-title v-text="appName"></v-app-bar-title >
      <v-spacer></v-spacer>
      <v-switch
          v-model="$vuetify.theme.dark"
          hide-details
          inset
          color="blue darken-4"
      ></v-switch>
    </v-app-bar>
    <router-view></router-view>
  </v-layout>
</v-content>
</template>

<script lang="ts">
import { appName } from '@/env';
import { dispatchUserLogOut } from '@/store/main/actions';
import { readDashboardMiniDrawer, readDashboardShowDrawer } from '@/store/main/getters';
import { commitSetDashboardMiniDrawer, commitSetDashboardShowDrawer } from '@/store/main/mutations';
import { Component, Vue } from 'vue-property-decorator';

const routeGuardMain = async (to, from, next) => {
  if (to.path === '/main') {
    next('/main/dashboard');
  } else {
    next();
  }
};

@Component
export default class Main extends Vue {
  public appName = appName;

  public beforeRouteEnter(to, from, next) {
    routeGuardMain(to, from, next);
  }

  public beforeRouteUpdate(to, from, next) {
    routeGuardMain(to, from, next);
  }

  get miniDrawer() {
    return readDashboardMiniDrawer(this.$store);
  }

  get showDrawer() {
    return readDashboardShowDrawer(this.$store);
  }

  set showDrawer(value) {
    commitSetDashboardShowDrawer(this.$store, value);
  }

  public switchShowDrawer() {
    commitSetDashboardShowDrawer(
      this.$store,
      !readDashboardShowDrawer(this.$store),
    );
  }

  public switchMiniDrawer() {
    commitSetDashboardMiniDrawer(
      this.$store,
      !readDashboardMiniDrawer(this.$store),
    );
  }

  public async logout() {
    await dispatchUserLogOut(this.$store);
  }
}
</script>

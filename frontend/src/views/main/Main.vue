<template>
<v-content fill-height>
  <v-layout  >
    <v-navigation-drawer persistent v-model="showDrawer" fixed app>
      <v-layout column fill-height>
        <v-list nav>
          <v-subheader>Main menu</v-subheader>
          <v-list-item href="https://doi.org/10.1093/molbev/msac095" target="_blank">
            <v-list-item-action>
              <v-icon>mdi-school</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Paper</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item href="https://beastiary.wytamma.com" target="_blank">
            <v-list-item-action>
              <v-icon>mdi-file-document-multiple</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Documentation</v-list-item-title>
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
        <img class="mr-6 ml-5" src="https://beastiary.wytamma.com/images/Beastiary.png" alt="">
        <!-- citation -->
        <code>
          Wytamma Wirth, Sebastian Duchene, Real-Time and Remote MCMC Trace Inspection with Beastiary, Molecular Biology and Evolution, Volume 39, Issue 5, May 2022, msac095, https://doi.org/10.1093/molbev/msac095
        </code>
        <v-divider></v-divider>
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
    <v-app-bar dark color="teal lighten-2" app>
      <v-app-bar-nav-icon @click.stop="switchShowDrawer"></v-app-bar-nav-icon>
      <v-app-bar-title v-text="appName"></v-app-bar-title >
      <v-spacer></v-spacer>
      <v-switch
          v-model="$vuetify.theme.dark"
          hide-details
          inset
          color="teal darken-4"
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
import { Component, Vue, Watch } from 'vue-property-decorator';

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

  @Watch('$vuetify.theme.dark') 
  public onThemeChange(val) {
    console.log(val);
    
    if (val) {
        document.documentElement.setAttribute('data-theme', 'dark');
      } else {
        document.documentElement.removeAttribute('data-theme');
      }
  }
}
</script>

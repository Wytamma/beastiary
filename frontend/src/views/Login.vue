<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="teal lighten-2">
              <v-toolbar-title>{{appName}}</v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-text>
              <v-form @keyup.enter="submit">
                <v-text-field :disabled="loading" @keyup.enter="submit" v-model="token" prepend-icon="person" name="token" label="Token" type="text"></v-text-field>
              </v-form>
              <div v-if="loginError">
                <v-alert :value="loginError" transition="fade-transition" type="error">
                  Could not validate token
                </v-alert>
              </div>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-progress-circular
                indeterminate
                color="primary"
                v-if="loading"
                class="mr-4 mb-1"
              ></v-progress-circular>
              <v-btn v-else @click.prevent="submit">Login</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script lang="ts">
import { appName } from '@/env';
import { dispatchCheckToken } from '@/store/main/actions';
import { readLoginError } from '@/store/main/getters';
import { Component, Vue } from 'vue-property-decorator';


@Component
export default class Login extends Vue {
  public token: string = '';
  public appName = appName;
  public get loginError() {
    return readLoginError(this.$store);
  }
  public loading = false;

  public submit() {
    this.loading = true;
    dispatchCheckToken(this.$store, {token: this.token}).finally(() => {
      this.loading = false;
    });
  }
  private getTokenFromUrl() {
    // @ts-ignore
    return this.$router.history.current.query.token;
  }
  private mounted() {
    this.token = this.getTokenFromUrl();
    if (this.token) {
      this.submit();
    }
 }
}
</script>

<style>
</style>

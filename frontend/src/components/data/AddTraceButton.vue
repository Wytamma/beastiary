<template>
    <v-dialog
      v-model="dialog"
      persistent
      max-width="600px"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="teal lighten-2"
          dark
          fab
          elevation="2"
          x-small
          v-bind="attrs"
          v-on="on"
          @click="reset()"
        >
          <v-icon dark>
            mdi-plus
          </v-icon>
        </v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="text-h5">Add trace to Beastiary</span>
        </v-card-title>
        <v-card-text>
        <v-form @submit.prevent="submit"> 
          <v-text-field
                  required
                  label="Path to the log file"
                  v-model="path"
          ></v-text-field>
        </v-form>
         <v-list style="max-height: 300px;overflow: auto;">
              <v-list-item v-if="!isRoot">
                <v-list-item-avatar>
                  <v-icon
                      class="grey lighten-1"
                      dark
                    >
                      mdi-folder
                  </v-icon>
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title >..</v-list-item-title>
              </v-list-item-content>

              <v-list-item-action>
                <v-btn @click="currentPath=parentDir; list_dir()" icon >
                  <v-icon color="grey lighten-1">mdi-chevron-right</v-icon>
                </v-btn>
              </v-list-item-action>
              </v-list-item>
              <v-list-item
              v-for="file in files"
              :key="file.name"
              >
              <v-list-item-avatar>
                  <v-icon
                      class="grey lighten-1"
                      dark
                      v-if="file.is_dir"
                    >
                      mdi-folder
                  </v-icon>
                  <v-icon
                      class="primary lighten-1"
                      dark
                      v-else
                    >
                      mdi-file
                  </v-icon>
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title v-text="file.name"></v-list-item-title>
              </v-list-item-content>

              <v-list-item-action>
                <v-btn @click="currentPath=file.path; list_dir()" icon v-if="file.is_dir">
                  <v-icon color="grey lighten-1">mdi-chevron-right</v-icon>
                </v-btn>
                <v-btn @click="path=file.path" icon v-else>
                  <v-icon color="primary">mdi-plus</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="red lighten-3"
            text
            @click="dialog = false"
          >
            Close
          </v-btn>
          <v-btn
            color="primary"
            text
            @click="submit"
          >
            Add
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script lang="ts">
import { api } from '@/api';
import { dispatchCreateTrace } from '@/store/data/actions';
import { AxiosResponse } from 'axios';
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class AddTraceButton extends Vue {
    public dialog: boolean = false;
    public path: string = '';
    public currentPath: string = '';
    public parentDir: string = '';
    public files: any[] = [];
    public isRoot: boolean = true;

    public submit() {
      dispatchCreateTrace(this.$store, {path: this.path});
      this.dialog = false;
    }

    public reset() {
      this.path = '';
      this.currentPath = '';
      this.parentDir  = '';
      this.files = [];
      this.list_dir();
      this.isRoot = true;
    }

    public async list_dir() {
      let response: AxiosResponse | null = null;
      response = await api.listDirectory(this.$store.getters.token, this.currentPath);
      this.files = response.data.files;
      this.currentPath = response.data.path;
      this.parentDir = response.data.parent;
      this.isRoot = response.data.is_root;
    }
}
</script>

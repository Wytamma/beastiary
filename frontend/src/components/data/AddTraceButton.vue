<template>
    <v-dialog
      v-model="dialog"
      persistent
      max-width="600px"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="primary"
          dark
          fab
          elevation="2"
          x-small
          v-bind="attrs"
          v-on="on"
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
        <form>
          <v-text-field
                  required
                  label="Path to the log file"
                  v-model="path"
          ></v-text-field>
        </form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="dialog = false"
          >
            Close
          </v-btn>
          <v-btn
            color="blue darken-1"
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
import { dispatchCreateTrace } from '@/store/data/actions';
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class AddTraceButton extends Vue {
    public dialog: boolean = false;
    public path: string = '';

    public submit() {
      dispatchCreateTrace(this.$store, {path: this.path});
      this.dialog = false;
    }
}
</script>

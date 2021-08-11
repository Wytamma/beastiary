<template>
      <v-list dense >
      <v-list-item-group
        v-model="selectedItem"
        color="primary"
      >
        <v-list-item
          v-for="(run, i) in runs"
          :key="i"
        >   
        <v-list-item-action class="mr-0">
            <v-checkbox class="align-self-center"></v-checkbox>
        </v-list-item-action>
        <v-list-item-action class="mr-1">
            <v-radio class="align-self-center"></v-radio>
        </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title >{{fileName(run.path)}}</v-list-item-title>
          </v-list-item-content>
        <v-list-item-action class="mr-0">
            <v-checkbox class="align-self-center"></v-checkbox>
        </v-list-item-action>
        </v-list-item>
      </v-list-item-group>
    </v-list>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { dispatchGetRuns } from '@/store/data/actions';
import { readRuns } from '@/store/data/getters';

@Component
export default class RunsPanel extends Vue {

    get runs() {
        return readRuns(this.$store);
    }
    public async mounted() {
        await dispatchGetRuns(this.$store);
    }
    public fileName(path) {
     return path.substring(path.lastIndexOf('/') + 1);
 }
}
</script>

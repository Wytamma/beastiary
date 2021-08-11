<template>
      <v-list dense v-if="traces.length">
      <v-list-item-group
        color="primary"
        v-model="activeTraces"
        multiple
        active-class=""
      >
        <v-list-item
          v-for="(trace, i) in traces"
          :key="i"
        >  
        <template v-slot:default="{ active }">
          <v-list-item-action class="mr-0">
              <v-checkbox :input-value="active"></v-checkbox>
          </v-list-item-action>
          <v-list-item-action class="mr-1">
              <v-radio :value="i" ></v-radio>
          </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title >{{fileName(trace.path)}}</v-list-item-title>
            </v-list-item-content>
        </template>
        </v-list-item>
        
      </v-list-item-group>
    </v-list>
    <div v-else>
        No traces
      </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { dispatchGetTraces } from '@/store/data/actions';
import { readTraces } from '@/store/data/getters';

@Component
export default class TracesPanel extends Vue {
    public activeTraces = [];
    get traces() {
        return readTraces(this.$store);
    }
    public async mounted() {
        await dispatchGetTraces(this.$store);
    }
    public fileName(path) {
     return path.substring(path.lastIndexOf('/') + 1);
 }
}
</script>

<template>
      <v-layout fill-height  style=" overflow: hidden;">
      <v-row class="ml-4 mr-2 pb-8 mt-4">
        <v-col cols="3" class="pa-0">
          <div class="mt-0 fill-height elevation-4 rounded-lg">
            <v-toolbar
                  class="rounded-t-lg"
                  flat >
              <v-toolbar-title class="text-h5">
                  Traces
              </v-toolbar-title>
              
              <v-spacer></v-spacer>
              <AddTraceButton/>
            </v-toolbar>
            <v-divider v-if="traces.length > 0"></v-divider>
            <TraceList />
          </div>
        </v-col>
        <v-col cols="9" class="pl-4 pt-0">
          <div  v-if="activeParams" class="">

            <Trace class="elevation-3 mb-4 rounded-lg" />
            <Violin class="elevation-3 rounded-lg" />
          </div>
        </v-col>
      </v-row>
</v-layout>
</template>

<script lang="ts">
import '@/assets/css/custom.css';

import AddTraceButton from '@/components/data/AddTraceButton.vue';
import Trace from '@/components/data/graphs/Trace.vue';
import Violin from '@/components/data/graphs/Violin.vue';
import ParamsPanel from '@/components/data/ParamsPanel.vue';
import TraceList from '@/components/data/TraceList.vue';
import { readActiveTraceIDs, readTraces } from '@/store/data/getters';
import { Plotly } from 'vue-plotly';
import { Component, Vue } from 'vue-property-decorator';

@Component({
  components: {
    TraceList,
    ParamsPanel,
    Plotly,
    Trace,
    Violin,
    AddTraceButton,

  },
})
export default class Dashboard extends Vue {
  get activeTraceIDs() {
    const IDs = readActiveTraceIDs(this.$store);
    return IDs;
  }
  get traces() {
    return readTraces(this.$store);
  }

  get activeParams() {
    const traces = Object.values(this.traces);
    const activeParams = traces.map((trace) => trace.activeParams).flat().map((t) => t.toLowerCase());
    if (activeParams) {
      return [...new Set(activeParams)].join(' ');
    }
    return '';
  }


}
</script>

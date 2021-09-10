<template>
      <v-layout fill-height  style=" overflow: hidden;">
      <v-row>
        <v-col cols="4" class="pr-0 pl-6 mb-4 mt-2">
          <v-toolbar
                class="rounded-md"
                flat >
            <v-toolbar-title class="text-h5">
                Traces
            </v-toolbar-title>
            
            <v-spacer></v-spacer>
            <AddTraceButton/>
          </v-toolbar>
          <v-divider v-if="traces.length > 0"></v-divider>
          <TraceList />
        </v-col>
        <v-col cols="8" class="pl-2">
          <div  v-if="activeParams" class="">
            <Trace />
            <Violin />
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
    console.log(IDs);
    return IDs;
  }
  get traces() {
    return readTraces(this.$store);
  }

  get activeParams() {
    console.log(Object.values(this.traces));
    const traces = Object.values(this.traces);
    const activeParams = traces.map((trace) => trace.activeParams).flat().map((t) => t.toLowerCase());
    if (activeParams) {
      return [...new Set(activeParams)].join(' ');
    }
    return '';
  }


}
</script>

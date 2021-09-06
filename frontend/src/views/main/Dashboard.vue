<template>
      <v-layout fill-height  style=" overflow-y: hidden;">
      <v-row>
        <v-col cols="4" class="pr-0 pl-6 mb-4 mt-2">
          <v-toolbar
                class="rounded-md"
                flat >
            <v-toolbar-title >
                Traces
            </v-toolbar-title>
            
            <v-spacer></v-spacer>
            <AddTraceButton/>
          </v-toolbar>
          <v-divider v-if="traces.length > 0"></v-divider>
          <TraceList />
        </v-col>
        <v-col cols="8" class="pl-2">
          <div  v-if="activeTrace" class="my-4">
            <div class="text-button text-center">{{activeParam ? activeParam : ''}}</div >
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
import Histogram from '@/components/data/graphs/Histogram.vue';
import Trace from '@/components/data/graphs/Trace.vue';
import Violin from '@/components/data/graphs/Violin.vue';
import ParamsPanel from '@/components/data/ParamsPanel.vue';
import TraceList from '@/components/data/TraceList.vue';
import { readActiveTrace, readTraces } from '@/store/data/getters';
import { readActiveParam } from '@/store/data/getters';
import { Plotly } from 'vue-plotly';
import { Component, Vue } from 'vue-property-decorator';

@Component({
  components: {
    TraceList,
    ParamsPanel,
    Plotly,
    Histogram,
    Trace,
    Violin,
    AddTraceButton,

  },
})
export default class Dashboard extends Vue {
  get activeTrace() {
    return readActiveTrace(this.$store);
  }
  get traces() {
    return readTraces(this.$store);
  }
  get activeParam() {
    return readActiveParam(this.$store);
  }

}
</script>

<template>
      <v-layout fill-height  style=" overflow-y: hidden;">
        <v-col cols="4" class="pr-0">
          <v-toolbar
                class="rounded-md"
                flat >
            <v-toolbar-title >
                Traces
            </v-toolbar-title>
            
            <v-spacer></v-spacer>
            <AddTraceButton/>
            </v-toolbar>
            <v-divider></v-divider>
          <TraceList />
          <!-- <v-row no-gutters class="">
            <v-col>
              <TracesPanel />
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col>
              <ParamsPanel />
            </v-col>
          </v-row> -->
        </v-col>
        <v-col cols="8" class="pl-0">
          <div  v-if="activeTrace" class="my-4">
            <Trace />
            <Histogram />
          </div>
        </v-col>
</v-layout>
</v-content >
</template>

<script lang="ts">
import '@/assets/css/custom.css';

import { Component, Vue } from 'vue-property-decorator';
import TraceList from '@/components/data/TraceList.vue';
import ParamsPanel from '@/components/data/ParamsPanel.vue';
import Histogram from '@/components/data/graphs/Histogram.vue';
import AddTraceButton from '@/components/data/AddTraceButton.vue';
import Trace from '@/components/data/graphs/Trace.vue';
import { readActiveTrace } from '@/store/data/getters';
import { Plotly } from 'vue-plotly';
@Component({
  components: {
    TraceList,
    ParamsPanel,
    Plotly,
    Histogram,
    Trace,
    AddTraceButton,
  },
})
export default class Dashboard extends Vue {
  get activeTrace() {
    return readActiveTrace(this.$store);
}
}
</script>

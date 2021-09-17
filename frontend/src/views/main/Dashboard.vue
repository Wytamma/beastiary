<template>
      <v-layout  style=" overflow: hidden;">
      <v-row class="ma-0 pb-0">
        <v-col cols="3" class="mt-4 pt-0 pr-0">
          <v-card  class="rounded-lg px-0 ma-0">
               <div>
            <v-toolbar
                  class="rounded-t-lg"
                  flat >
              <v-toolbar-title class="text-h5">
                  Traces
              </v-toolbar-title>
              
              <v-spacer></v-spacer>
              <AddTraceButton/>
            </v-toolbar>
            </div>
            <v-divider v-if="traces.length > 0"></v-divider>
            <div style="max-height: 80vh;overflow: auto;">
              <TraceList />
            </div>
          </v-card>
        </v-col>
        <v-col cols="9" class="pl-4 mt-4 pt-0">
          <v-card v-if="activeParams" class="rounded-lg ">
              <v-tabs  v-model="tab" right  class="mb-4">
                <v-tab >
                  Trace
                </v-tab>
                <v-tab>
                  Violin
                </v-tab>
                <v-tab>
                  Histogram
                </v-tab>
                <v-tab>
                  Density
                </v-tab>
                <v-tab>
                  Joint
                </v-tab>
                <v-tab>
                  ESS
                </v-tab>
                <v-tab>
                  Estimates
                </v-tab>
              </v-tabs>
            <v-tabs-items v-model="tab">
              <v-tab-item >
                <v-card flat class="pa-2" >
                    <Trace v-if="tab === 0" />
                </v-card>
              </v-tab-item>
              <v-tab-item>
                <v-card flat class="pa-2"  fill-height>
                    <Violin v-if="tab === 1"/>
                </v-card>
              </v-tab-item>
              <v-tab-item>
                <v-card flat class="pa-2"  fill-height>
                    WIP
                </v-card>
              </v-tab-item>
              <v-tab-item>
                <v-card flat class="pa-2"  fill-height>
                    WIP
                </v-card>
              </v-tab-item>
              <v-tab-item>
                <v-card flat class="pa-2"  fill-height>
                    WIP
                </v-card>
              </v-tab-item>
              <v-tab-item>
                <v-card flat class="pa-2"  fill-height>
                    WIP
                </v-card>
              </v-tab-item>
              <v-tab-item>
                <v-card flat class="pa-2"  fill-height>
                    WIP
                </v-card>
              </v-tab-item>
            </v-tabs-items>
            
          </v-card>
          
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
  public tab = null;

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

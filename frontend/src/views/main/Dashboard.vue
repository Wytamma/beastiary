<template>
      <v-layout  style=" overflow: hidden;">
      <v-row class="ma-0 pb-0">
        <v-col cols="3" class="mt-4 pt-0 pr-0">
          <v-card  class="rounded-lg px-0 ma-0">
               <div>
            <v-toolbar
                  class="rounded-lg"
                  flat >
              <v-toolbar-title class="text-h5">
                  Traces
              </v-toolbar-title>
              
              <v-spacer></v-spacer>
              <AddTraceButton/>
            </v-toolbar>
            </div>
            <v-divider v-if="traces.length > 0"></v-divider>
            <div style="max-height: 80vh" class="no-scrollbar">
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
                  Pairwise
                </v-tab>
                <v-tab>
                  Parallel
                </v-tab>
                <v-tab>
                  ESS
                </v-tab>
                <v-tab>
                  Estimates
                </v-tab>
              </v-tabs>
            <v-tabs-items v-model="tab" >
             <div ref="tabItems" >
              <v-tab-item >
                <v-card flat class="pa-2"  fill-height>
                  <vue-resizable 
                    :active='["b"]'
                    @mount="eHandler"
                    @resize:move="eHandler"
                    @resize:start="eHandler"
                    @resize:end="eHandler" 
                    :width="tabWidth"
                    :height="tabHeight"
                    class="pb-4"
                  >
                    <Trace v-if="tab === 0" :height="tabHeight" :width="tabWidth" />
                  </vue-resizable>
                </v-card>
              </v-tab-item>
              <v-tab-item>
                <v-card flat class="pa-2"  fill-height>
                  <vue-resizable 
                    :active='["b"]'
                    @mount="eHandler"
                    @resize:move="eHandler"
                    @resize:start="eHandler"
                    @resize:end="eHandler" 
                    :width="tabWidth"
                    :height="tabHeight"
                  >
                    <Violin v-if="tab === 1" :height="tabHeight" :width="tabWidth" />
                  </vue-resizable>
                </v-card>
              </v-tab-item>
              <v-tab-item>
                <v-card flat class="pa-2"  fill-height>
                  <vue-resizable 
                    :active='["b"]'
                    @mount="eHandler"
                    @resize:move="eHandler"
                    @resize:start="eHandler"
                    @resize:end="eHandler" 
                    :width="tabWidth"
                    :height="tabHeight"
                  >
                    <Histogram v-if="tab === 2" :height="tabHeight" :width="tabWidth" />
                  </vue-resizable>
                </v-card>
              </v-tab-item>
              <v-tab-item>
                <v-card flat class="pa-2"  fill-height >
                  <vue-resizable 
                    :active='["b"]'
                    @mount="eHandler"
                    @resize:move="eHandler"
                    @resize:start="eHandler"
                    @resize:end="eHandler" 
                    :width="tabWidth"
                    :height="tabHeight"
                  >
                    <Pairwise v-if="tab === 3" :height="tabHeight" :width="tabWidth" />
                  </vue-resizable>
                </v-card>
              </v-tab-item>
              <v-tab-item>
                <v-card flat class="pt-2 pb-2"  fill-height>
                  <vue-resizable 
                    :active='["b"]'
                    @mount="eHandler"
                    @resize:move="eHandler"
                    @resize:start="eHandler"
                    @resize:end="eHandler" 
                    :width="tabWidth"
                    :height="tabHeight"
                  >
                    <Parallel v-if="tab === 4" :height="tabHeight" :width="tabWidth" />
                  </vue-resizable>
                </v-card>
              </v-tab-item>
              <v-tab-item>
                <v-card flat class="pa-2"  fill-height>
                  <vue-resizable 
                    :active='["b"]'
                    @mount="eHandler"
                    @resize:move="eHandler"
                    @resize:start="eHandler"
                    @resize:end="eHandler" 
                    :width="tabWidth"
                    :height="tabHeight"
                  >
                    <CumulativeESS v-if="tab === 5" :height="tabHeight" :width="tabWidth" />
                    
                  </vue-resizable>
                </v-card>
              </v-tab-item>
              <v-tab-item>
                <v-card flat class="pa-2"  fill-height>
                    <StatsTable v-if="tab === 6" :height="tabHeight" :width="tabWidth" />
                </v-card>
              </v-tab-item>
            </div>
            </v-tabs-items>
          </v-card>
        </v-col>
      </v-row>
</v-layout>
</template>

<script lang="ts">
import '@/assets/css/custom.css';

import AddTraceButton from '@/components/data/AddTraceButton.vue';
import CumulativeESS from '@/components/data/graphs/ESS.vue';
import Histogram from '@/components/data/graphs/Histogram.vue';
import Pairwise from '@/components/data/graphs/Pairwise.vue';
import Parallel from '@/components/data/graphs/Parallel.vue';
import Trace from '@/components/data/graphs/Trace.vue';
import Violin from '@/components/data/graphs/Violin.vue';
import ParamsPanel from '@/components/data/ParamsPanel.vue';
import StatsTable from '@/components/data/StatsTable.vue';
import TraceList from '@/components/data/TraceList.vue';

import { readActiveTraceIDs, readTraces } from '@/store/data/getters';
import { Plotly } from 'vue-plotly';
import { Component, Vue } from 'vue-property-decorator';
import VueResizable from 'vue-resizable';

@Component({
  components: {
    TraceList,
    ParamsPanel,
    Plotly,
    Trace,
    Violin,
    Histogram,
    Parallel,
    AddTraceButton,
    StatsTable,
    CumulativeESS,
    Pairwise,
    VueResizable,
  },
})
export default class Dashboard extends Vue {
  public tab = null;
  public tabHeight = 450;
  public tabWidth = null;

  public eHandler(data) {
      this.tabHeight = data.height;
      if (this.$refs.tabItems) {
        // @ts-ignore
        this.tabWidth = this.$refs.tabItems.clientWidth;
      }
  }

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

  private mounted() {
    window.addEventListener('resize', this.setPlotWidth);
  }
  private unmounted() {
    window.removeEventListener('resize', this.setPlotWidth);
  }

  private setPlotWidth() {
    if (this.$refs.tabItems) {
      // @ts-ignore
      this.tabWidth = this.$refs.tabItems.clientWidth;
    }
  }

}
</script>

<style scoped>
    .resizable-content {
        height: 450px;
        width: 100%;
        background-color: aqua;
    }
</style>
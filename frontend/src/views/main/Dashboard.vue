<template>
      <v-layout fill-height>
      <v-row
        no-gutters
      > 
        <v-col cols="3" class="">
          <v-row no-gutters class="">
            <v-col>
              <TracesPanel />
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col>
              <ParamsPanel />
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="9">
          <div class="ma-4">
            <Trace />
            <Histogram />
          </div>
        </v-col>
      </v-row>
</v-layout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import TracesPanel from '@/components/data/TracesPanel.vue';
import ParamsPanel from '@/components/data/ParamsPanel.vue';
import Histogram from '@/components/data/graphs/Histogram.vue';
import Trace from '@/components/data/graphs/Trace.vue';
import { Plotly } from 'vue-plotly';
@Component({
  components: {
    TracesPanel,
    ParamsPanel,
    Plotly,
    Histogram,
    Trace,
  },
})
export default class Dashboard extends Vue {}
</script>

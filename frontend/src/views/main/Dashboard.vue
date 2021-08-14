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
          <Plotly v-if="activeTrace" :data="plotData" :layout="layout" :display-mode-bar="false"></Plotly>
          </div>
        </v-col>
      </v-row>
</v-layout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Plotly } from 'vue-plotly'
import TracesPanel from '@/components/TracesPanel.vue';
import ParamsPanel from '@/components/ParamsPanel.vue';
import { readActiveParam, readActiveTrace } from '@/store/data/getters';

@Component({
  components: {
    TracesPanel,
    ParamsPanel,
    Plotly,
  },
})
export default class Dashboard extends Vue {
  get layout () {
      return {title: this.activeParam}
  }
  get plotData() {
    let trace = readActiveTrace(this.$store);
    let param = readActiveParam(this.$store)
    if (trace && param){
      return [{
        x: trace.parameters[param].map(function(row) { return row['state']; }),
        y: trace.parameters[param].map(function(row) { return row['value']; }),
        type:"scatter"
      }]
    } else {
      return {}
    }
  }
  get activeTrace() {
        return readActiveTrace(this.$store);
  }
  get activeParam() {
    return readActiveParam(this.$store)
  }
}
</script>

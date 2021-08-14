<template>
      <v-layout fill-height>
      <v-row
        no-gutters
      > 
        <v-col cols="3">
          <v-row no-gutters>
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
          <Plotly v-if="activeTrace" :data="plotData" :layout="layout" :display-mode-bar="false"></Plotly>
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
      let y = {};
      trace.parameters[param].forEach(obj => {
        Object.keys(obj).forEach(key => {
          y[key] = (y[key] || []).concat([obj[key]]);
        });
      });
      console.log([y])
      return [{
        x: y['state'],
        y: y['value'],
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

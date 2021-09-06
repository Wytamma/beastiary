<template>
<div>
    <Plotly :data="traceData" :layout="layout" :display-mode-bar="false"></Plotly>
</div>
</template>

<script lang="ts">
import { readActiveParam, readActiveTrace } from '@/store/data/getters';
import { readBurnIn } from '@/store/data/getters';
import { Plotly } from 'vue-plotly';
import { Component, Vue } from 'vue-property-decorator';
@Component({
  components: {
    Plotly,
  },
})
export default class Histogram extends Vue {
  get layout() {
    return {
      grid: {pattern: 'dependent'},
      xaxis: {domain: [0, 0.7], showgrid: true, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
      yaxis: {showgrid: true, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
      yaxis2: {showgrid: true, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
      xaxis2: {domain: [0.73, 1], showline: false, zeroline: false, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
      showlegend: false,
      plot_bgcolor: 'rgba(0, 0, 0, 0)',
      paper_bgcolor: 'rgba(0, 0, 0, 0)',
      margin: {
        l: 50,
        r: 30,
        b: 30,
        t: 10,
        pad: 0,
      },
    };
  }
  get traceData() {
    const trace = readActiveTrace(this.$store);
    const param = readActiveParam(this.$store);
    const burnIn = readBurnIn(this.$store) / 100;
    if (trace && param) {

      return [{
        x: trace.parameters[param].slice(trace.parameters.state.length * burnIn).map((row) =>  row.state),
        y: trace.parameters[param].slice(trace.parameters.state.length * burnIn).map((row) =>  row.value),
        type: 'scatter',
        opacity: 0.8,
      }, {
        y: trace.parameters[param].slice(trace.parameters.state.length * burnIn).map((row) =>  row.value),
        type: 'histogram',
        xaxis: 'x2',
        yaxis: 'y1',
        opacity: 0.6,
      }];
    } else {
      return {};
    }
  }
  get activeTrace() {
        return readActiveTrace(this.$store);
  }
}
</script>

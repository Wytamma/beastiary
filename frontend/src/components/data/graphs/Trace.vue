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
      plot_bgcolor: 'rgba(0, 0, 0, 0)',
      paper_bgcolor: 'rgba(0, 0, 0, 0)',
      margin: {
        l: 80,
        r: 80,
        b: 80,
        t: 20,
        pad: 0,
      },
      height: 400,
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

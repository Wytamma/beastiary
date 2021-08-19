<template>
<div>
    <Plotly v-if="activeTrace" :data="traceData" :layout="layout" :display-mode-bar="false"></Plotly>
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { readActiveParam, readActiveTrace } from '@/store/data/getters';
import { Plotly } from 'vue-plotly';
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
    if (trace && param) {
      return [{
        x: trace.parameters[param].map((row) =>  row.state),
        y: trace.parameters[param].map((row) =>  row.value),
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

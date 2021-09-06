<template>
    <Plotly :data="HistogramData" :layout="layout" :display-mode-bar="false" class="mt-0"></Plotly>
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
    get activeTrace() {
        return readActiveTrace(this.$store);
    }
    get layout() {
        return {
            plot_bgcolor: 'rgba(0, 0, 0, 0)',
            paper_bgcolor: 'rgba(0, 0, 0, 0)',
            margin: {
            l: 40,
            r: 40,
            b: 80,
            t: 20,
            pad: 0,
            },
            height: 500,
        };
    }
    get HistogramData() {
    const trace = readActiveTrace(this.$store);
    const param = readActiveParam(this.$store);
    const burnIn = readBurnIn(this.$store) / 100;
    if (trace && param) {
      return [{
        y: trace.parameters[param].slice(trace.parameters.state.length * burnIn).map((row) =>  row.value),
        type: 'histogram',
      }];
    } else {
      return {};
    }
  }
}
</script>

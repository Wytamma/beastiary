<template>
    <Plotly :data="ViolinData" :layout="layout" :display-mode-bar="false" class="mt-0"></Plotly>
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
export default class Violin extends Vue {
    get activeTrace() {
        return readActiveTrace(this.$store);
    }
    get layout() {
        return {
            plot_bgcolor: 'rgba(0, 0, 0, 0)',
            paper_bgcolor: 'rgba(0, 0, 0, 0)',
            yaxis: {showticklabels: false, zeroline: false},
            xaxis: { zeroline: false, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
            margin: {
            l: 50,
            r: 30,
            b: 20,
            t: 30,
            pad: 0,
            },
            height: 200,
        };
    }
    get ViolinData() {
    const trace = readActiveTrace(this.$store);
    const param = readActiveParam(this.$store);
    const burnIn = readBurnIn(this.$store) / 100;
    if (trace && param) {
        // console.log(Object.keys(trace.parameters).map( param => trace.parameters[param].map((row) =>  row.value)))
        const data = trace.parameters[param].slice(trace.parameters.state.length * burnIn).map((row) =>  row.value);
        return [{
        x: data,
        type: 'violin',
        points: 'none',
        box: {
            visible: true,
        },
        boxpoints: false,
        line: {
            color: 'black',
        },
        opacity: 0.6,
        meanline: {
            visible: true,
        },
        fillcolor: '#8dd3c7',
      }];
    } else {
      return {};
    }
  }
}
</script>

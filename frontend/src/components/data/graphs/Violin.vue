<template>
    <Plotly :data="ViolinData" :layout="layout" :display-mode-bar="false" class="mt-0"></Plotly>
</template>

<script lang="ts">
import { readActiveTraceIDs, readTraces } from '@/store/data/getters';
import { Plotly } from 'vue-plotly';
import { Component, Vue } from 'vue-property-decorator';
import { Trace } from '../../../interfaces';
@Component({
  components: {
    Plotly,
  },
})
export default class Violin extends Vue {
    get traces() {
      return readTraces(this.$store);
    }
    get activeTraceIDs() {
      return readActiveTraceIDs(this.$store);
    }
    get layout() {
        return {
            plot_bgcolor: 'rgba(0, 0, 0, 0)',
            paper_bgcolor: this.$vuetify.theme.dark ? '#1E1E1E' : 'rgba(0, 0, 0, 0)',
            yaxis: {showticklabels: false, zeroline: false},
            xaxis: { zeroline: false, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
            margin: {
            l: 50,
            r: 30,
            b: 30,
            t: 10,
            pad: 0,
            },
            height: 270,
        };
    }
    get ViolinData() {
    const data: any[] = [];
    const colours = [
      '#2980b9',
      '#2ecc71',
      '#9b59b6',
      '#f1c40f',
      '#e74c3c',
      '#1abc9c',
      '#8e44ad',
      '#1f77b4',
      '#ff7f0e',
      '#2ca02c',
      '#d62728',
      '#9467bd',
      '#8c564b',
      '#e377c2',
      '#7f7f7f',
      '#bcbd22',
      '#17becf',
    ];
    let count = 0;
    for (const trace of Object.values(this.traces)) {
      // @ts-ignore
      if (trace.isActive) {
        // @ts-ignore
        const burnIn = trace.burnIn / 100;
        // @ts-ignore
        for (const param of trace.activeParams) {
          data.push({
            // @ts-ignore
            x: trace.parameters[param].slice(trace.parameters.state.length * burnIn).map((row) =>  row.value),
            y: null,
            type: 'violin',
            points: 'none',
            box: {
                visible: true,
            },
            boxpoints: false,
            line: {
                color: 'black',
            },
            opacity: 0.5,
            meanline: {
                visible: true,
            },
            fillcolor: colours[count],
            name: Object.values(this.traces).filter((t) => t.activeParams.length > 0).length === 1 ? `${param}` : `${this.fileName(trace.path)} - ${param}`,
            hovertemplate: '%{y}',
            // @ts-ignore
            showlegend: false,
            // @ts-ignore
            legendgroup: `${param}`,
          });

          count++;
        }
      }
    }
    return data;
  }
  public fileName(path) {
    return path.substring(path.lastIndexOf('/') + 1);
  }
}
</script>

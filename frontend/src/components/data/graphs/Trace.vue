<template>
<div>
    <Plotly :data="traceData" :layout="layout" :display-mode-bar="false"></Plotly>
</div>
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
export default class Histogram extends Vue {
  get traces() {
    return readTraces(this.$store);
  }
  get activeTraceIDs() {
      return readActiveTraceIDs(this.$store);
  }
  get layout() {
    return {
      grid: {pattern: 'dependent'},
      xaxis: {domain: [0, 0.7], showgrid: true, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
      yaxis: {showgrid: true, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
      yaxis2: {showgrid: true, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
      xaxis2: {domain: [0.73, 1], showline: false, zeroline: false, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
      plot_bgcolor: 'rgba(0, 0, 0, 0)',
      paper_bgcolor: this.$vuetify.theme.dark ? '#1E1E1E' : 'rgba(0, 0, 0, 0)',
      barmode: 'overlay',
      legend: {orientation: 'h', x: 0.5, y: 1.15, xanchor: 'center', font: {color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'}},
      margin: {
        l: 50,
        r: 30,
        b: 30,
        t: 0,
        pad: 0,
      },
      height: 400,
    };
  }
  get traceData() {
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
        for (const param of trace.activeParams) {
          data.push({
            x: trace.parameters[param].slice(trace.parameters.state.length * burnIn).map((row) =>  row.state),
            y: trace.parameters[param].slice(trace.parameters.state.length * burnIn).map((row) =>  row.value),
            type: 'scatter',
            opacity: 0.8,
            name: Object.values(this.traces).filter((t) => t.activeParams.length > 0).length === 1 ? `${param}` : `${this.fileName(trace.path)} - ${param}`,
            marker: {color: colours[count]},
            hovertemplate: '%{y}',
            showlegend: false,
          });
          data.push({
            y: trace.parameters[param].slice(trace.parameters.state.length * burnIn).map((row) =>  row.value),
            type: 'histogram',
            xaxis: 'x2',
            yaxis: 'y1',
            opacity: 0.6,
            name: Object.values(this.traces).filter((t) => t.activeParams.length > 0).length === 1 ? `${param}` : `${this.fileName(trace.path)} - ${param}`,
            marker: {color: colours[count]},
            hovertemplate: '%{y}',
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

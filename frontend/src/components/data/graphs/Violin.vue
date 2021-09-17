<template>
    <Plotly :data="ViolinData" :layout="layout" :toImageButtonOptions="{
          filename: 'violin',
          width: null,
          height: null,
          format: 'svg'
      }" :displaylogo="false"  :mode-bar-buttons-to-remove="modeBarButtons" :display-mode-bar="true"></Plotly>
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
    get modeBarButtons() {
      return [
        'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d',
        'hoverClosestCartesian', 'hoverCompareCartesian',
        'zoom3d', 'pan3d', 'resetCameraDefault3d', 'resetCameraLastSave3d', 'hoverClosest3d',
        'orbitRotation', 'tableRotation',
        'zoomInGeo', 'zoomOutGeo', 'resetGeo', 'hoverClosestGeo',
        'sendDataToCloud',
        'hoverClosestGl2d',
        'hoverClosestPie',
        'toggleHover',
        'resetViews',
        'toggleSpikelines',
        'resetViewMapbox',
      ];
    }
    get traces() {
      return readTraces(this.$store);
    }
    get activeTraceIDs() {
      return readActiveTraceIDs(this.$store);
    }
    get layout() {
      return {
          plot_bgcolor: this.$vuetify.theme.dark ? '#1E1E1E' : 'white',
          paper_bgcolor: this.$vuetify.theme.dark ? '#1E1E1E' : 'white',
          yaxis: {showticklabels: false, zeroline: false},
          xaxis: { zeroline: false, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
          legend: {
            orientation: 'h', x: 0.5, y: 1.15,
            xanchor: 'center',
            font: {size: 15, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
          },
          displayModeBar: true,
          margin: {
          l: 50,
          r: 50,
          b: 30,
          t: 0,
          pad: 0,
          },
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
            showlegend: true,
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

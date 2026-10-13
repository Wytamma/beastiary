<template>
<div>
    <Plotly :data="traceData" :layout="layout" 
    :toImageButtonOptions="{
          filename: 'trace',
          width: null,
          height: null,
          format: 'svg'
      }" :displaylogo="false"  :mode-bar-buttons-to-remove="modeBarButtons" :display-mode-bar="true" ></Plotly>
</div>
</template>

<script lang="ts">
import { Data } from '@/interfaces';
import { urlFileName } from '@/logParser';
import { readActiveTraceIDs, readTraces } from '@/store/data/getters';
import { readSettings } from '@/store/settings/getters';
import { thin } from '@/utils';
import { Plotly } from 'vue-plotly';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({
  components: {
    Plotly,
  },
})
export default class Trace extends Vue {
  // @ts-ignore
  @Prop() public height: number;
  // @ts-ignore
  @Prop() public width: number;
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
      grid: {pattern: 'dependent'},
      xaxis: {domain: [0, 0.7], showgrid: true, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
      yaxis: {showgrid: true, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
      yaxis2: {showgrid: true, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
      xaxis2: {domain: [0.73, 1], showline: false, zeroline: false, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
      plot_bgcolor: this.$vuetify.theme.dark ? '#1E1E1E' : 'white',
      paper_bgcolor: this.$vuetify.theme.dark ? '#1E1E1E' : 'white',
      barmode: 'overlay',
      legend: {orientation: 'h', x: 0.5, y: 1.15, xanchor: 'center', font: {size: 15, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'}},
      margin: {
        l: 50,
        r: 20,
        b: 30,
        t: 0,
        pad: 0,
      },
      height: this.height,
      width: this.width,
    };
  }
  get traceData() {
    const data: any[] = [];
    const settings = readSettings(this.$store);
    const colours = settings.palette;
    let count = 0;
    for (const trace of Object.values(this.traces)) {
      // @ts-ignore
      if (trace.isActive) {
        // @ts-ignore
        const burnIn = trace.burnIn / 100;
        for (const param of trace.activeParams) {
          const rows: Data[] = trace.parameters[param].slice(trace.parameters.state.length * burnIn);
          // Only the line is thinned; the side histogram summarises every sample.
          const lineRows = thin(rows, settings.thinningInterval);
          data.push({
            x: lineRows.map((row) =>  row.state),
            y: lineRows.map((row) =>  row.value),
            type: 'scatter',
            opacity: 0.8,
            name: Object.values(this.traces).filter((t) => t.activeParams.length > 0).length === 1 ? `${param}` : `${this.fileName(trace.path)} - ${param}`,
            marker: {color: colours[count % colours.length]},
            hovertemplate: '%{y}',
            showlegend: false,
          });
          data.push({
            y: rows.map((row) =>  row.value),
            type: 'histogram',
            histnorm: 'probability',
            // The histogram is drawn sideways (values on y), so the bin count is nbinsy.
            nbinsy: settings.histogramBins,
            xaxis: 'x2',
            yaxis: 'y1',
            opacity: settings.histogramOpacity,
            name: Object.values(this.traces).filter((t) => t.activeParams.length > 0).length === 1 ? `${param}` : `${this.fileName(trace.path)} - ${param}`,
            marker: {color: colours[count % colours.length]},
            hovertemplate: '%{y}',
          });
          count++;
        }
      }

    }
    return data;
  }
  public fileName(path) {
    return urlFileName(path);
  }
}
</script>

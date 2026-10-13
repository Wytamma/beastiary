<template>
    <Plotly :data="HistogramData" :layout="layout" :toImageButtonOptions="{
          filename: 'histogram',
          width: null,
          height: null,
          format: 'svg'
      }" :displaylogo="false"  :mode-bar-buttons-to-remove="modeBarButtons" :display-mode-bar="true"></Plotly>
</template>

<script lang="ts">
import { urlFileName } from '@/logParser';
import { readActiveTraceIDs, readTraces } from '@/store/data/getters';
import { readSettings } from '@/store/settings/getters';
import { Plotly } from 'vue-plotly';
import { Component, Prop, Vue } from 'vue-property-decorator';
@Component({
  components: {
    Plotly,
  },
})
export default class Histogram extends Vue {
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
          plot_bgcolor: this.$vuetify.theme.dark ? '#1E1E1E' : 'white',
          paper_bgcolor: this.$vuetify.theme.dark ? '#1E1E1E' : 'white',
          yaxis: {showticklabels: true, zeroline: false, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
          xaxis: { zeroline: false, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
          legend: {
            orientation: 'h', x: 0.5, y: 1.15,
            xanchor: 'center',
            font: {size: 15, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
          },
          barmode: 'overlay',
          displayModeBar: true,
          margin: {
          l: 50,
          r: 50,
          b: 30,
          t: 0,
          pad: 0,
          },
          height: this.height,
          width: this.width,
      };
    }
    get HistogramData() {
    const data: any[] = [];
    const settings = readSettings(this.$store);
    const colours = settings.palette;
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
            type: 'histogram',
            histnorm: 'probability',
            nbinsx: settings.histogramBins,
            points: 'none',
            box: {
                visible: true,
            },
            boxpoints: false,
            line: {
                color: 'black',
            },
            opacity: settings.histogramOpacity,
            meanline: {
                visible: true,
            },
            marker: {
                color: colours[count % colours.length],
            },
            fillcolor: colours[count % colours.length],
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
    return urlFileName(path);
  }
}
</script>

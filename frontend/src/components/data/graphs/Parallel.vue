<template>
    <Plotly :data="ParallelData" :layout="layout" :toImageButtonOptions="{
          filename: 'parallel',
          width: null,
          height: null,
          format: 'svg'
      }" :displaylogo="false"  :mode-bar-buttons-to-remove="modeBarButtons" :display-mode-bar="true"></Plotly>
</template>

<script lang="ts">
import { Data } from '@/interfaces';
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
export default class Parallel extends Vue {
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
          yaxis: {showticklabels: false, zeroline: false, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
          xaxis: { zeroline: false, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
          displayModeBar: true,
          name: 'test',
          margin: {
          l: 50,
          r: 50,
          b: 30,
          t: 50,
          pad: 0,
          },
          height: this.height,
          width: this.width,
      };
    }
    get ParallelData() {
    const data: any = {};
    const dimensions: any[] = [];
    const interval = readSettings(this.$store).thinningInterval;
    let traceFound = null;
    let  burnIn = null;
    for (const trace of Object.values(this.traces)) {
      // @ts-ignore
      if (trace.isActive) {
        // @ts-ignore
        burnIn = trace.burnIn / 100;
        // @ts-ignore

        // dimentsions
        for (const param of trace.activeParams) {
          // found open tace break
          traceFound = trace;
          // @ts-ignore
          const rows: Data[] = trace.parameters[param].slice(trace.parameters.state.length * burnIn);
          dimensions.push(
            {
              label: param,
              values: thin(rows, interval).map((row) =>  row.value),
            },
          );
        }
      }
      if (traceFound) {
        break;
      }
    }
    if (traceFound) {
      data.dimensions = dimensions;
      data.labelfont = {color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'};
      data.rangefont = {color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'};

      data.type = 'parcoords';
      const found: any = traceFound;
      // @ts-ignore
      const colourRows: Data[] = found.parameters[found.activeParams[0]].slice(found.parameters.state.length * burnIn);
      const colorValues = thin(colourRows, interval).map((row) =>  row.value);
      data.line = {
        showscale: true,
        reversescale: true,
        colorscale: 'Jet',
        color: colorValues,
        label: 'test',
        colorbar: {
          outlinecolor: this.$vuetify.theme.dark ? 'white' : '#2c3e50',
          tickfont: {
            color: this.$vuetify.theme.dark ? 'white' : '#2c3e50',
          },
          title: {
            font: {color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
            // @ts-ignore
            text: traceFound.activeParams[0],
          },
        },
      };
      return [data];
    }
    return [];

  }
  public fileName(path) {
    return path.substring(path.lastIndexOf('/') + 1);
  }
}
</script>

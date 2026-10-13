<template>
    <Plotly :data="JointData" :layout="layout" :toImageButtonOptions="{
          filename: 'pairwise',
          width: null,
          height: null,
          format: 'svg'
      }" :displaylogo="false"  :mode-bar-buttons-to-remove="modeBarButtons" :display-mode-bar="true"></Plotly>
</template>

<script lang="ts">
// @ts-ignore
import { Data } from '@/interfaces';
import { readActiveTraceIDs, readDisplayTraces } from '@/store/data/getters';
import { readSettings } from '@/store/settings/getters';
import { thin } from '@/utils';
import { Plotly } from 'vue-plotly';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({
  components: {
    Plotly,
  },
})
// @ts-ignore
export default class Pairwise extends Vue {
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
      return readDisplayTraces(this.$store);
    }
    get activeTraceIDs() {
      return readActiveTraceIDs(this.$store);
    }
    get numberOfActivePrams() {
      let count = 0;
      for (const trace of Object.values(this.traces)) {
        // @ts-ignore
        if (trace.isActive) {
          // @ts-ignore
          for (const param of trace.activeParams) {
            count++;
          }
        }
      }
      return count;
    }
    get layout() {
      const layout = {
          plot_bgcolor: this.$vuetify.theme.dark ? '#1E1E1E' : 'white',
          paper_bgcolor: this.$vuetify.theme.dark ? '#1E1E1E' : 'white',
          hovermode: 'closest',
          dragmode: 'select',

          yaxis: {
            zeroline: false,
            separatethousands: false,
            color: this.$vuetify.theme.dark ? 'white' : '#2c3e50',
            title: {
              standoff: 100,
            },
          },
          xaxis: {
            zeroline: false,
            separatethousands: false,
            color: this.$vuetify.theme.dark ? 'white' : '#2c3e50',
          },
          displayModeBar: true,
          margin: {
          l: 70,
          r: 50,
          b: 40,
          t: 0,
          pad: 0,
          },
          height: this.height,
          width: this.width,
      };
      for (let i = 2; i < this.numberOfActivePrams + 1; i++) {
        console.log(`yaxis${i}`);
        layout[`yaxis${i}`] = {
          zeroline: false,
          separatethousands: false,
          color: this.$vuetify.theme.dark ? 'white' : '#2c3e50',
          title: {
              standoff: 100,
            },
        },
        layout[`xaxis${i}`] = {
          zeroline: false,
          separatethousands: false,
          color: this.$vuetify.theme.dark ? 'white' : '#2c3e50',
        };
      }
      return layout;
    }
    get JointData() {
      const data: any = {};
      const dimensions: any[] = [];
      const settings = readSettings(this.$store);
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
                values: thin(rows, settings.thinningInterval).map((row) =>  row.value),
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
        data.tickfont = {color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'};

        data.type = 'splom';
        // @ts-ignore
        data.marker = {
          size: settings.pairwiseMarkerSize,
          color: settings.palette[0],
          opacity: settings.pairwiseMarkerOpacity,
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

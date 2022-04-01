<template>
    <Plotly :data="JointData" :layout="layout" :toImageButtonOptions="{
          filename: 'marginal',
          width: null,
          height: null,
          format: 'svg'
      }" :displaylogo="false"  :mode-bar-buttons-to-remove="modeBarButtons" :display-mode-bar="true"></Plotly>
</template>

<script lang="ts">
import { readActiveTraceIDs, readTraces } from '@/store/data/getters';
import { Plotly } from 'vue-plotly';
import { Component, Vue } from 'vue-property-decorator';

@Component({
  components: {
    Plotly,
  },
})
export default class Marginal extends Vue {
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
          height: this.numberOfActivePrams > 3 ? this.numberOfActivePrams * 150 : 450,
          displayModeBar: true,
          margin: {
          l: 70,
          r: 50,
          b: 40,
          t: 50,
          pad: 0,
          },
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
      const count = 0;
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
            dimensions.push(
              {
                label: param,
                // @ts-ignore
                values: trace.parameters[param].slice(trace.parameters.state.length * burnIn).map((row) =>  row.value),
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
          size: 5,
          color: '#2980b9',
          opacity: 0.4,
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

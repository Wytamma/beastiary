<template>
    <Plotly id="cumulativeESS" :data="cumulativeESSData" :layout="layout" :toImageButtonOptions="{
          filename: 'cumulativeESS',
          width: null,
          height: null,
          format: 'svg'
      }" :displaylogo="false"  :mode-bar-buttons-to-remove="modeBarButtons" :display-mode-bar="true"></Plotly>
</template>

<script lang="ts">
import { readActiveTraceIDs, readTraces } from '@/store/data/getters';
import { Plotly } from 'vue-plotly';
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import { Trace, Traces } from '../../../interfaces';
@Component({
  components: {
    Plotly,
  },
})
export default class CumulativeESS extends Vue {

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

  get layout() {
    return {
      xaxis: {showgrid: true, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
      yaxis: {showgrid: true, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'},
      plot_bgcolor: this.$vuetify.theme.dark ? '#1E1E1E' : 'white',
      paper_bgcolor: this.$vuetify.theme.dark ? '#1E1E1E' : 'white',
      legend: {orientation: 'h', x: 0.5, y: 1.15, xanchor: 'center', font: {size: 15, color: this.$vuetify.theme.dark ? 'white' : '#2c3e50'}},
      margin: {
        l: 50,
        r: 20,
        b: 30,
        t: 0,
        pad: 0,
      },
      shapes: [

        {
          type: 'line',
          xref: 'paper',
          x0: 0.05,
          y0: 200,
          x1: 0.95,
          y1: 200,
          line: {
            color: '#4CAF50',
            dash: 'dot',
            width: 3,
          },
        },

        {
          type: 'line',
          xref: 'paper',
          x0: 0.05,
          y0: 100,
          x1: 0.95,
          y1: 100,
          line: {
            color: '#ff9800',
            dash: 'dot',
            width: 3,
          },
        },
      ],
      // height: 400,
    };
  }
  get cumulativeESSData() {
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
    let trace: Trace;
    for (trace of Object.values(this.traces)) {
      if (trace.isActive) {
        for (const parameter of Object.values(trace.activeParams)) {
          const parameterCumulativeESSData = this.CumulativeESSdata.filter(
              (e) => e.id === `${trace.id}-${parameter}`,
            ).pop();
          if (parameterCumulativeESSData) {
            data.push({
              x: parameterCumulativeESSData.data.map((row) =>  row.state), // because it's used here
              y: parameterCumulativeESSData.data.map((row) =>  row.value),
              type: 'scatter',
              mode: 'lines+markers',
              connectgaps: true,
              opacity: 0.8,
              name: Object.values(this.traces).filter((t) => t.activeParams.length > 0).length === 1 ? `${parameter}` : `${this.fileName(trace.path)} - ${parameter}`,
              marker: {color: colours[count]},
              hovertemplate: '%{y}',
              showlegend: true,
            });
            count++;
          }
        }
      }
    }
    return data;
  }

  public CumulativeESSdata: Array<{id: string, data: Array<{state: number, value: number}>}> = [];
  // @ts-ignore
  public worker = this.$worker.create(this.actions);

  public actions = [
  { message: 'CumulativeESS', func: (data, burnIn, k) => {

    const dataWithBurnIn = data.slice(
        data.length * (burnIn / 100),
      );

    const cumESSdata: Array<{state: number, value: number}> = [];
    for (let index = k; index < dataWithBurnIn.length; index += k) {
      const values: Array<number | null> = dataWithBurnIn.slice(
        0, index,
      ).map((v) => v.value);

      if (values.includes(null)) {
        return null;
      }
      const stepSize: number = data[1].state - data[0].state;
      const MAX_LAG: number = 2000;
      const nSmaples: number = values.length;
      const maxLag: number = Math.min(nSmaples - 1, MAX_LAG);
      // @ts-ignore
      const valuesMean: number = values.reduce((a, b) => (a + b)) / values.length;
      const gammaStat: number[] = new Array(maxLag); for (let i = 0; i < maxLag; ++i) { gammaStat[i] = 0; }
      let stat = 0.0;
      for (let lag = 0; lag < maxLag; lag++) {
        for (let j = 0; j < (nSmaples - lag); j++) {
          // @ts-ignore
          const del1 = values[j] - valuesMean;
          // @ts-ignore
          const del2 = values[j + lag] - valuesMean;
          gammaStat[lag] = gammaStat[lag] + (del1 * del2);
        }
        gammaStat[lag] = gammaStat[lag] / (nSmaples - lag);
        if (lag === 0) {
          stat = gammaStat[0];
        } else if (lag % 2 === 0) {
          if (gammaStat[lag - 1] + gammaStat[lag] > 0) {
            stat += 2.0 * (gammaStat[lag - 1] + gammaStat[lag]);
          } else {
            break;
          }
        }
      }
      let ACT: number = 0;
      const gStat = gammaStat[0];
      if (gStat > 0 ) {
        ACT = stepSize * stat / gammaStat[0];
      }
      let ESS: number = 1;
      if (ACT !== 0) {
        ESS = (stepSize * nSmaples) / ACT;
      }
      cumESSdata[index] = {state: dataWithBurnIn[index].state, value: ESS};
    }
    return cumESSdata;
  }}];

  get traces(): Traces {
    return readTraces(this.$store);
  }

  public removeESSdata(id) {
    this.CumulativeESSdata = this.CumulativeESSdata.filter((data) => data.id !== id);
  }
  public addESSdata(id, data) {
    this.removeESSdata(id);
    this.CumulativeESSdata.push({id, data});
  }
  public fileName(path) {
    return path.substring(path.lastIndexOf('/') + 1);
  }

  public updateCumulativeESS() {
    let trace: Trace;
    for (trace of Object.values(this.traces)) {
      if (trace.isActive) {
        for (const parameter of Object.values(trace.activeParams)) {
          const burnIn = trace.burnIn;
          const data = trace.parameters[parameter];
          const traceId = trace.id;
          this.worker.postMessage('CumulativeESS', [data, burnIn, 50]) // compute ESS in worker
          .then((res) => {
            this.addESSdata(`${traceId}-${parameter}`, res);
            })
          .catch(console.error);
        }
      }
    }
  }

  @Watch('traces', { immediate: true, deep: true })
  public onTraceChange(val: Traces, oldVal: Traces) {
    this.updateCumulativeESS();
  }

  public mounted() {
    this.updateCumulativeESS();
  }
}
</script>

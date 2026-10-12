<template>
    <Plotly :data="DensityData" :layout="layout" :toImageButtonOptions="{
          filename: 'kernel-density',
          width: null,
          height: null,
          format: 'svg'
      }" :displaylogo="false"  :mode-bar-buttons-to-remove="modeBarButtons" :display-mode-bar="true"></Plotly>
</template>

<script lang="ts">
import { urlFileName } from '@/logParser';
import { readActiveTraceIDs, readTraces } from '@/store/data/getters';
import { Plotly } from 'vue-plotly';
import { Component, Prop, Vue } from 'vue-property-decorator';

const GRID_SIZE = 512;
// Evaluate the density this many bandwidths beyond the min / max sample.
const TAIL_BANDWIDTHS = 3;
// Gaussian kernel contribution is negligible beyond this many bandwidths.
const KERNEL_CUTOFF = 4;

function quantile(sorted: number[], q: number) {
  const pos = (sorted.length - 1) * q;
  const lo = Math.floor(pos);
  const hi = Math.ceil(pos);
  return sorted[lo] + (sorted[hi] - sorted[lo]) * (pos - lo);
}

// Gaussian KDE with Silverman's rule-of-thumb bandwidth. Samples are binned onto a
// fixed grid first so the cost depends on GRID_SIZE rather than on the chain length.
function gaussianKDE(values: number[]) {
  const sorted = values.filter((v) => Number.isFinite(v)).sort((a, b) => a - b);
  const n = sorted.length;
  if (n === 0) {
    return null;
  }

  const mean = sorted.reduce((acc, v) => acc + v, 0) / n;
  const sd = Math.sqrt(sorted.reduce((acc, v) => acc + (v - mean) ** 2, 0) / Math.max(n - 1, 1));
  const iqr = quantile(sorted, 0.75) - quantile(sorted, 0.25);
  const spread = iqr > 0 ? Math.min(sd, iqr / 1.34) : sd;

  let h = 0.9 * spread * Math.pow(n, -0.2);
  if (!(h > 0)) {
    // All samples identical (or a single sample): fall back to a narrow arbitrary bandwidth.
    h = Math.abs(mean) * 0.01 || 0.1;
  }

  const lo = sorted[0] - TAIL_BANDWIDTHS * h;
  const hi = sorted[n - 1] + TAIL_BANDWIDTHS * h;
  const dx = (hi - lo) / (GRID_SIZE - 1);

  const counts = new Array(GRID_SIZE).fill(0);
  for (const v of sorted) {
    counts[Math.round((v - lo) / dx)]++;
  }

  const x: number[] = new Array(GRID_SIZE);
  const y: number[] = new Array(GRID_SIZE).fill(0);
  const norm = 1 / (n * h * Math.sqrt(2 * Math.PI));
  const reach = Math.ceil((KERNEL_CUTOFF * h) / dx);
  for (let j = 0; j < GRID_SIZE; j++) {
    x[j] = lo + j * dx;
    let sum = 0;
    const from = Math.max(0, j - reach);
    const to = Math.min(GRID_SIZE - 1, j + reach);
    for (let k = from; k <= to; k++) {
      if (counts[k] > 0) {
        const u = ((j - k) * dx) / h;
        sum += counts[k] * Math.exp(-0.5 * u * u);
      }
    }
    y[j] = sum * norm;
  }
  return { x, y };
}

function hexToRGBA(hex: string, alpha: number) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

@Component({
  components: {
    Plotly,
  },
})
export default class KernelDensity extends Vue {
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
          yaxis: {
            showticklabels: true,
            zeroline: false,
            rangemode: 'tozero',
            color: this.$vuetify.theme.dark ? 'white' : '#2c3e50',
          },
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
          height: this.height,
          width: this.width,
      };
    }
    get DensityData() {
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
          // @ts-ignore
          const values = trace.parameters[param].slice(trace.parameters.state.length * burnIn).map((row) =>  row.value);
          const kde = gaussianKDE(values);
          const colour = colours[count % colours.length];
          count++;
          if (!kde) {
            continue;
          }
          data.push({
            x: kde.x,
            y: kde.y,
            type: 'scatter',
            mode: 'lines',
            fill: 'tozeroy',
            line: {
                color: colour,
                width: 2,
            },
            fillcolor: hexToRGBA(colour, 0.4),
            name: Object.values(this.traces).filter((t) => t.activeParams.length > 0).length === 1 ? `${param}` : `${this.fileName(trace.path)} - ${param}`,
            hovertemplate: '%{x:.4g}: %{y:.4g}',
            showlegend: true,
          });
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

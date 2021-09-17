<template>
    <v-tooltip  color="black" bottom>
      <template #activator="{ on }">
          <v-chip v-show="ESS" :color="color" text-color="white" v-on="on" small>{{ESS}}</v-chip>
      </template>
      <span>ESS</span>
    </v-tooltip>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import { Data } from '../../interfaces';

@Component
export default class ESSChip extends Vue {
  // @ts-ignore
  @Prop() public data: Data[];
  // @ts-ignore
  @Prop() public burnIn: number;

  public ESS: number | null = null;

  get color() {
    if (this.ESS === null) {
      return 'red';
    }
    if (this.ESS < 100) {
      return 'red';
    } else if (this.ESS < 200) {
      return 'orange';
    } else {
      return 'green';
    }

  }
  public actions = [
  { message: 'ESS', func: (data, burnIn) => {
    const values: Array<number | null> = data.slice(
      data.length * (burnIn / 100),
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
    return ESS;
  }},
  ];

  // @ts-ignore
  public worker = this.$worker.create(this.actions);

  @Watch('data')
  // @ts-ignore
  public dataChanged() {
    this.updateESS();
  }

  @Watch('burnIn')
  // @ts-ignore
  public burnInChanged() {
    this.updateESS();
  }

  public updateESS() {
    const data = this.data;
    const burnIn = this.burnIn;
    this.worker.postMessage('ESS', [data, burnIn]) // compute ESS in worker
    .then((res) => this.ESS = Math.round(res))
    .catch(console.error);
  }

  public mounted() {
    const data = this.data;
    const burnIn = this.burnIn;
    this.worker.postMessage('ESS', [data, burnIn]) // compute ESS in worker
    .then((res) => this.ESS = Math.round(res))
    .catch(console.error);
  }

}
</script>

<template>
    <v-tooltip v-if="ESS" color="black" bottom>
      <template #activator="{ on }">
          <v-chip :color="color" text-color="white" v-on="on" small>{{ESS}}</v-chip>
      </template>
      <span>ESS</span>
    </v-tooltip>
</template>

<script lang="ts">
import { format, mean, zeros } from 'mathjs';
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Data } from '../../interfaces';

@Component
export default class ESSChip extends Vue {
  // @ts-ignore
  @Prop() public data: Data[];
  // @ts-ignore
  @Prop() public burnIn: number;

  get color() {
    if (this.ESS < 100) {
      return 'red';
    } else if (this.ESS < 200) {
      return 'orange';
    } else {
      return 'green';
    }

  }

  get ESS(): number {
    const MAX_LAG: number = 2000;
    const values: Array<number | null> = this.data.slice(
      this.data.length * (this.burnIn / 100),
      ).map((v) => v.value);
    if (values.includes(null)) {
      return 0;
    }
    const nSmaples: number = values.length;
    const stepSize: number = this.data[1].state - this.data[0].state;

    const maxLag: number = Math.min(nSmaples - 1, MAX_LAG);
    // @ts-ignore
    const valuesMean: number = mean(values);
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

    return Math.round(ESS);
  }
}
</script>

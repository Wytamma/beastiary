<template>
<div class="rounded-lg">
    <v-data-table
    class="rounded-lg"
    :headers="headers"
    :items="statistics"
    items-per-page=5
    dense
  >
   <template v-slot:footer.page-text>
        <vue-json-to-csv :json-data="statistics" csv-title="beastiary">
            <v-btn
          color="primary"
          dark
          small
          class="">
            Download
          </v-btn>
        </vue-json-to-csv>
    </template>
  </v-data-table>
  
</div>
</template>

<script lang="ts">
import { readTraces } from '@/store/data/getters';
import { format, mean, median, quantileSeq, sqrt, std, variance } from 'mathjs';
import VueJsonToCsv from 'vue-json-to-csv';
import { Component, Prop, Vue} from 'vue-property-decorator';

@Component({components: {
    VueJsonToCsv,
  }})
export default class StatsTable extends Vue {

    public get headers() {
        return [
            {text: 'Log File', value: 'filename'},
            {text: 'Trace', value: 'param'},
            {text: 'Mean', value: 'mean'},
            {text: 'SEM', value: 'stderr'},
            {text: 'STD', value: 'std'},
            {text: 'Var', value: 'variance'},
            {text: 'Median', value: 'median'},
            {text: '95% HPDI', value: 'HPD'},
            {text: 'ESS', value: 'ESS'},
            {text: 'Samples', value: 'nSamples'},

        ];
    }

    get traces() {
        return readTraces(this.$store);
    }



    get statistics() {
        const statistics: Array<{}> = [];
        for (const trace of Object.values(this.traces)) {
             // @ts-ignore
            for (const param of trace.activeParams) {
                const row: any = {};
                row.filename = this.fileName(trace.path);
                row.filepath = trace.path;
                row.param = param;
                // @ts-ignore
                const stats = this.calculateStats(trace.parameters[param], trace.burnIn);
                // @ts-ignore
                row.mean = format(stats.mean, {notation: 'auto', precision: 5});
                // @ts-ignore
                row.ESS = Math.round(stats.ESS);
                // @ts-ignore
                row.ACT = format(stats.ACT, {notation: 'auto', precision: 5});
                // @ts-ignore
                row.variance = format(stats.variance, {notation: 'auto', precision: 5});
                // @ts-ignore
                row.nSamples = stats.nSamples;
                // @ts-ignore
                row.std = format(stats.std, {notation: 'auto', precision: 5});
                // @ts-ignore
                row.stderr = format(stats.stderr, {notation: 'auto', precision: 5});
                // @ts-ignore
                row.median = format(stats.median, {notation: 'auto', precision: 5});
                // @ts-ignore
                row.quantile = format(stats.quantile, {notation: 'auto', precision: 5});
                // @ts-ignore
                row.HPD = format(stats.HPD, {notation: 'auto', precision: 5});
                // row.HPD = stats.HPD
                // @ts-ignore
                statistics.push(
                    row,
                );
            }
        }
        return statistics;
    }
    public mean(data, burnIn) {
        // TODO: worker
        const values: Array<number | null> = data.slice(
        data.length * (burnIn / 100),
        ).map((v) => v.value);
        if (values.includes(null)) {
            return null;
        }
        // @ts-ignore
        return values.reduce((a, b) => (a + b)) / values.length;
    }
    public fileName(path) {
        return path.substring(path.lastIndexOf('/') + 1);
    }


    public HPDInterval(proportion, values) {
        const sortedValues = values.sort();
        let hpdIndex = 0;
        let minRange = Number.MAX_VALUE;
        const diff = Math.round(proportion * values.length);
        for (let index = 0; index <= (values.length - diff); index++) {
            const minValue = sortedValues[index];
            const maxValue = sortedValues[index + diff - 1];
            const range = Math.abs(maxValue - minValue);
            if (range < minRange) {
                minRange = range;
                hpdIndex = index;
            }
        }
        return [sortedValues[hpdIndex], sortedValues[hpdIndex + diff - 1]];
    }

    public calculateStats(data, burnIn) {
        const values: Array<number | null> = data.slice(
            data.length * (burnIn / 100),
            ).map((v) => v.value);
        if (values.includes(null)) {
            return null;
            }
        const stepSize: number = data[1].state - data[0].state;
        const MAX_LAG: number = 2000;
        const nSamples: number = values.length;
        const maxLag: number = Math.min(nSamples - 1, MAX_LAG);
            // @ts-ignore
        const valuesMean: number = values.reduce((a, b) => (a + b)) / values.length;
        const gammaStat: number[] = new Array(maxLag); for (let i = 0; i < maxLag; ++i) { gammaStat[i] = 0; }
        let stat = 0.0;
        for (let lag = 0; lag < maxLag; lag++) {
            for (let j = 0; j < (nSamples - lag); j++) {
                // @ts-ignore
                const del1 = values[j] - valuesMean;
                // @ts-ignore
                const del2 = values[j + lag] - valuesMean;
                gammaStat[lag] = gammaStat[lag] + (del1 * del2);
            }
            gammaStat[lag] = gammaStat[lag] / (nSamples - lag);
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
            ESS = (stepSize * nSamples) / ACT;
            }
             // @ts-ignore
        const stdSamples = std(values);
        return {
                ESS,
                ACT,
                mean: valuesMean,
                // @ts-ignore
                variance: variance(values),
                nSamples,
                std: stdSamples,
                // @ts-ignore
                stderr: stdSamples / sqrt(nSamples),
                // @ts-ignore
                median: median(values),
                // @ts-ignore
                quantile: quantileSeq(values, [0.025, 0.975]),
                // @ts-ignore
                HPD: this.HPDInterval(0.95, values),
            };
    }
}
</script>

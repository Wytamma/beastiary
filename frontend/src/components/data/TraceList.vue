<template>
  <v-layout
    column
    fill-height
  >
    <v-list
      class="col mb-15 py-0"
      height="100%"
      style="overflow-y: auto;  overflow-x: hidden;"
    >

      <v-list
        class="py-0 "
        v-if="traces.length"
      >
        <v-list-group
          v-for="(trace, i) in traces"
          :key="i"
          @click="setAcitveTrace(trace)"
          color="primary"
        >
          <template v-slot:activator>
            <v-list-item-content class="mb-0">
              <v-list-item-title x-large>
                {{fileName(trace.path)}}
              </v-list-item-title>
              <v-list-item-subtitle class="wrap-text">
                {{trace.path}}
              </v-list-item-subtitle>
              <v-list-item-content>
                <v-chip-group
                  column
                  v-if="Object.keys(trace.parameters).length > 0"
                >
                  <v-tooltip
                    color="black"
                    bottom
                  >
                    <template #activator="{ on }">
                      <v-chip
                        color="cyan"
                        text-color="white"
                        v-on="on"
                        small
                      > {{trace.parameters.state[trace.parameters.state.length - 1].state}} </v-chip>
                    </template>
                    <span>Length</span>
                    </v-tooltip>
                    <v-tooltip
                      color="black"
                      bottom
                    >
                      <template #activator="{ on }">
                        <v-chip
                          color="green"
                          text-color="white"
                          v-on="on"
                          small
                        > {{trace.parameters.state.length}} </v-chip>
                      </template>
                      <span>Samples</span>
                      </v-tooltip>
                      </v-chip-group>
              </v-list-item-content>
            </v-list-item-content>

          </template>
          <div v-if="activeTrace && activeTrace.id === trace.id" >
          <v-col class=" mr-4 mb-0">
            <div>Burn-in {{burnIn}}%</div>
            <v-slider
              v-on:end="setBurnIn"
              v-model="burnIn"
              class="align-center"
              :max="100"
              :min="0"
              hide-details
            > 
              </v-slider>
          </v-col>
          <v-divider></v-divider>
          
          <ParamsPanel />
          </div>
          <div v-else class="text-center my-4">
             <v-progress-circular
              indeterminate
              color="primary"
            ></v-progress-circular>
          </div>
          <v-divider></v-divider>
          </v-list-group>
          </v-list>
          </v-list>
          
    </v-layout>
</template>

<script lang="ts">
import AddTraceButton from '@/components/data/AddTraceButton.vue';
import ParamsPanel from '@/components/data/ParamsPanel.vue';
import {
  dispatchGetSamples,
  dispatchGetTraces,
  dispatchSetActiveTrace,
  dispatchSetBurnIn,
  dispatchSetLoadingSamples,
} from '@/store/data/actions';
import { readActiveTrace, readBurnIn, readLoadingSamples, readTraces } from '@/store/data/getters';
import { Component, Vue } from 'vue-property-decorator';

@Component({
  components: {
    AddTraceButton,
    ParamsPanel,
  },
})
export default class TraceList extends Vue {
  public activeTraces = [];
  public show: boolean = true;
  public interval?: number;
  public burnIn: number = 10;

  get traces() {
    return readTraces(this.$store);
  }

  get activeTrace() {
    return readActiveTrace(this.$store);
  }

  public setBurnIn(value) {
    dispatchSetBurnIn(this.$store, value);
  }

  public async createInterval(trace) {
    this.interval = setInterval( async () => {
      const skip = 'state' in trace.parameters ? trace.parameters.state.length : 0;
      if (!readLoadingSamples(this.$store)) {
            await dispatchGetSamples(this.$store, {
            trace,
            skip,
            limit: 100,
          });
            await dispatchSetActiveTrace(this.$store, trace);
      }}, 2000);
  }

  public async setAcitveTrace(trace) {
    if (this.interval) {
      clearInterval(this.interval);
    }
    const skip =
      'state' in trace.parameters ? trace.parameters.state.length : 0;
    dispatchSetLoadingSamples(this.$store, true);
    await dispatchGetSamples(this.$store, { trace, skip, limit: 2000, all: true });
    await dispatchSetActiveTrace(this.$store, trace);
    dispatchSetLoadingSamples(this.$store, false);
    await this.createInterval(trace);
  }
  public async mounted() {
    await dispatchGetTraces(this.$store);
    // await dispatchLoadAllSamplesAllTraces(this.$store)
  }
  public async beforeDestroy() {
    clearInterval(this.interval);
  }
  public fileName(path) {
    return path.substring(path.lastIndexOf('/') + 1);
  }
}
</script>
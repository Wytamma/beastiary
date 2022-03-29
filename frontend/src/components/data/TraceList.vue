<template>
    <v-list
      class="col mb-0 py-0 my-0 rounded-b-lg no-scrollbar"
      style="overflow-x: hidden;"
    >
        <v-list-group
          v-for="trace in traces"
          :key="trace.id"
          @click="setAcitveTrace(trace)"
          color="primary"
          v-bind:disabled="isloading"
        >
          <template v-slot:activator>
            <v-list-item-content class="mb-0 px-0">
              <v-list-item-title class="text-h6 font-weight-regular">
                {{fileName(trace.path)}}
              </v-list-item-title>
              <v-list-item-subtitle class="wrap-text text-caption">
                {{trace.path}}
              </v-list-item-subtitle>
              <v-list-item-content class="pb-0">
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
                    <v-tooltip
                      color="black"
                      bottom
                      v-if="trace.activeParams.length"
                    >
                      <template #activator="{ on }">
                        <v-chip
                          color="red"
                          text-color="white"
                          v-on="on"
                          @click:close="setActiveParams(trace)"
                          small
                          close
                        > {{trace.activeParams.length}}</v-chip>
                      </template>
                      <span>Active</span>
                    </v-tooltip>
                  </v-chip-group>
              </v-list-item-content>
            </v-list-item-content>

          </template>
          <div style="overflow-x: hidden !important; overflow-y: auto !important;" v-if="openTraceID === trace.id && activeTraceIDs.includes(trace.id)">
            <v-col class=" mr-4 mb-0">
              <div>Burn-in {{burnIn[trace.id]}}%</div>
              <v-slider
                v-on:change="setBurnIn($event, trace.id)"
                v-model="burnIn[trace.id]"
                class="align-center"
                :max="100"
                :min="0"
                hide-details
              > 
                </v-slider>
            </v-col>
            <v-divider class="my-0"></v-divider>
            <div style="overflow-x:hidden" >
              <ParamsPanel :trace="trace" height="400px" />
            </div>
            
          </div>
          <div v-show="!activeTraceIDs.includes(trace.id)" class="text-center my-4">
             <v-progress-circular
              indeterminate
              color="primary"
            ></v-progress-circular>
          </div>
          <v-divider></v-divider>
          </v-list-group>
          </v-list>
          
</template>

<style>
.no-scrollbar {
  overflow-y: scroll; /* Add the ability to scroll */
}
/* Hide scrollbar for Chrome, Safari and Opera */
.no-scrollbar::-webkit-scrollbar {
    display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.no-scrollbar {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
</style>

<script lang="ts">
import AddTraceButton from '@/components/data/AddTraceButton.vue';
import ParamsPanel from '@/components/data/ParamsPanel.vue';
import {
  dispatchGetSamples,
  dispatchGetTraces,
  dispatchSetActiveParams,
  dispatchSetActiveTrace,
  dispatchSetBurnIn,
  dispatchSetLoadingSamples,
} from '@/store/data/actions';
import { readActiveTraceIDs, readLoadingSamples, readTraces } from '@/store/data/getters';
import { Component, Vue } from 'vue-property-decorator';

@Component({
  components: {
    AddTraceButton,
    ParamsPanel,
  },
})
export default class TraceList extends Vue {
  public activeTraces = [];
  public openTraceID = null;
  public show: boolean = true;
  public interval?: number;
  // this is so dumb need a better way to do dynamic v-model defualts
  public burnIn = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10];

  get traces() {
    const traces = readTraces(this.$store);
    return traces;
  }

  get activeTraceIDs() {
    return readActiveTraceIDs(this.$store);
  }

  get isloading() {
    return readLoadingSamples(this.$store);
  }

  public setActiveParams(trace) {
      dispatchSetActiveParams(this.$store, {traceID: trace.id, params: []});
  }

  public setBurnIn(value, traceID) {
    dispatchSetBurnIn(this.$store, {traceID, burnIn: value});
  }

  public async setAcitveTrace(trace) {
    this.openTraceID = trace.id;
    const skip =
      'state' in trace.parameters ? trace.parameters.state.length : 0;
    if (this.activeTraceIDs === [] || ( this.activeTraceIDs && !(this.activeTraceIDs.includes(trace.id)))) {
      // have not loaded or just started or part way though loading
      if (!readLoadingSamples(this.$store)) {
        // not loading and no active so load
        dispatchSetLoadingSamples(this.$store, true);
        await dispatchGetSamples(this.$store, { trace, skip, limit: 4000, all: true });
        await dispatchSetActiveTrace(this.$store, trace);
        dispatchSetLoadingSamples(this.$store, false);
        // await this.createInterval(trace);
      }
    }
  }

  public async mounted() {
    await dispatchGetTraces(this.$store);
    this.interval = setInterval( async () => {
      for (const id of Object.keys(this.traces)) {
        const trace = this.traces[id];
        if (trace.isActive === true) {
          const skip = 'state' in trace.parameters ? trace.parameters.state.length : 0;
          await dispatchGetSamples(this.$store, {trace, skip, limit: 1000});
          }
        }
      }, 5000);
  }
  public async beforeDestroy() {
    clearInterval(this.interval);
  }
  public fileName(path) {
    return path.substring(path.lastIndexOf('/') + 1);
  }
}
</script>
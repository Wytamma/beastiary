<template>
  <v-card class="elevation-12 ma-2" outlined>
    <v-toolbar dark color="primary">
      <v-toolbar-title> Traces </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click="show = !show">
        <v-icon>{{ show ? "mdi-chevron-up" : "mdi-chevron-down" }}</v-icon>
      </v-btn>
    </v-toolbar>
    <v-expand-transition>
      <div v-show="show">
        <v-card-text style="max-height: 300px; overflow: auto">
          <v-list dense v-if="traces.length">
            <v-list-item-group
              color="primary"
            >
              <v-list-item
                v-for="(trace, i) in traces"
                :key="i"
                @click="setAcitveTrace(trace)"
              >
                <template>
                  <v-list-item-content>
                    <v-list-item-title style="white-space: normal;">
                      {{fileName(trace.path)}}
                    </v-list-item-title>
                    <v-list-item-subtitle style="white-space: normal;">
                      {{trace.path}}
                    </v-list-item-subtitle>
                    <v-list-item-content>
                      <v-chip-group
                          column
                        >
                          <v-tooltip v-if="Object.keys(trace.parameters).length > 0" color="black" bottom>
                            <template #activator="{ on }">
                                <v-chip color="cyan" text-color="white" v-on="on" small> {{trace.parameters.state[trace.parameters.state.length - 1].state}} </v-chip>
                            </template>
                            <span>Length</span>
                          </v-tooltip>
                          <v-tooltip v-if="Object.keys(trace.parameters).length > 0" color="black" bottom>
                            <template #activator="{ on }">
                                <v-chip color="green" text-color="white" v-on="on" small> {{trace.parameters.state.length}} </v-chip>
                            </template>
                            <span>Samples</span>
                          </v-tooltip>
                      </v-chip-group>            
                    </v-list-item-content>
                  </v-list-item-content>
                </template>
              </v-list-item>
            </v-list-item-group>
          </v-list>
          <div v-else>No traces</div>
        </v-card-text>
      </div>
    </v-expand-transition>
    <v-card-actions>
      <v-spacer></v-spacer>
      <AddTraceButton></AddTraceButton>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {
  dispatchGetTraces,
  dispatchSetActiveTrace,
  dispatchGetSamples,
} from '@/store/data/actions';
import { readTraces } from '@/store/data/getters';
import AddTraceButton from '@/components/data/AddTraceButton.vue';

@Component({
  components: {
    AddTraceButton,
  },
})
export default class TracesPanel extends Vue {
  public activeTraces = [];
  public show: boolean = true;
  public interval?: number;

  get traces() {
    return readTraces(this.$store);
  }
  public async setAcitveTrace(trace) {
    if (this.interval) {
      clearInterval(this.interval);
    }
    const skip = 'state' in trace.parameters ? trace.parameters.state.length : 0;
    await dispatchGetSamples(this.$store, {trace, skip, limit: 1000000});
    await dispatchSetActiveTrace(this.$store, trace);
    this.interval = setInterval(() =>  {
      const intervalSkip = 'state' in trace.parameters ? trace.parameters.state.length : 0;
      dispatchGetSamples(this.$store, {trace, skip: intervalSkip, limit: 1000});
      dispatchSetActiveTrace(this.$store, trace);
    }, 1000);

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

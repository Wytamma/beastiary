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
              v-model="activeTraces"
            >
              <v-list-item
                v-for="(trace, i) in traces"
                :key="i"
                @click="setAcitveTrace(trace)"
              >
                <template>
                  <v-list-item-content>
                    <v-list-item-title>{{
                      fileName(trace.path)
                    }}</v-list-item-title>
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
import AddTraceButton from '@/components/AddTraceButton.vue';
@Component({
  components: {
    AddTraceButton,
  },
})
export default class TracesPanel extends Vue {
  public activeTraces = [];
  public show: boolean = true;
  get traces() {
    return readTraces(this.$store);
  }
  public async setAcitveTrace(trace) {
    const skip = 'state' in trace.parameters ? trace.parameters.state.length : 0;
    await dispatchGetSamples(this.$store, {trace, skip, limit: 1000000});
    await dispatchSetActiveTrace(this.$store, trace);


  }
  public async mounted() {
    await dispatchGetTraces(this.$store);
    // await dispatchLoadAllSamplesAllTraces(this.$store)
  }
  public fileName(path) {
    return path.substring(path.lastIndexOf('/') + 1);
  }
}
</script>

<template>
  <div>
    <input
      ref="reloadFileInput"
      type="file"
      accept=".log,.txt,.tsv,.csv"
      style="display: none"
      @change="onReloadFileInputChange"
    />
    <v-list
      class="col mb-0 py-0 my-0 rounded-b-lg no-scrollbar"
      style="overflow-x: hidden;"
    >
      <v-list-group
        v-for="trace in traces"
        :key="trace.id"
        class="trace-group"
        @click="setAcitveTrace(trace)"
        color="primary"
        :disabled="isLoading"
      >
        <template v-slot:activator>
          <v-list-item-content class="mb-0 px-0">
            <div class="d-flex align-start">
              <div class="trace-leading-icon mr-0 mt-2 flex-shrink-0">
                <v-icon medium class="trace-file-icon">mdi-file-outline</v-icon>
                <v-btn
                  icon
                  small
                  class="trace-close-btn"
                  title="Close trace"
                  @click.stop="removeTrace(trace)"
                >
                  <v-icon small>mdi-close</v-icon>
                </v-btn>
              </div>
              <div class="min-width-0 flex-grow-1">
                <v-list-item-title class="text-h6 font-weight-regular">
                  {{ fileName(trace.path) }}
                </v-list-item-title>
                <v-list-item-subtitle style="word-break: break-all;" class="wrap-text text-caption overflow-x-scroll">
                  {{ trace.path }}
                </v-list-item-subtitle>
              </div>
            </div>
            <v-list-item-content class="pb-0">
              <div class="d-flex align-center" v-if="Object.keys(trace.parameters).length > 0">
                <v-chip-group column>
                  <v-tooltip color="black" bottom>
                    <template #activator="{ on }">
                      <v-chip color="cyan" text-color="white" v-on="on" small>
                        {{ trace.parameters.state[trace.parameters.state.length - 1].state }}
                      </v-chip>
                    </template>
                    <span>Length</span>
                  </v-tooltip>
                  <v-tooltip color="black" bottom>
                    <template #activator="{ on }">
                      <v-chip color="green" text-color="white" v-on="on" small>
                        {{ trace.parameters.state.length }}
                      </v-chip>
                    </template>
                    <span>Samples</span>
                  </v-tooltip>
                  <v-tooltip color="black" bottom>
                    <template #activator="{ on }">
                      <v-chip
                        :color="traceSourceColor(trace.source)"
                        text-color="white"
                        v-on="on"
                        small
                      >
                        {{ trace.source }}
                      </v-chip>
                    </template>
                    <span>Trace source</span>
                  </v-tooltip>
                  <v-tooltip color="black" bottom v-if="trace.source === 'local' && trace.localFile?.autoReload">
                    <template #activator="{ on }">
                      <v-chip color="teal" text-color="white" v-on="on" small>
                        auto
                      </v-chip>
                    </template>
                    <span>Client-side auto-reload enabled</span>
                  </v-tooltip>
                  <v-tooltip color="black" bottom v-if="trace.activeParams.length">
                    <template #activator="{ on }">
                      <v-chip
                        color="red"
                        text-color="white"
                        v-on="on"
                        @click:close="setActiveParams(trace)"
                        small
                        close
                      >
                        {{ trace.activeParams.length }}
                      </v-chip>
                    </template>
                    <span>Active</span>
                  </v-tooltip>
                </v-chip-group>
                <v-progress-circular
                  indeterminate
                  color="primary"
                  size="20"
                  class="pl-1"
                  v-if="trace.isLoading"
                ></v-progress-circular>
              </div>
            </v-list-item-content>
          </v-list-item-content>
        </template>
        <div
          v-if="openTraceID === trace.id && activeTraceIDs.includes(trace.id)"
          style="overflow-x: hidden !important; overflow-y: auto !important;"
        >
          <div class="my-3 mx-2">
            <div class="d-flex align-center">
              <div>Burn-in</div>
              <v-slider
                v-model="burnIn[trace.id]"
                :max="99"
                :min="0"
                hide-details
                @change="setBurnIn($event, trace.id)"
              ></v-slider>
              <span class="fixed-width">{{ burnIn[trace.id] }}</span>%
              <v-btn
                v-if="trace.source === 'local'"
                icon
                small
                class="ml-2"
                title="Reload file"
                @click.stop="reloadTrace(trace)"
              >
                <v-icon small>mdi-refresh</v-icon>
              </v-btn>
            </div>
          </div>
          <v-divider class="my-0"></v-divider>
          <div style="overflow-x:hidden">
            <ParamsPanel :trace="trace" height="400px" />
          </div>
        </div>
        <div v-show="!('state' in trace.parameters)" class="text-center my-4">
          <v-progress-circular
            indeterminate
            color="primary"
          ></v-progress-circular>
        </div>
        <v-divider></v-divider>
      </v-list-group>
    </v-list>
  </div>
</template>

<style>
.no-scrollbar {
  overflow-y: scroll;
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}

.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.fixed-width {
  display: inline-block;
  width: 1.2em;
  text-align: right;
}

.trace-group > .v-list-group__header {
  padding-left: 8px !important;
  padding-right: 8px !important;
}

.trace-leading-icon {
  position: relative;
  width: 28px;
  height: 28px;
}

.trace-file-icon,
.trace-close-btn {
  position: absolute !important;
  top: 0;
  left: 0;
  transition: opacity 0.15s ease-in-out;
  color: inherit !important;
}

.trace-file-icon {
  opacity: 1;
}

.trace-close-btn {
  opacity: 0;
}

.trace-close-btn .v-icon {
  color: inherit !important;
}

.trace-group > .v-list-group__header:hover .trace-close-btn,
.trace-group > .v-list-group__header:focus-within .trace-close-btn {
  opacity: 1;
}

.trace-group > .v-list-group__header:hover .trace-file-icon,
.trace-group > .v-list-group__header:focus-within .trace-file-icon {
  opacity: 0;
}
</style>

<script lang="ts">
import ParamsPanel from '@/components/data/ParamsPanel.vue';
import { urlFileName } from '@/logParser';
import { runtimeCapabilities } from '@/runtime';
import {
  dispatchGetSamples,
  dispatchGetTraces,
  dispatchPollTraces,
  dispatchRemoveTrace,
  dispatchReloadLocalTrace,
  dispatchSetActiveParams,
  dispatchSetActiveTrace,
  dispatchSetBurnIn,
  dispatchSetLoadingSamples,
} from '@/store/data/actions';
import { readActiveTraceIDs, readLoadingSamples, readTraces } from '@/store/data/getters';
import { Trace } from '@/interfaces';
import { Component, Vue } from 'vue-property-decorator';

@Component({
  components: {
    ParamsPanel,
  },
})
export default class TraceList extends Vue {
  public openTraceID: number | null = null;
  public interval?: number;
  public reloadingTraceID: number | null = null;
  public burnIn = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10];

  get traces() {
    return readTraces(this.$store);
  }

  get activeTraceIDs() {
    return readActiveTraceIDs(this.$store);
  }

  get isLoading() {
    return readLoadingSamples(this.$store);
  }

  public setActiveParams(trace: Trace) {
    dispatchSetActiveParams(this.$store, { traceID: trace.id, params: [] });
  }

  public traceSourceColor(source: Trace['source']) {
    if (source === 'local') {
      return 'deep-purple';
    }
    if (source === 'url') {
      return 'indigo';
    }
    return 'blue-grey';
  }

  public setBurnIn(value: number, traceID: number) {
    dispatchSetBurnIn(this.$store, { traceID, burnIn: value });
  }

  public async setAcitveTrace(trace: Trace) {
    this.openTraceID = trace.id;
    this.syncBurnIn(trace);
    if (this.activeTraceIDs.includes(trace.id)) {
      return;
    }

    if (trace.source === 'local') {
      await dispatchSetActiveTrace(this.$store, trace);
      return;
    }

    const skip = 'state' in trace.parameters ? trace.parameters.state.length : 0;
    if (!readLoadingSamples(this.$store)) {
      dispatchSetLoadingSamples(this.$store, { traceID: trace.id, loading: true });
      await dispatchSetActiveTrace(this.$store, trace);
      await dispatchGetSamples(this.$store, { trace, skip, limit: 2500, all: true });
      dispatchSetLoadingSamples(this.$store, { traceID: trace.id, loading: false });
    }
  }

  public async reloadTrace(trace: Trace) {
    if (trace.localFile?.handleId) {
      await dispatchReloadLocalTrace(this.$store, { traceID: trace.id });
      return;
    }
    this.reloadingTraceID = trace.id;
    const input = this.$refs.reloadFileInput as HTMLInputElement;
    input.value = '';
    input.click();
  }

  public async removeTrace(trace: Trace) {
    if (this.openTraceID === trace.id) {
      this.openTraceID = null;
    }
    if (this.reloadingTraceID === trace.id) {
      this.reloadingTraceID = null;
    }
    await dispatchRemoveTrace(this.$store, { traceID: trace.id });
  }

  public async onReloadFileInputChange(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (file && this.reloadingTraceID !== null) {
      await dispatchReloadLocalTrace(this.$store, { traceID: this.reloadingTraceID, file });
    }
    this.reloadingTraceID = null;
  }

  public async mounted() {
    await dispatchGetTraces(this.$store);
    Object.values(this.traces).forEach((trace) => this.syncBurnIn(trace));
    this.interval = window.setInterval(async () => {
      await dispatchPollTraces(this.$store);
    }, runtimeCapabilities.supportsPolling ? 5000 : 4000);
  }

  public beforeDestroy() {
    clearInterval(this.interval);
  }

  public fileName(path: string) {
    return urlFileName(path);
  }

  private syncBurnIn(trace: Trace) {
    if (typeof this.burnIn[trace.id] !== 'number') {
      this.$set(this.burnIn, trace.id, trace.burnIn);
    }
  }
}
</script>

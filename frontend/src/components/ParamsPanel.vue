<template>
      <v-card style="overflow: auto" class="elevation-12 ma-2 mt-2" outlined v-if="activeTrace">
    <v-toolbar dark color="primary">
      <v-toolbar-title> Parameters </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-expand-transition>
      <div >
        <v-card-text style="max-height: 350px ;overflow: auto">
          <v-list dense >
            <v-list-item-group
              color="primary"
            >
              <v-list-item
                v-for="(param, i) in parameters"
                :key="i"
                @click="setActiveParam(param)"
              >
                <template>
                  <v-list-item-content>
                    <v-list-item-title>{{
                      param
                    }}</v-list-item-title>
                  </v-list-item-content>
                </template>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';
import { readParamsOfActiveTrace, readActiveTrace } from '@/store/data/getters';
import { dispatchSetActiveParam } from '@/store/data/actions';

@Component
export default class ParamsPanel extends Vue {
    // public parameters: Array<string> = []
    get activeTrace() {
        return readActiveTrace(this.$store);
    }
    get parameters() {
        return readParamsOfActiveTrace(this.$store);
    }

    public async setActiveParam(param) {
      await dispatchSetActiveParam(this.$store, param);
    }
    @Watch('activeParams', { deep: true })
    public onChildChanged() {
      // this.parameters = this.$store.getters.paramsOfActiveTrace
    }
}
</script>

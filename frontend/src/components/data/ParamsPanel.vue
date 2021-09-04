<template>
    <v-list-item-group style="height:400px; overflow:auto" class="mb-0" dense two-line v-model="selectedItem">
        <div v-for="(param, i) in parameters"
          :key="i"
          @click="setActiveParam(param)">
          
          <!-- <v-divider class="mx-4" v-if="i > 0" ></v-divider> -->
        <v-list-item >
          <template v-slot:default="{ active }">
          <v-list-item-action>
              <v-checkbox :input-value="active"></v-checkbox>
            </v-list-item-action>
            <!-- <v-list-item-action>
              <v-icon>mdi-phone</v-icon>
            </v-list-item-action> -->
            <v-list-item-content class="mb-0">
              <v-list-item-title>{{param}}</v-list-item-title>
              
            </v-list-item-content>
           </template>
        </v-list-item>
        </div>
    </v-list-item-group>
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

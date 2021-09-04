<template>
    <v-list-item-group style="height:400px; overflow:auto" class="mb-0" dense v-model="selectedItem">
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
            <!-- <v-list-item-icon>
              <v-tooltip color="black" bottom>
                <template #activator="{ on }">
                    <v-chip v-on="on" small>{{ paramMean(param) }}</v-chip>
                </template>
                <span>Mean</span>
              </v-tooltip>
            </v-list-item-icon> -->
           </template>
        </v-list-item>
        </div>
    </v-list-item-group>
</template>

<script lang="ts">
import { dispatchSetActiveParam } from '@/store/data/actions';
import { readActiveTrace, readBurnIn, readParamsOfActiveTrace } from '@/store/data/getters';
import { format, mean } from 'mathjs';
import { Component, Vue, Watch } from 'vue-property-decorator';

@Component
export default class ParamsPanel extends Vue {

    get activeTrace() {
        return readActiveTrace(this.$store);
    }
    get parameters() {
        return readParamsOfActiveTrace(this.$store);
    }

    /**
     * paramMean
     */
    // public paramMean(param) {
    //   const trace = this.activeTrace;
    //   const burnIn = readBurnIn(this.$store) / 100;
    //   if (trace && trace.parameters.param) {
    //       return format(
    //         mean(
    //           trace.parameters[param].slice(
    //             trace.parameters.state.length * burnIn,
    //             ).map((row) =>  row.value),
    //         ),
    //       {precision: 4});
    //   }
    //   return null;
    // }

    public async setActiveParam(param) {
      await dispatchSetActiveParam(this.$store, param);
    }
    @Watch('activeParams', { deep: true })
    public onChildChanged() {
      // this.parameters = this.$store.getters.paramsOfActiveTrace
    }
}
</script>

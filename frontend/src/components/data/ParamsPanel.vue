<template>
  <v-list dense class="my-0 py-0">
    <v-list-item-group style="height:400px; overflow:auto" >
      <div v-for="(data, param) in trace.parameters"
          :key="param"
          >
          <!-- <v-divider class="mx-4" v-if="i > 0" ></v-divider> -->
      <v-lazy
        :options="{
          threshold: .9
        }"
        transition="fade-transition"
        
        :value="param"
      >
        <v-list-item >
          <template>
            <v-list-item-action>
              <v-checkbox v-model="activeParams" multiple :value="param" ></v-checkbox>
            </v-list-item-action>
            <v-list-item-content @click="setActiveParams([param])" class="my-0">
              <v-list-item-title>{{param}}</v-list-item-title>
            </v-list-item-content>
            <!-- <v-list-item-icon class="mt-3 d-flex align-center ">
              <v-tooltip color="black" bottom>
                <template #activator="{ on }">
                    <v-chip v-on="on" small>{{paramMean(param)}}</v-chip>
                </template>
                <span>Mean</span>
              </v-tooltip>
            </v-list-item-icon> -->
           </template>
        </v-list-item>
        </v-lazy>
        </div>
        
    </v-list-item-group>
  </v-list>
</template>

<script lang="ts">
import { dispatchSetActiveParams } from '@/store/data/actions';
import { format, mean } from 'mathjs';
import { Component, Prop, Vue} from 'vue-property-decorator';
import { Trace } from '../../interfaces';

@Component({})
export default class ParamsPanel extends Vue {
    // @ts-ignore
    @Prop(Trace) public trace;

    public isActive = false;

    get activeParams() {
      return this.trace.activeParams;
    }

    set activeParams(params) {
      dispatchSetActiveParams(this.$store, {traceID: this.trace.id, params});
    }

    public setActiveParams(params) {
      dispatchSetActiveParams(this.$store, {traceID: this.trace.id, params});
    }

    public paramMean(param) {
      console.log(param);

      const burnIn = this.trace.burnIn;
      const data = this.trace.parameters[param].slice(
            this.trace.parameters.state.length * burnIn / 100,
            ).map((row) =>  row.value).filter(Boolean); // nulls (inf etc) not in mean
      if (data.length > 0) {
          // @ts-ignore: No overload matches this call error
          return format(mean(data), {precision: 4});
      }
      return null;
    }

}
</script>

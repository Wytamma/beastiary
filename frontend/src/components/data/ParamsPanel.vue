<template>
    <v-list style="max-height: 55vh;overflow: auto;" dense class="my-0 py-0" >
      <v-list-item-group >
        <div v-for="(data, param) in trace.parameters"
            :key="param"
            v-if="param != 'state'">
          <v-list-item class="ma-0" >
            <template>
              <v-list-item-action class="my-1">
                <v-checkbox v-model="activeParams" multiple :value="param" ></v-checkbox>
              </v-list-item-action>
              <v-list-item-content @click="setActiveParams([param])" class="mt-0">
                <v-list-item-title>{{param}}</v-list-item-title>
              </v-list-item-content>
              <v-list-item-icon class="mb-1 mt-2 d-flex align-center ">
                <ESSChip :data="data" :burnIn="trace.burnIn"/>
              </v-list-item-icon>
            </template>
          </v-list-item>
          </div>
          
      </v-list-item-group>
    </v-list>
</template>

<script lang="ts">
import ESSChip from '@/components/data/ESSChip.vue';
import { dispatchSetActiveParams } from '@/store/data/actions';
import { format, mean } from 'mathjs';
import { Component, Prop, Vue} from 'vue-property-decorator';
import { Trace } from '../../interfaces';

@Component({components: {
    ESSChip,
  }})
export default class ParamsPanel extends Vue {
    // @ts-ignore
    @Prop(Trace) public trace;

    public isActive = false;

    get height() {
        switch (this.$vuetify.breakpoint.name) {
          case 'xs': return 400
          case 'sm': return 400
          case 'md': return 400
          case 'lg': return 400
          case 'xl': return 600
        }
    }
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

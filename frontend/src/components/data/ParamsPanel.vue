<template>
    <v-list style="max-height: 55vh;overflow: auto;" dense class="my-0 py-0" >
      <div class="px-2 py-2">
        <div class="d-flex align-center">
          <v-text-field
            append-icon="mdi-magnify"
            clearable
            dense
            hide-details
            outlined
            placeholder="Filter parameters"
            @input="queueFilterUpdate"
            @click:clear="clearFilter"
          ></v-text-field>
        </div>
      </div>
      <v-list-item-group >
        <div v-for="param in parameterNames"
            :key="param">
          <v-list-item v-show="visibleParamSet.has(param)" @click="setActiveParams([param])"  class="ma-0" >
            <template>
              <v-list-item-action class="my-1" @click.stop>
                <v-checkbox v-model="activeParams" multiple :value="param" @click.stop></v-checkbox>
              </v-list-item-action>
              <v-list-item-content class="mt-0">
                <v-list-item-title>{{param}}</v-list-item-title>
              </v-list-item-content>
              <v-list-item-icon class="mb-1 mt-2 d-flex align-center ">
                <ESSChip :data="trace.parameters[param]" :burnIn="trace.burnIn"/>
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
    public paramFilter = '';
    public filterTimer: number | null = null;

    get height() {
        switch (this.$vuetify.breakpoint.name) {
          case 'xs': return 400;
          case 'sm': return 400;
          case 'md': return 400;
          case 'lg': return 400;
          case 'xl': return 600;
        }
    }
    get activeParams() {
      return this.trace.activeParams;
    }

    set activeParams(params) {
      dispatchSetActiveParams(this.$store, {traceID: this.trace.id, params});
    }

    get parameterNames() {
      return Object.keys(this.trace.parameters)
        .filter((param) => param !== 'state');
    }

    get visibleParamNames() {
      const filter = this.paramFilter.trim().toLowerCase();
      return !filter
        ? this.parameterNames
        : this.parameterNames.filter((param) => param.toLowerCase().includes(filter));
    }

    get visibleParamSet() {
      return new Set(this.visibleParamNames);
    }

    public setActiveParams(params) {
      dispatchSetActiveParams(this.$store, {traceID: this.trace.id, params});
    }

    public queueFilterUpdate(value: string) {
      if (this.filterTimer !== null) {
        window.clearTimeout(this.filterTimer);
      }
      if (!value) {
        this.paramFilter = '';
        this.filterTimer = null;
        return;
      }
      this.filterTimer = window.setTimeout(() => {
        this.paramFilter = value;
        this.filterTimer = null;
      }, 250);
    }

    public clearFilter() {
      if (this.filterTimer !== null) {
        window.clearTimeout(this.filterTimer);
        this.filterTimer = null;
      }
      this.paramFilter = '';
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

    public beforeDestroy() {
      if (this.filterTimer !== null) {
        window.clearTimeout(this.filterTimer);
      }
    }

}
</script>

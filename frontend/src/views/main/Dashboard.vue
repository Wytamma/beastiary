<template>
      <v-layout fill-height>
      <v-row
        no-gutters
      > 
        <v-col cols="3">
          <v-card
            class="elevation-12 ma-2"
            outlined
          >
            <v-toolbar dark color="primary">
              <v-toolbar-title>Traces</v-toolbar-title>
            </v-toolbar>
            <v-card-text style="max-height: 300px;overflow:auto;" >
                <TracesPanel />
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <AddTraceButton></AddTraceButton>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col cols="9">
          <v-card>
          </v-card>
        </v-col>
      </v-row>
</v-layout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { readUserProfile } from '@/store/main/getters';
import TracesPanel from '@/components/TracesPanel.vue';
import AddTraceButton from '@/components/AddTraceButton.vue';

@Component({
  components: {
    TracesPanel,
    AddTraceButton,
  },
})
export default class Dashboard extends Vue {}
</script>

<template>
  <v-dialog v-model="dialog" max-width="720px" scrollable>
    <template #activator="{ on, attrs }">
      <v-btn icon v-bind="attrs" v-on="on" title="Settings" aria-label="Settings">
        <v-icon>mdi-cog</v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title class="text-h5">Settings</v-card-title>
      <v-divider></v-divider>
      <v-card-text style="max-height: 70vh" class="pt-4">
        <div v-for="(section, sectionIndex) in sections" :key="section.title" class="mb-6">
          <v-divider v-if="sectionIndex > 0" class="mb-4"></v-divider>
          <div class="text-h6 mb-1">{{ section.title }}</div>
          <div v-if="section.note" class="text-caption mb-3">{{ section.note }}</div>

          <div v-if="section.palette" class="mb-4">
            <div class="text-subtitle-1 font-weight-medium mb-2">Plot colours</div>
            <v-select
              :items="presetItems"
              :value="currentPreset"
              label="Palette"
              dense
              outlined
              hide-details
              class="mb-3"
              @change="applyPreset"
            ></v-select>
            <div class="d-flex flex-wrap mb-2">
              <v-menu
                v-for="(colour, index) in settings.palette"
                :key="`${paletteVersion}-${index}`"
                :close-on-content-click="false"
                offset-y
              >
                <template #activator="{ on }">
                  <v-btn
                    v-on="on"
                    fab
                    x-small
                    elevation="1"
                    class="ma-1"
                    :color="colour"
                    :aria-label="`Edit colour ${index + 1}`"
                  ></v-btn>
                </template>
                <v-card>
                  <v-color-picker
                    :value="colour"
                    mode="hexa"
                    hide-mode-switch
                    show-swatches
                    @input="setColour(index, $event)"
                  ></v-color-picker>
                  <v-btn
                    block
                    text
                    color="error"
                    :disabled="settings.palette.length <= 1"
                    @click="removeColour(index)"
                  >
                    <v-icon left>mdi-delete</v-icon>Remove colour
                  </v-btn>
                </v-card>
              </v-menu>
              <v-btn
                fab
                x-small
                outlined
                class="ma-1"
                title="Add colour"
                aria-label="Add colour"
                @click="addColour"
              >
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </div>
            <div class="text-caption">
              Click a colour to change or remove it, or use + to add one. Colours are assigned to parameters in order
              and repeat if there are more parameters than colours.
            </div>
          </div>

          <div v-for="group in section.groups" :key="group.title" class="mb-4">
            <div class="text-subtitle-1 font-weight-medium mb-1">{{ group.title }}</div>
            <div v-if="group.note" class="text-caption mb-3">{{ group.note }}</div>
            <template v-for="field in group.fields">
              <v-slider
                v-if="field.step"
                :key="field.key"
                :label="field.label"
                :hint="field.hint"
                :min="limits[field.key].min"
                :max="limits[field.key].max"
                :step="field.step"
                :value="settings[field.key]"
                persistent-hint
                thumb-label
                class="mb-4"
                @change="update(field.key, $event)"
              ></v-slider>
              <v-text-field
                v-else
                :key="field.key"
                :label="field.label"
                :hint="field.hint"
                :value="settings[field.key]"
                :rules="rules(field.key)"
                type="number"
                dense
                outlined
                persistent-hint
                class="mb-2"
                @change="updateFromText(field.key, $event)"
              ></v-text-field>
            </template>
          </div>
        </div>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-btn text @click="reset">Reset to defaults</v-btn>
        <v-spacer></v-spacer>
        <v-btn text color="primary" @click="dialog = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { isValidNumber, nextPaletteColour, PALETTE_PRESETS, SETTING_LIMITS } from '@/store/settings/defaults';
import { readSettings } from '@/store/settings/getters';
import { commitResetSettings, commitUpdateSettings } from '@/store/settings/mutations';
import { NumericSettingKey } from '@/store/settings/state';
import { Component, Vue } from 'vue-property-decorator';

interface Field {
  key: NumericSettingKey;
  label: string;
  hint: string;
  // Fields with a step are shown as sliders, the rest as number inputs.
  step?: number;
}

interface Group {
  title: string;
  note?: string;
  fields: Field[];
}

interface Section {
  title: string;
  note?: string;
  // Show the colour palette editor at the top of the section.
  palette?: boolean;
  groups: Group[];
}

const COLOUR_DEBOUNCE_MS = 150;

@Component
export default class SettingsDialog extends Vue {
  public dialog = false;
  public limits = SETTING_LIMITS;
  // Bumped when a colour is removed so the colour menus are recreated (closing any open one) instead of being
  // reused with shifted indices.
  public paletteVersion = 0;

  // The plot groups follow the order of the tabs on the dashboard (Trace, Violin, Histogram, Density, Pairwise,
  // Parallel, ESS). Trace, Violin and Parallel have no settings of their own.
  public sections: Section[] = [
    {
      title: 'General',
      palette: true,
      groups: [
        {
          title: 'Polling',
          note: 'How open traces are kept up to date. Changes apply immediately.',
          fields: [
            {
              key: 'pollingInterval', label: 'Polling interval (seconds)',
              hint: 'How often open traces are checked for new samples, or for changes to auto-reloaded local files.',
            },
            {
              key: 'pollingBatchSize', label: 'Batch size (samples)',
              hint: 'Most samples requested from the server in one request. '
                + 'A poll fetches one batch and any left over comes on the next poll, so smaller batches '
                + 'keep each update light but catch up more slowly. Server mode only.',
            },
          ],
        },
        {
          title: 'Thinning',
          note: 'Applies to the plots that draw one mark per sample: Trace, Pairwise and Parallel. '
            + 'Violin, Histogram, Density, ESS and the statistics always use every sample. '
            + 'Samples are counted after burn-in.',
          fields: [
            {
              key: 'thinningInterval', label: 'Thinning interval (k)',
              hint: 'Only samples k, 2k, 3k, ... are drawn, e.g. k = 5 keeps samples 5, 10, 15. 1 keeps every sample.',
            },
          ],
        },
      ],
    },
    {
      title: 'Plots',
      groups: [
        {
          title: 'Histogram',
          note: 'Also applies to the histogram shown beside the Trace plot.',
          fields: [
            { key: 'histogramBins', label: 'Bins', hint: 'Number of bins. 0 lets the plot choose automatically.' },
            { key: 'histogramOpacity', label: 'Opacity', step: 0.05, hint: '' },
          ],
        },
        {
          title: 'Density',
          fields: [
            { key: 'kdeGridSize', label: 'Grid size', hint: 'Number of points the density is evaluated at.' },
            {
              key: 'kdeBandwidthScale', label: 'Bandwidth scale', step: 0.1,
              hint: 'Multiplier on the automatic (Silverman) bandwidth. Below 1 is more detailed, above 1 is smoother.',
            },
            { key: 'kdeFillOpacity', label: 'Fill opacity', step: 0.05, hint: '' },
          ],
        },
        {
          title: 'Pairwise',
          fields: [
            { key: 'pairwiseMarkerSize', label: 'Point size', step: 1, hint: '' },
            { key: 'pairwiseMarkerOpacity', label: 'Point opacity', step: 0.05, hint: '' },
          ],
        },
        {
          title: 'ESS',
          note: 'The thresholds also set the colour of the ESS chips in the trace list.',
          fields: [
            {
              key: 'essStep', label: 'Step (k)',
              hint: 'Samples between each ESS evaluation. Smaller is finer but slower to compute.',
            },
            {
              key: 'essLowThreshold', label: 'Low ESS threshold',
              hint: 'ESS below this is red. ESS between the low and high thresholds is orange.',
            },
            {
              key: 'essHighThreshold', label: 'High ESS threshold',
              hint: 'ESS at or above this is shown in green. Must be greater than the low threshold.',
            },
          ],
        },
      ],
    },
    {
      title: 'Statistics',
      groups: [
        {
          title: 'Stats table',
          fields: [
            {
              key: 'credibleInterval', label: 'HPD interval width', step: 0.01,
              hint: 'Proportion of samples contained in the highest posterior density interval.',
            },
          ],
        },
      ],
    },
  ];

  private colourTimer: number | null = null;
  private pendingPalette: string[] | null = null;

  get settings() {
    return readSettings(this.$store);
  }

  get presetItems() {
    return [
      ...PALETTE_PRESETS.map((p) => ({ text: p.name, value: p.name })),
      { text: 'Custom', value: 'Custom', disabled: true },
    ];
  }

  get currentPreset() {
    const palette = this.settings.palette;
    const match = PALETTE_PRESETS.find((p) =>
      p.colours.length === palette.length && p.colours.every((c, i) => c.toLowerCase() === palette[i].toLowerCase()));
    return match ? match.name : 'Custom';
  }

  public beforeDestroy() {
    this.flushColour();
  }

  public update(key: NumericSettingKey, value: number) {
    commitUpdateSettings(this.$store, { [key]: value });
  }

  public updateFromText(key: NumericSettingKey, value: string) {
    if (this.validationError(key, value) === true) {
      this.update(key, Number(value));
    }
  }

  public rules(key: NumericSettingKey) {
    return [(value: string) => this.validationError(key, value)];
  }

  public validationError(key: NumericSettingKey, value: string): true | string {
    const { min, max, integer } = SETTING_LIMITS[key];
    const n = Number(value);
    if (value === '' || !isValidNumber(key, n)) {
      return `Enter ${integer ? 'a whole number' : 'a number'} between ${min} and ${max}`;
    }
    if (key === 'essLowThreshold' && n >= this.settings.essHighThreshold) {
      return `Must be below the high threshold (${this.settings.essHighThreshold})`;
    }
    if (key === 'essHighThreshold' && n <= this.settings.essLowThreshold) {
      return `Must be above the low threshold (${this.settings.essLowThreshold})`;
    }
    return true;
  }

  public applyPreset(name: string) {
    const preset = PALETTE_PRESETS.find((p) => p.name === name);
    if (preset) {
      this.flushColour();
      commitUpdateSettings(this.$store, { palette: [...preset.colours] });
    }
  }

  // The colour picker emits continuously while dragging; debounce so graphs aren't recomputed on every tick.
  public setColour(index: number, colour: string) {
    const palette = this.pendingPalette || [...this.settings.palette];
    palette[index] = colour.slice(0, 7);
    this.pendingPalette = palette;
    if (this.colourTimer !== null) {
      window.clearTimeout(this.colourTimer);
    }
    this.colourTimer = window.setTimeout(this.flushColour, COLOUR_DEBOUNCE_MS);
  }

  public addColour() {
    this.flushColour();
    const palette = [...this.settings.palette];
    palette.push(nextPaletteColour(palette));
    commitUpdateSettings(this.$store, { palette });
  }

  // The palette can't be empty (it would be rejected by the settings validation), so the last colour stays.
  public removeColour(index: number) {
    this.flushColour();
    if (this.settings.palette.length <= 1) {
      return;
    }
    const palette = [...this.settings.palette];
    palette.splice(index, 1);
    commitUpdateSettings(this.$store, { palette });
    this.paletteVersion++;
  }

  public flushColour() {
    if (this.colourTimer !== null) {
      window.clearTimeout(this.colourTimer);
      this.colourTimer = null;
    }
    if (this.pendingPalette) {
      commitUpdateSettings(this.$store, { palette: this.pendingPalette });
      this.pendingPalette = null;
    }
  }

  public reset() {
    this.flushColour();
    commitResetSettings(this.$store);
  }
}
</script>

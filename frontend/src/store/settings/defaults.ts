import { ChoiceSettingKey, NumericSettingKey, SettingsState } from "./state";

const STORAGE_KEY = "beastiary-settings";

export const DEFAULT_PALETTE = [
  "#2980b9",
  "#2ecc71",
  "#9b59b6",
  "#f1c40f",
  "#e74c3c",
  "#1abc9c",
  "#8e44ad",
  "#ff7f0e",
  "#2ca02c",
  "#d62728",
  "#9467bd",
  "#8c564b",
  "#e377c2",
  "#7f7f7f",
  "#17becf",
];

// Okabe-Ito colour-blind safe palette (black replaced with grey so it stays visible on the dark theme).
export const COLOURBLIND_PALETTE = [
  "#0072B2",
  "#E69F00",
  "#009E73",
  "#D55E00",
  "#CC79A7",
  "#56B4E9",
  "#F0E442",
  "#999999",
];

export const PALETTE_PRESETS: Array<{ name: string; colours: string[] }> = [
  { name: "Default", colours: DEFAULT_PALETTE },
  { name: "Colour-blind safe (Okabe-Ito)", colours: COLOURBLIND_PALETTE },
];

// The colour to append when the user adds one to the palette: the first default colour that isn't already used, or
// (once they all are) the default colours again in order.
export function nextPaletteColour(palette: string[]): string {
  const used = new Set(palette.map((c) => c.toLowerCase()));
  const unused = DEFAULT_PALETTE.find((c) => !used.has(c.toLowerCase()));
  return unused || DEFAULT_PALETTE[palette.length % DEFAULT_PALETTE.length];
}

export const SETTING_LIMITS: Record<
  NumericSettingKey,
  { min: number; max: number; integer?: boolean }
> = {
  pollingInterval: { min: 1, max: 3600, integer: true },
  pollingBatchSize: { min: 100, max: 100000, integer: true },
  thinningInterval: { min: 1, max: 100000, integer: true },
  combineThinningInterval: { min: 1, max: 100000, integer: true },
  essStep: { min: 10, max: 10000, integer: true },
  essLowThreshold: { min: 1, max: 100000, integer: true },
  essHighThreshold: { min: 2, max: 100000, integer: true },
  kdeGridSize: { min: 64, max: 4096, integer: true },
  kdeBandwidthScale: { min: 0.1, max: 5 },
  kdeFillOpacity: { min: 0, max: 1 },
  histogramBins: { min: 0, max: 1000, integer: true },
  histogramOpacity: { min: 0.05, max: 1 },
  pairwiseMarkerSize: { min: 1, max: 20 },
  pairwiseMarkerOpacity: { min: 0.05, max: 1 },
  credibleInterval: { min: 0.5, max: 0.999 },
};

export const CHOICE_OPTIONS: Record<ChoiceSettingKey, readonly string[]> = {
  combineMode: ["all", "off"],
  combineThinning: ["auto", "off", "custom"],
};

export function defaultSettings(): SettingsState {
  return {
    palette: [...DEFAULT_PALETTE],
    pollingInterval: 5,
    pollingBatchSize: 2500,
    thinningInterval: 1,
    combineMode: "all",
    combineThinning: "auto",
    combineThinningInterval: 2,
    essStep: 100,
    essLowThreshold: 100,
    essHighThreshold: 200,
    kdeGridSize: 512,
    kdeBandwidthScale: 1,
    kdeFillOpacity: 0.4,
    histogramBins: 0,
    histogramOpacity: 0.6,
    pairwiseMarkerSize: 5,
    pairwiseMarkerOpacity: 0.4,
    credibleInterval: 0.95,
  };
}

const HEX_COLOUR = /^#[0-9a-f]{6}$/i;

export function isValidNumber(
  key: NumericSettingKey,
  value: unknown,
): value is number {
  const limits = SETTING_LIMITS[key];
  return (
    typeof value === "number" &&
    Number.isFinite(value) &&
    value >= limits.min &&
    value <= limits.max &&
    (!limits.integer || Number.isInteger(value))
  );
}

export function isValidChoice(key: ChoiceSettingKey, value: unknown): boolean {
  return typeof value === "string" && CHOICE_OPTIONS[key].includes(value);
}

// Returns `current` with every valid entry of `partial` applied. Invalid entries are ignored rather than
// clamped, so a bad value never silently turns into a different one. Unknown keys are ignored.
export function mergeSettings(
  current: SettingsState,
  partial: unknown,
): SettingsState {
  const next: SettingsState = { ...current, palette: [...current.palette] };
  if (typeof partial !== "object" || partial === null) {
    return next;
  }
  const input = partial as { [key: string]: unknown };

  const palette = input.palette;
  const isHex = (c: unknown) => typeof c === "string" && HEX_COLOUR.test(c);
  if (Array.isArray(palette) && palette.length > 0 && palette.every(isHex)) {
    next.palette = [...palette];
  }

  for (const key of Object.keys(SETTING_LIMITS) as NumericSettingKey[]) {
    if (key in input && isValidNumber(key, input[key])) {
      next[key] = input[key] as number;
    }
  }

  for (const key of Object.keys(CHOICE_OPTIONS) as ChoiceSettingKey[]) {
    if (key in input && isValidChoice(key, input[key])) {
      (next as unknown as Record<string, unknown>)[key] = input[key];
    }
  }

  if (next.essLowThreshold >= next.essHighThreshold) {
    next.essLowThreshold = current.essLowThreshold;
    next.essHighThreshold = current.essHighThreshold;
  }
  return next;
}

export function loadSettings(): SettingsState {
  const defaults = defaultSettings();
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? mergeSettings(defaults, JSON.parse(stored)) : defaults;
  } catch {
    // Storage unavailable or corrupted JSON: fall back to defaults.
    return defaults;
  }
}

export function saveSettings(settings: SettingsState) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
  } catch {
    // Storage unavailable (e.g. private mode / quota exceeded): settings just won't persist.
  }
}

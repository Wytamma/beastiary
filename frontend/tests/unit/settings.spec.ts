import {
  DEFAULT_PALETTE,
  defaultSettings,
  isValidNumber,
  loadSettings,
  mergeSettings,
  nextPaletteColour,
  saveSettings,
} from "@/store/settings/defaults";

describe("nextPaletteColour", () => {
  it("picks the first default colour that isn't already in the palette", () => {
    expect(nextPaletteColour(["#ff0000"])).toBe(DEFAULT_PALETTE[0]);
    expect(nextPaletteColour([DEFAULT_PALETTE[0]])).toBe(DEFAULT_PALETTE[1]);
    expect(nextPaletteColour([DEFAULT_PALETTE[1]])).toBe(DEFAULT_PALETTE[0]);
  });

  it("ignores case when checking for used colours", () => {
    expect(nextPaletteColour([DEFAULT_PALETTE[0].toUpperCase()])).toBe(
      DEFAULT_PALETTE[1],
    );
  });

  it("cycles through the defaults once they are all in use", () => {
    const full = [...DEFAULT_PALETTE];
    expect(nextPaletteColour(full)).toBe(DEFAULT_PALETTE[0]);
    expect(nextPaletteColour([...full, "#000000"])).toBe(DEFAULT_PALETTE[1]);
  });

  it("always returns a colour the settings validation accepts", () => {
    const palette = nextPaletteColour(["#123456"]);
    expect(
      mergeSettings(defaultSettings(), { palette: ["#123456", palette] })
        .palette,
    ).toEqual(["#123456", palette]);
  });
});

describe("isValidNumber", () => {
  it("accepts values within limits", () => {
    expect(isValidNumber("essStep", 100)).toBe(true);
    expect(isValidNumber("kdeBandwidthScale", 0.5)).toBe(true);
  });

  it("accepts the limits themselves", () => {
    expect(isValidNumber("kdeFillOpacity", 0)).toBe(true);
    expect(isValidNumber("kdeFillOpacity", 1)).toBe(true);
  });

  it("defaults the thinning interval to 1 (keep every sample) and requires a positive whole number", () => {
    expect(defaultSettings().thinningInterval).toBe(1);
    expect(isValidNumber("thinningInterval", 1)).toBe(true);
    expect(isValidNumber("thinningInterval", 5000)).toBe(true);
    expect(isValidNumber("thinningInterval", 0)).toBe(false);
    expect(isValidNumber("thinningInterval", -1)).toBe(false);
    expect(isValidNumber("thinningInterval", 1.5)).toBe(false);
  });

  it("defaults polling to 5s and 2500 samples per request, and rejects values that would hammer the server", () => {
    const defaults = defaultSettings();
    expect(defaults.pollingInterval).toBe(5);
    expect(defaults.pollingBatchSize).toBe(2500);
    expect(isValidNumber("pollingInterval", 1)).toBe(true);
    expect(isValidNumber("pollingInterval", 0)).toBe(false);
    expect(isValidNumber("pollingInterval", 2.5)).toBe(false);
    expect(isValidNumber("pollingBatchSize", 100)).toBe(true);
    expect(isValidNumber("pollingBatchSize", 99)).toBe(false);
  });

  it("rejects out of range values", () => {
    expect(isValidNumber("essStep", 9)).toBe(false);
    expect(isValidNumber("kdeGridSize", 5000)).toBe(false);
    expect(isValidNumber("credibleInterval", 1)).toBe(false);
  });

  it("rejects non-integers for integer settings", () => {
    expect(isValidNumber("essStep", 100.5)).toBe(false);
    expect(isValidNumber("pairwiseMarkerSize", 5.5)).toBe(true);
  });

  it("rejects non-numbers and non-finite numbers", () => {
    expect(isValidNumber("essStep", "100")).toBe(false);
    expect(isValidNumber("essStep", NaN)).toBe(false);
    expect(isValidNumber("essStep", Infinity)).toBe(false);
    expect(isValidNumber("essStep", null)).toBe(false);
    expect(isValidNumber("essStep", undefined)).toBe(false);
  });
});

describe("mergeSettings", () => {
  it("applies valid values", () => {
    const next = mergeSettings(defaultSettings(), {
      essStep: 250,
      kdeGridSize: 1024,
      palette: ["#ff0000"],
    });
    expect(next.essStep).toBe(250);
    expect(next.kdeGridSize).toBe(1024);
    expect(next.palette).toEqual(["#ff0000"]);
  });

  it("does not mutate the current settings", () => {
    const current = defaultSettings();
    mergeSettings(current, { essStep: 250, palette: ["#ff0000"] });
    expect(current).toEqual(defaultSettings());
  });

  it("ignores invalid values instead of clamping them", () => {
    const next = mergeSettings(defaultSettings(), {
      essStep: 5,
      kdeGridSize: "big",
      histogramOpacity: 7,
    });
    expect(next).toEqual(defaultSettings());
  });

  it("keeps valid entries when others in the same update are invalid", () => {
    const next = mergeSettings(defaultSettings(), {
      essStep: 5,
      kdeGridSize: 1024,
    });
    expect(next.essStep).toBe(defaultSettings().essStep);
    expect(next.kdeGridSize).toBe(1024);
  });

  it("ignores unknown keys", () => {
    const next = mergeSettings(defaultSettings(), { notASetting: 1 });
    expect(next).toEqual(defaultSettings());
    expect(next).not.toHaveProperty("notASetting");
  });

  it("rejects malformed palettes", () => {
    const defaults = defaultSettings();
    expect(mergeSettings(defaults, { palette: [] }).palette).toEqual(
      defaults.palette,
    );
    expect(mergeSettings(defaults, { palette: ["red"] }).palette).toEqual(
      defaults.palette,
    );
    expect(mergeSettings(defaults, { palette: ["#fff"] }).palette).toEqual(
      defaults.palette,
    );
    expect(
      mergeSettings(defaults, { palette: ["#ff0000", 3] }).palette,
    ).toEqual(defaults.palette);
    expect(mergeSettings(defaults, { palette: "nope" }).palette).toEqual(
      defaults.palette,
    );
  });

  it("rejects an update that makes the low ESS threshold >= the high one", () => {
    const defaults = defaultSettings();
    const next = mergeSettings(defaults, { essLowThreshold: 300 });
    expect(next.essLowThreshold).toBe(defaults.essLowThreshold);
    expect(next.essHighThreshold).toBe(defaults.essHighThreshold);
  });

  it("accepts both ESS thresholds changed consistently in one update", () => {
    const next = mergeSettings(defaultSettings(), {
      essLowThreshold: 300,
      essHighThreshold: 600,
    });
    expect(next.essLowThreshold).toBe(300);
    expect(next.essHighThreshold).toBe(600);
  });

  it("tolerates a non-object payload", () => {
    expect(mergeSettings(defaultSettings(), null)).toEqual(defaultSettings());
    expect(mergeSettings(defaultSettings(), "x")).toEqual(defaultSettings());
  });

  it("combines same-name parameters without thinning them, by default", () => {
    const defaults = defaultSettings();
    expect(defaults.combineMode).toBe("all");
    expect(defaults.combineThinning).toBe("off");
  });

  it("accepts the known combine options and ignores anything else", () => {
    const defaults = defaultSettings();
    expect(mergeSettings(defaults, { combineMode: "all" }).combineMode).toBe(
      "all",
    );
    expect(mergeSettings(defaults, { combineMode: "off" }).combineMode).toBe(
      "off",
    );
    expect(
      mergeSettings(defaults, { combineThinning: "custom" }).combineThinning,
    ).toBe("custom");
    expect(mergeSettings(defaults, { combineMode: "some" }).combineMode).toBe(
      defaults.combineMode,
    );
    // "selected" is no longer a mode, so a value saved by an older version falls back to the default.
    expect(
      mergeSettings(defaults, { combineMode: "selected" }).combineMode,
    ).toBe(defaults.combineMode);
    expect(mergeSettings(defaults, { combineMode: 1 }).combineMode).toBe(
      defaults.combineMode,
    );
    expect(
      mergeSettings(defaults, { combineThinning: "selected" }).combineThinning,
    ).toBe(defaults.combineThinning);
  });

  it("requires the custom combine thinning interval to be a positive whole number", () => {
    expect(isValidNumber("combineThinningInterval", 1)).toBe(true);
    expect(isValidNumber("combineThinningInterval", 4)).toBe(true);
    expect(isValidNumber("combineThinningInterval", 0)).toBe(false);
    expect(isValidNumber("combineThinningInterval", 2.5)).toBe(false);
  });
});

describe("persistence", () => {
  beforeEach(() => localStorage.clear());

  it("round-trips through localStorage", () => {
    const settings = mergeSettings(defaultSettings(), {
      essStep: 500,
      palette: ["#123456", "#abcdef"],
    });
    saveSettings(settings);
    expect(loadSettings()).toEqual(settings);
  });

  it("falls back to defaults on corrupted JSON", () => {
    localStorage.setItem("beastiary-settings", "{not json");
    expect(loadSettings()).toEqual(defaultSettings());
  });

  it("drops invalid stored values but keeps valid ones", () => {
    localStorage.setItem(
      "beastiary-settings",
      JSON.stringify({ essStep: -1, kdeGridSize: 256 }),
    );
    const loaded = loadSettings();
    expect(loaded.essStep).toBe(defaultSettings().essStep);
    expect(loaded.kdeGridSize).toBe(256);
  });
});

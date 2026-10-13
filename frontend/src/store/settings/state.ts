export interface SettingsState {
  // Plot colours, assigned to parameters in order (cycles if there are more parameters than colours).
  palette: string[];
  // How often, in seconds, open traces are polled for new samples (server mode) or file changes (auto-reload).
  pollingInterval: number;
  // Maximum number of samples requested from the server in a single request: the chunk size used when a trace is
  // first opened, and the most fetched by one poll (if more are waiting, the next poll fetches the rest).
  pollingBatchSize: number;
  // Thinning interval k for plots that draw one mark per sample (Trace, Pairwise, Parallel): only samples
  // k, 2k, 3k, ... are drawn. 1 keeps every sample. Distribution plots, ESS and statistics always use every sample.
  thinningInterval: number;
  // Combining parameters that share a name across traces into one extra "combined" trace at the top of the trace list.
  // "all" combines every parameter that two or more loaded traces have, "off" doesn't combine anything.
  combineMode: CombineMode;
  // How each trace is thinned before being combined (after burn-in, before ESS and statistics are computed):
  // "auto" uses k = the number of traces combined into the parameter, so the combined parameter is about as long as
  // one trace's, "custom" uses `combineThinningInterval`, "off" keeps every sample.
  combineThinning: CombineThinning;
  combineThinningInterval: number;
  // Cumulative ESS plot: number of samples between ESS evaluations (the "k" step).
  essStep: number;
  // ESS below `essLowThreshold` is red, below `essHighThreshold` is orange, otherwise green.
  essLowThreshold: number;
  essHighThreshold: number;
  // Kernel density plot.
  kdeGridSize: number;
  kdeBandwidthScale: number;
  kdeFillOpacity: number;
  // Histogram plot, and the side histogram of the Trace plot. 0 bins lets Plotly choose.
  histogramBins: number;
  histogramOpacity: number;
  // Pairwise scatter plot.
  pairwiseMarkerSize: number;
  pairwiseMarkerOpacity: number;
  // Width of the HPD / credible interval shown in the stats table (0-1).
  credibleInterval: number;
}

export type CombineMode = "off" | "all";
export type CombineThinning = "auto" | "off" | "custom";

// Settings that hold one of a fixed set of strings rather than a number.
export type ChoiceSettingKey = "combineMode" | "combineThinning";

export type NumericSettingKey = Exclude<
  keyof SettingsState,
  "palette" | ChoiceSettingKey
>;

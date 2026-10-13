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

export type NumericSettingKey = Exclude<keyof SettingsState, "palette">;

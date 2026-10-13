import { Traces } from "@/interfaces";

export interface DataState {
  traces: Traces;
  loadingSamples: boolean;
  // Parameters selected on the combined trace. The combined trace is derived from the other traces, so this is
  // the only part of it that is stored.
  combinedActiveParams: string[];
}

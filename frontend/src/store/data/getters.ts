import { combineTraces, withActiveParams } from "@/combine";
import { Trace, Traces } from "@/interfaces";
import { getStoreAccessors } from "typesafe-vuex";
import { State } from "../state";
import { DataState } from "./state";

export const getters = {
  traces: (state: DataState) => state.traces,
  loadingSamples: (state: DataState) => state.loadingSamples,
  activeTraceIDs: (state: DataState) =>
    Object.values(state.traces)
      .filter((t) => t.isActive)
      .map((t) => t.id),
  activeTraces: (state: DataState) =>
    Object.values(state.traces).filter((t) => t.isActive),
  // The combined traces' data (see combine.ts and the combine settings). This doesn't depend on the selected
  // parameters, so selecting one doesn't rebuild the combined data.
  combinedTracesData: (
    state: DataState,
    _getters: any,
    rootState: State,
  ): Trace[] => combineTraces(Object.values(state.traces), rootState.settings),
  // The combined traces with their selected parameters.
  combinedTraces: (state: DataState, getters: any): Trace[] =>
    (getters.combinedTracesData as Trace[]).map((trace) =>
      withActiveParams(trace, state.combinedActiveParams),
    ),
  // Every trace the plots and statistics should show: the loaded traces plus the combined ones.
  displayTraces: (state: DataState, getters: any): Traces => {
    const traces: Traces = { ...state.traces };
    for (const trace of getters.combinedTraces as Trace[]) {
      traces[trace.id] = trace;
    }
    return traces;
  },
};
const { read } = getStoreAccessors<DataState, State>("");

export const readTraces = read(getters.traces);
export const readLoadingSamples = read(getters.loadingSamples);
export const readActiveTraceIDs = read(getters.activeTraceIDs);
export const readActiveTraces = read(getters.activeTraces);
export const readCombinedTraces = read(getters.combinedTraces);
export const readDisplayTraces = read(getters.displayTraces);

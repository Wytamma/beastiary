import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';
import { DataState } from './state';

export const getters = {
    traces: (state: DataState) => state.traces,
    loadingSamples: (state: DataState) => state.loadingSamples,
    activeTraceIDs: (state: DataState) => Object.values(state.traces).filter((t) => t.isActive).map((t) => t.id),
};
const {read} = getStoreAccessors<DataState, State>('');

export const readTraces = read(getters.traces);
export const readLoadingSamples = read(getters.loadingSamples);
export const readActiveTraceIDs = read(getters.activeTraceIDs);


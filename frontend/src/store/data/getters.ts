import { DataState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
    traces: (state: DataState) => state.traces,
    activeTrace: (state: DataState) => state.activeTraceID ? state.traces.find((trace) => trace.id == state.activeTraceID) : null,
    paramsOfActiveTrace: (state: DataState) => {
        if (state.activeTraceID) {
            const activeTrace = state.traces.find((trace) => trace.id == state.activeTraceID);
            if (activeTrace && activeTrace.parameters) {
                return Object.keys(activeTrace.parameters);
            } else {
                return null;
            }
        }
    },
    activeParam: (state: DataState) => state.activeParam,
};
const {read} = getStoreAccessors<DataState, State>('');

export const readTraces = read(getters.traces);
export const readParamsOfActiveTrace = read(getters.paramsOfActiveTrace);
export const readActiveTrace = read(getters.activeTrace);
export const readActiveParam = read(getters.activeParam);


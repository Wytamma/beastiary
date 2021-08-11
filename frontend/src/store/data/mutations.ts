import { DataState, Trace } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';


export const mutations = {
    setTraces(state: DataState, payload: Trace[]) {
        state.traces = payload;
    },
    setTrace(state: DataState, payload: Trace) {
        state.traces.push(payload);
    },
};

const {commit} = getStoreAccessors<DataState | any, State>('');

export const commitSetTraces = commit(mutations.setTraces);
export const commitSetTrace = commit(mutations.setTrace);


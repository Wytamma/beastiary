import { Data, InSample, SetSample, Trace } from '@/interfaces';
import { getStoreAccessors } from 'typesafe-vuex';
import Vue from 'vue';
import { State } from '../state';
import { DataState } from './state';

function formatData(samples: InSample[]) {
    const parameters: { [key: string]: Data[] } = {};
    for (let index = 0; index < samples.length; index++) {
        const row = samples[index].data;
        const state = samples[index].state;
        for (const param in row) {
            if (param) {
                if (index === 0) {
                    parameters[param] = [];
                }
                parameters[param].push({ state, value: row[param] });
            }
        }

    }

    return parameters;
}

function setTraceDefaults(trace: Trace) {
    trace.parameters = {};
    trace.activeParams = [];
    trace.isActive = false;
    trace.burnIn = 10;
}

export const mutations = {
    setTraces(state: DataState, payload: Trace[]) {
        for (const trace of payload) {
            setTraceDefaults(trace);
        }
        const traces = payload.reduce((obj, trace) => {
            obj[trace.id] = trace;
            return obj;
          }, {});
        state.traces = traces;
    },
    setTrace(state: DataState, payload: Trace) {
        setTraceDefaults(payload);
        // https://vuex.vuejs.org/guide/mutations.html#mutations-follow-vue-s-reactivity-rules
        Vue.set(state.traces, payload.id, payload);
    },
    setActiveTrace(state: DataState, payload: Trace) {
        state.traces[payload.id].isActive = true;

    },
    setActiveParams(state: DataState, payload: {traceID: number, params: string[]}) {
        state.traces[payload.traceID].activeParams = payload.params;
    },
    setBurnIn(state: DataState, payload: {traceID: number, burnIn: number}) {
        state.traces[payload.traceID].burnIn = payload.burnIn;
    },
    setLoadingSamples(state: DataState, payload: boolean) {
        state.loadingSamples = payload;
    },
    setSetSamples(state: DataState, payload: {traceID: number, data: InSample[]}) {
        const data = formatData(payload.data);
        const trace = state.traces[payload.traceID];
        if (Object.keys(trace.parameters).length === 0) {
            trace.parameters = data;
        } else {
            for (const paramName in data) {
                if (paramName) {
                    trace.parameters[paramName] = trace.parameters[paramName].concat(
                        data[paramName]).sort((a, b) => a.state - b.state,
                    );
                }
            }
        }
    },
};

const {commit} = getStoreAccessors<DataState | any, State>('');

export const commitSetTraces = commit(mutations.setTraces);
export const commitSetTrace = commit(mutations.setTrace);
export const commitSetActiveTrace = commit(mutations.setActiveTrace);
export const commitSetSamples = commit(mutations.setSetSamples);
export const commitSetActiveParams = commit(mutations.setActiveParams);
export const commitSetBurnIn = commit(mutations.setBurnIn);
export const commitSetLoadingSamples = commit(mutations.setLoadingSamples);


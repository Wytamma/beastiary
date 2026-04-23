import { Data, InSample, LocalTraceState, Trace } from '@/interfaces';
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
    trace.source = trace.source || 'server';
    trace.parameters = trace.parameters || {};
    trace.activeParams = trace.activeParams || [];
    trace.isActive = typeof trace.isActive === 'boolean' ? trace.isActive : false;
    trace.burnIn = typeof trace.burnIn === 'number' ? trace.burnIn : 10;
    trace.isLoading = typeof trace.isLoading === 'boolean' ? trace.isLoading : false;
}

function mergeTraces(existingTraces: {[id: number]: Trace}, serverTraces: Trace[]) {
    const traces = Object.values(existingTraces)
        .filter((trace) => trace.source !== 'server')
        .reduce((accumulator, trace) => {
            accumulator[trace.id] = trace;
            return accumulator;
        }, {} as {[id: number]: Trace});

    for (const trace of serverTraces) {
        setTraceDefaults(trace);
        trace.source = 'server';
        traces[trace.id] = trace;
    }

    return traces;
}

function preserveLocalTraceState(existingTrace: Trace, payload: Trace) {
    const validActiveParams = existingTrace.activeParams.filter((param) => param in payload.parameters);
    return {
        ...payload,
        burnIn: existingTrace.burnIn,
        activeParams: validActiveParams.length ? validActiveParams : payload.activeParams,
        isActive: existingTrace.isActive,
        isLoading: false,
        localFile: payload.localFile || existingTrace.localFile,
    };
}

export const mutations = {
    setTraces(state: DataState, payload: Trace[]) {
        state.traces = mergeTraces(state.traces, payload);
    },
    setTrace(state: DataState, payload: Trace) {
        setTraceDefaults(payload);
        payload.source = 'server';
        // https://vuex.vuejs.org/guide/mutations.html#mutations-follow-vue-s-reactivity-rules
        Vue.set(state.traces, payload.id, payload);
    },
    setParsedTrace(state: DataState, payload: Trace) {
        setTraceDefaults(payload);
        payload.source = 'local';
        Vue.set(state.traces, payload.id, payload);
    },
    reloadParsedTrace(state: DataState, payload: Trace) {
        const existing = state.traces[payload.id];
        Vue.set(state.traces, payload.id, preserveLocalTraceState(existing, payload));
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
    setLoadingSamples(state: DataState, payload: {traceID: number, loading: boolean}) {
        state.loadingSamples = payload.loading;
        state.traces[payload.traceID].isLoading = payload.loading;
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
                        data[paramName], // ).sort((a, b) => a.state - b.state,
                    );
                }
            }
        }
    },
    setLocalTraceState(state: DataState, payload: {traceID: number, localFile: Partial<LocalTraceState>}) {
        const trace = state.traces[payload.traceID];
        if (!trace.localFile) {
            return;
        }
        trace.localFile = {
            ...trace.localFile,
            ...payload.localFile,
        };
    },
};

const {commit} = getStoreAccessors<DataState | any, State>('');

export const commitSetTraces = commit(mutations.setTraces);
export const commitSetTrace = commit(mutations.setTrace);
export const commitAddParsedTrace = commit(mutations.setParsedTrace);
export const commitReloadParsedTrace = commit(mutations.reloadParsedTrace);
export const commitSetActiveTrace = commit(mutations.setActiveTrace);
export const commitSetSamples = commit(mutations.setSetSamples);
export const commitSetActiveParams = commit(mutations.setActiveParams);
export const commitSetBurnIn = commit(mutations.setBurnIn);
export const commitSetLoadingSamples = commit(mutations.setLoadingSamples);
export const commitSetLocalTraceState = commit(mutations.setLocalTraceState);

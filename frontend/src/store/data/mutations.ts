import { Data, InSample, SetSample, Trace } from '@/interfaces';
import { getStoreAccessors } from 'typesafe-vuex';
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

export const mutations = {
    setTraces(state: DataState, payload: Trace[]) {
        for (const trace of payload) {
            if (!trace.parameters) {
                trace.parameters = {};
            }
        }
        state.traces = payload;
    },
    setTrace(state: DataState, payload: Trace) {
        if (!payload.parameters) {
            payload.parameters = {};
        }
        state.traces.push(payload);
    },
    setActiveTrace(state: DataState, payload: Trace) {
        if (payload) {
            state.activeTraceID = payload.id;
        } else {
            state.activeTraceID = null
        }
        
    },
    setActiveParam(state: DataState, payload: string) {
        state.activeParam = payload;
    },
    setBurnIn(state: DataState, payload: number) {
        state.burnIn = payload;
    },
    setLoadingSamples(state: DataState, payload: boolean) {
        state.loadingSamples = payload;
    },
    setSetSamples(state: DataState, payload: SetSample) {
        const traceId = payload.trace.id;
        const data = formatData(payload.data);
        const trace = state.traces.find((t) => t.id === traceId);
        if (trace) {
            if (Object.keys(trace.parameters).length === 0) {
                trace.parameters = data;
            } else {
                for (const paramName in data) {
                    if (paramName) {
                        trace.parameters[paramName] = trace.parameters[paramName].concat(data[paramName]).sort((a,b) => a.state - b.state);
                    }
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
export const commitSetActiveParam = commit(mutations.setActiveParam);
export const commitSetBurnIn = commit(mutations.setBurnIn);
export const commitSetLoadingSamples = commit(mutations.setLoadingSamples);


import { DataState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';
import { Trace, SetSample, inSample, Data } from '@/interfaces';

function formatData(samples: inSample[]) {
    const parameters: { [key: string]: Data[] } = {};
    for (let index = 0; index < samples.length; index++) {
        const row = samples[index].data;
        const state = row.state;
        for (const param in row) {
            if (index == 0) {
                parameters[param] = [];
            }
            parameters[param].push({ state, value: row[param] });
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
        state.activeTraceID = payload.id;
    },
    setActiveParam(state: DataState, payload: string) {
        state.activeParam = payload;
    },
    setSetSamples(state: DataState, payload: SetSample) {
        const traceId = payload.trace.id;
        const data = formatData(payload.data);
        const trace = state.traces.find((t) => t.id == traceId);
        if (trace) {
            if (Object.keys(trace.parameters).length === 0) {
                trace.parameters = data;
            } else {
                for (const paramName in data) {
                    trace.parameters[paramName] = trace.parameters[paramName].concat(data[paramName]);
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


import { actions } from './actions';
import { getters } from './getters';
import { mutations } from './mutations';
import { DataState } from './state';

const defaultState: DataState = {
    traces: [],
    activeTraceID: null,
    activeParam: null,
    burnIn: 10,
    loadingSamples: false,
};

export const dataModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};

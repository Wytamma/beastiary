import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { DataState } from './state';

const defaultState: DataState = {
    traces: [],
    activeTraceID: null,
    activeParam: null,
};

export const dataModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};

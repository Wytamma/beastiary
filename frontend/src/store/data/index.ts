import { actions } from './actions';
import { getters } from './getters';
import { mutations } from './mutations';
import { DataState } from './state';

const defaultState: DataState = {
    traces: {},
    loadingSamples: false,
};

export const dataModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};

import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { DataState } from './state';

const defaultState: DataState = {
    traces: [],
};

export const dataModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};

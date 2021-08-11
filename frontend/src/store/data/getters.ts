import { DataState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
    runs: (state: DataState) => state.runs,
};

const {read} = getStoreAccessors<DataState, State>('');

export const readRuns = read(getters.runs);

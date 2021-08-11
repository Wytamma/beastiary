import { DataState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
    traces: (state: DataState) => state.traces,
};

const {read} = getStoreAccessors<DataState, State>('');

export const readTraces = read(getters.traces);

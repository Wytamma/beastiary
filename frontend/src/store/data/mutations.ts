import { DataState, Run } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';


export const mutations = {
    setRuns(state: DataState, payload: Run[]) {
        state.runs = payload;
    },
};

const {commit} = getStoreAccessors<DataState | any, State>('');

export const commitSetRuns = commit(mutations.setRuns);


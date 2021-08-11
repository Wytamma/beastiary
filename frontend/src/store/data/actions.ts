import { api } from '@/api';
import router from '@/router';
import { getLocalToken, removeLocalToken, saveLocalToken } from '@/utils';
import { AxiosError } from 'axios';
import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import { State } from '../state';
import { commitAddNotification, commitRemoveNotification } from '../main/mutations';
import { DataState } from './state';
import { dispatchCheckApiError } from '../main/actions';
import { commitSetRuns } from './mutations';

type MainContext = ActionContext<DataState, State>;

export const actions = {
    async actionGetRuns(context: MainContext) {
        try {
            const response = await api.getRuns(context.rootState.main.token);
            if (response) {
                commitSetRuns(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
};

const { dispatch } = getStoreAccessors<DataState | any, State>('');

export const dispatchGetRuns = dispatch(actions.actionGetRuns);


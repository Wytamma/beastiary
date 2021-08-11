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
import { commitSetTraces, commitSetTrace } from './mutations';
import { TraceCreate } from '@/interfaces';

type MainContext = ActionContext<DataState, State>;

export const actions = {
    async actionGetTraces(context: MainContext) {
        try {
            const response = await api.getTraces(context.rootState.main.token);
            if (response) {
                commitSetTraces(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionCreateTrace(context: MainContext, payload: TraceCreate) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.createTrace(context.rootState.main.token, payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetTrace(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Trace successfully created', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
};

const { dispatch } = getStoreAccessors<DataState | any, State>('');

export const dispatchGetTraces = dispatch(actions.actionGetTraces);
export const dispatchCreateTrace = dispatch(actions.actionCreateTrace);


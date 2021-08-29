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
import { commitSetTraces, commitSetTrace, commitSetActiveTrace, commitSetSamples, commitSetActiveParam } from './mutations';
import { TraceCreate, Trace } from '@/interfaces';
import { readTraces } from './getters';

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
    async actionSetActiveTrace(context: MainContext, payload: Trace) {
        commitSetActiveTrace(context, payload);
    },
    async actionSetActiveParam(context: MainContext, payload: string) {
        commitSetActiveParam(context, payload);
    },
    async actionGetSamples(context: MainContext, payload: {trace: Trace, skip?: number, limit?: number}) {
        const trace = payload.trace;
        const skip = payload.skip ? payload.skip : 0;
        const limit = payload.limit ? payload.limit : 100;
        try {
            const loadingNotification = { content: 'Loading samples...', showProgress: true };
            if (skip === 0) {
                commitAddNotification(context, loadingNotification);
            }
            const response = await api.getSamples(context.rootState.main.token, trace, skip, limit);
            if (response) {
                commitSetSamples(context, {trace, data: response.data});
            }
            commitRemoveNotification(context, loadingNotification);
        } catch (error) {
            console.log(error);
            await dispatchCheckApiError(context, error);
        }
    },
    async actionLoadAllSamplesAllTraces(context: MainContext) {
        const traces = readTraces(context);
        for (const trace of traces) {
            if (trace) {
                await dispatchGetSamples(context, {trace});
            }
        }
    },

};

const { dispatch } = getStoreAccessors<DataState | any, State>('');

export const dispatchGetTraces = dispatch(actions.actionGetTraces);
export const dispatchCreateTrace = dispatch(actions.actionCreateTrace);
export const dispatchSetActiveTrace = dispatch(actions.actionSetActiveTrace);
export const dispatchGetSamples = dispatch(actions.actionGetSamples);
export const dispatchLoadAllSamplesAllTraces = dispatch(actions.actionLoadAllSamplesAllTraces);
export const dispatchSetActiveParam = dispatch(actions.actionSetActiveParam);



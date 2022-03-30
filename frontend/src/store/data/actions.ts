import { api } from '@/api';
import { Trace, TraceCreate } from '@/interfaces';
import { AxiosResponse } from 'axios';
import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import { dispatchCheckApiError } from '../main/actions';
import { commitAddNotification, commitRemoveNotification } from '../main/mutations';
import { State } from '../state';
import {
    commitSetActiveParams,
    commitSetActiveTrace,
    commitSetBurnIn,
    commitSetLoadingSamples,
    commitSetSamples,
    commitSetTrace,
    commitSetTraces,
} from './mutations';
import { DataState } from './state';

type MainContext = ActionContext<DataState, State>;

export const actions = {
    async actionGetTraces(context: MainContext) {
        let response: AxiosResponse | null = null;
        try {
            response = await api.getTraces(context.rootState.main.token);
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
        if (response) {
            commitSetTraces(context, response.data);
        }
    },
    async actionCreateTrace(context: MainContext, payload: TraceCreate) {
        const loadingNotification = { content: 'saving', showProgress: true };
        commitAddNotification(context, loadingNotification);
        let response: AxiosResponse | null = null;
        try {
            response = await api.createTrace(context.rootState.main.token, payload);
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
        commitRemoveNotification(context, loadingNotification);
        if (response != null) {
            commitSetTrace(context, response.data);
            commitAddNotification(context, { content: 'Trace successfully created', color: 'success' });
        }
    },
    async actionSetActiveTrace(context: MainContext, payload: Trace) {
        commitSetActiveTrace(context, payload);
    },
    async actionSetActiveParams(context: MainContext, payload: {traceID: number, params: string[]}) {
        commitSetActiveParams(context, payload);
    },
    async actionGetSamples(
        context: MainContext,
        payload: {trace: Trace,
            skip?: number,
            limit?: number,
            all?: boolean}) {
        const trace = payload.trace;
        const skip = payload.skip ? payload.skip : 0;
        const limit = payload.limit ? payload.limit : 100;
        const all = payload.all ? payload.all : false;
        const loadingNotification = { content: 'Loading samples...', showProgress: true };
        if (skip === 0) {
            commitAddNotification(context, loadingNotification);
        }
        let response: AxiosResponse | null = null;
        try {
            response = await api.getSamples(context.rootState.main.token, trace, skip, limit);
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
        if (response != null) {
            commitSetSamples(context, {traceID: trace.id, data: response.data});
            if (all === true && response.data.length === limit) {
                // if you get back what you request go again
                await dispatchGetSamples(context, {trace, skip: skip + limit, limit, all: true});
            }}
        commitRemoveNotification(context, loadingNotification);
    },
    async actionSetBurnIn(context: MainContext, payload: {traceID: number, burnIn: number}) {
        commitSetBurnIn(context, payload);
    },
    async actionSetLoadingSamples(context: MainContext, payload: {traceID: number, loading: boolean}) {
        commitSetLoadingSamples(context, payload);
    },
};

const { dispatch } = getStoreAccessors<DataState | any, State>('');

export const dispatchGetTraces = dispatch(actions.actionGetTraces);
export const dispatchCreateTrace = dispatch(actions.actionCreateTrace);
export const dispatchSetActiveTrace = dispatch(actions.actionSetActiveTrace);
export const dispatchGetSamples = dispatch(actions.actionGetSamples);
export const dispatchSetActiveParams = dispatch(actions.actionSetActiveParams);
export const dispatchSetBurnIn = dispatch(actions.actionSetBurnIn);
export const dispatchSetLoadingSamples = dispatch(actions.actionSetLoadingSamples);



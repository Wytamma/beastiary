import { api } from '@/api';
import router from '@/router';
import { AxiosError } from 'axios';
import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import { State } from '../state';
import {
    commitAddNotification,
    commitDisconnected,
    commitRemoveNotification,
    commitSetLoggedIn,
    commitSetLogInError,
    commitSetToken,
} from './mutations';
import { AppNotification, MainState } from './state';

type MainContext = ActionContext<MainState, State>;

export const actions = {
    async actionCheckToken(context: MainContext, payload: { token: string }) {
        try {
            const response = await api.getToken(payload.token);
            const token = response.data.token;
            if (token) {
                commitSetToken(context, token);
                commitSetLoggedIn(context, true);
                commitSetLogInError(context, false);
                await dispatchRouteLoggedIn(context);
                commitAddNotification(context, { content: 'Logged in', color: 'success' });
            } else {
                await dispatchLogOut(context);
            }
        } catch (err) {
            commitSetLogInError(context, true);
            await dispatchLogOut(context);
        }
    },
    async actionCheckLoggedIn(context: MainContext) {
        if (!context.state.isLoggedIn) {
            const token = context.state.token;
            if (token) {
                try {
                    commitSetLoggedIn(context, true);
                } catch (error) {
                    await dispatchRemoveLogIn(context);
                }
            } else {
                await dispatchRemoveLogIn(context);
            }
        }
    },
    async actionRemoveLogIn(context: MainContext) {
        commitSetToken(context, '');
        commitSetLoggedIn(context, false);
    },
    async actionLogOut(context: MainContext) {
        await dispatchRemoveLogIn(context);
        await dispatchRouteLogOut(context);
    },
    async actionUserLogOut(context: MainContext) {
        await dispatchLogOut(context);
        commitAddNotification(context, { content: 'Logged out', color: 'success' });
    },
    actionRouteLogOut(context: MainContext) {
        if (router.currentRoute.path !== '/login') {
            router.push('/login');
        }
    },
    async actionCheckApiError(context: MainContext, payload: AxiosError) {
        // check for general errors e.g. CORS or network issues
        if (!payload.response) {
            console.log('Network error');
            return commitDisconnected(context, true);
        }
        console.log('API error', payload.response);
        commitDisconnected(context, false);
        if (payload.response!.status === 401) {
            return await dispatchLogOut(context);
        }
        if (payload.response!.status === 404) {
            return commitAddNotification(context, { content: payload.response!.data.detail, color: 'error', notFound: true});
        }
        if (payload.response!.status === 500) {
            return commitAddNotification(context, { content: payload.response!.data.detail, color: 'error', notFound: true});
        }
    },
    actionRouteLoggedIn(context: MainContext) {
        if (router.currentRoute.path === '/login' || router.currentRoute.path === '/') {
            router.push('/main/dashboard');
        }
    },
    async removeNotification(context: MainContext, payload: { notification: AppNotification, timeout: number }) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                commitRemoveNotification(context, payload.notification);
                resolve(true);
            }, payload.timeout);
        });
    },
};

const { dispatch } = getStoreAccessors<MainState | any, State>('');

export const dispatchCheckApiError = dispatch(actions.actionCheckApiError);
export const dispatchCheckLoggedIn = dispatch(actions.actionCheckLoggedIn);
export const dispatchCheckToken = dispatch(actions.actionCheckToken);
export const dispatchLogOut = dispatch(actions.actionLogOut);
export const dispatchUserLogOut = dispatch(actions.actionUserLogOut);
export const dispatchRemoveLogIn = dispatch(actions.actionRemoveLogIn);
export const dispatchRouteLoggedIn = dispatch(actions.actionRouteLoggedIn);
export const dispatchRouteLogOut = dispatch(actions.actionRouteLogOut);
export const dispatchRemoveNotification = dispatch(actions.removeNotification);

import { api } from '@/api';
import router from '@/router';
import { runtimeCapabilities } from '@/runtime';
import { AxiosError } from 'axios';
import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import { State } from '../state';
import {
    commitAddNotification,
    commitDisconnected,
    commitRemoveNotification,
    commitSetAuthEnabled,
    commitSetLoggedIn,
    commitSetLogInError,
    commitSetToken,
} from './mutations';
import { AppNotification, MainState } from './state';

type MainContext = ActionContext<MainState, State>;

export const actions = {
    async actionCheckSecurity(context: MainContext) {
        if (!runtimeCapabilities.supportsAuth) {
            commitSetAuthEnabled(context, false);
            commitSetLoggedIn(context, true);
            return false;
        }
        try {
            const response = await api.getSecurityConfig();
            const authEnabled = response.data.security !== false;
            commitSetAuthEnabled(context, authEnabled);
            if (!authEnabled) {
                commitSetLoggedIn(context, true);
            }
            return authEnabled;
        } catch (error) {
            commitSetAuthEnabled(context, true);
            return true;
        }
    },
    async actionCheckToken(context: MainContext, payload: { token: string }) {
        const authEnabled = await dispatchCheckSecurity(context);
        if (!authEnabled) {
            commitSetLoggedIn(context, true);
            await dispatchRouteLoggedIn(context);
            return;
        }
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
        const authEnabled = await dispatchCheckSecurity(context);
        if (!authEnabled) {
            commitSetLoggedIn(context, true);
            return;
        }
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
        commitSetLoggedIn(context, context.state.authEnabled ? false : true);
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
        if (!context.state.authEnabled) {
            if (router.currentRoute.path !== runtimeCapabilities.defaultRoute) {
                router.push(runtimeCapabilities.defaultRoute);
            }
            return;
        }
        if (router.currentRoute.path !== '/login') {
            router.push('/login');
        }
    },
    async actionCheckApiError(context: MainContext, payload: AxiosError) {
        if (!context.state.authEnabled) {
            return;
        }
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
        if (!context.state.authEnabled) {
            if (router.currentRoute.path === '/' || router.currentRoute.path === '/login') {
                router.push(runtimeCapabilities.defaultRoute);
            }
            return;
        }
        if (router.currentRoute.path === '/login' || router.currentRoute.path === '/') {
            router.push('/main/dashboard');
        }
    },
    async removeNotification(context: MainContext, payload: { notification: AppNotification, timeout: number }) {
        return new Promise((resolve) => {
            setTimeout(() => {
                commitRemoveNotification(context, payload.notification);
                resolve(true);
            }, payload.timeout);
        });
    },
};

const { dispatch } = getStoreAccessors<MainState | any, State>('');

export const dispatchCheckApiError = dispatch(actions.actionCheckApiError);
export const dispatchCheckSecurity = dispatch(actions.actionCheckSecurity);
export const dispatchCheckLoggedIn = dispatch(actions.actionCheckLoggedIn);
export const dispatchCheckToken = dispatch(actions.actionCheckToken);
export const dispatchLogOut = dispatch(actions.actionLogOut);
export const dispatchUserLogOut = dispatch(actions.actionUserLogOut);
export const dispatchRemoveLogIn = dispatch(actions.actionRemoveLogIn);
export const dispatchRouteLoggedIn = dispatch(actions.actionRouteLoggedIn);
export const dispatchRouteLogOut = dispatch(actions.actionRouteLogOut);
export const dispatchRemoveNotification = dispatch(actions.removeNotification);

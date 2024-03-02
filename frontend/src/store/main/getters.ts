import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';
import { MainState } from './state';

export const getters = {
    loginError: (state: MainState) => state.logInError,
    disconnected: (state: MainState) => state.disconnected,
    dashboardShowDrawer: (state: MainState) => state.dashboardShowDrawer,
    dashboardMiniDrawer: (state: MainState) => state.dashboardMiniDrawer,
    token: (state: MainState) => state.token,
    isLoggedIn: (state: MainState) => state.isLoggedIn,
    firstNotification: (state: MainState) => state.notifications.length > 0 && state.notifications[0],
};

const {read} = getStoreAccessors<MainState, State>('');

export const readDashboardMiniDrawer = read(getters.dashboardMiniDrawer);
export const readDashboardShowDrawer = read(getters.dashboardShowDrawer);
export const readIsLoggedIn = read(getters.isLoggedIn);
export const readLoginError = read(getters.loginError);
export const readToken = read(getters.token);
export const readFirstNotification = read(getters.firstNotification);
export const readDisconnected = read(getters.disconnected);

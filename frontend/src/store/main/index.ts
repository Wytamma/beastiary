import { actions } from './actions';
import { getters } from './getters';
import { mutations } from './mutations';
import { runtimeCapabilities } from '@/runtime';
import { MainState } from './state';

const defaultState: MainState = {
  authEnabled: runtimeCapabilities.supportsAuth,
  isLoggedIn: runtimeCapabilities.supportsAuth ? null : true,
  token: '',
  logInError: false,
  disconnected: false,
  dashboardMiniDrawer: false,
  dashboardShowDrawer: false,
  notifications: [],
};

export const mainModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};

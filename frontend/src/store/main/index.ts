import { actions } from './actions';
import { getters } from './getters';
import { mutations } from './mutations';
import { MainState } from './state';

const defaultState: MainState = {
  isLoggedIn: null,
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

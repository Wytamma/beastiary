import { getStoreAccessors } from "typesafe-vuex";
import { State } from "../state";
import { defaultSettings, mergeSettings } from "./defaults";
import { SettingsState } from "./state";

export const mutations = {
  updateSettings(state: SettingsState, payload: Partial<SettingsState>) {
    Object.assign(state, mergeSettings(state, payload));
  },
  resetSettings(state: SettingsState) {
    Object.assign(state, defaultSettings());
  },
};

const { commit } = getStoreAccessors<SettingsState | any, State>("");

export const commitUpdateSettings = commit(mutations.updateSettings);
export const commitResetSettings = commit(mutations.resetSettings);

import { getStoreAccessors } from "typesafe-vuex";
import { State } from "../state";
import { SettingsState } from "./state";

export const getters = {
  settings: (state: SettingsState) => state,
};

const { read } = getStoreAccessors<SettingsState, State>("");

export const readSettings = read(getters.settings);

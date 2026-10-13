import { loadSettings } from "./defaults";
import { getters } from "./getters";
import { mutations } from "./mutations";

export const settingsModule = {
  state: loadSettings(),
  mutations,
  getters,
};

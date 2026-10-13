import Vue from "vue";
import Vuex, { StoreOptions } from "vuex";

import { dataModule } from "./data";
import { mainModule } from "./main";
import { settingsModule } from "./settings";
import { saveSettings } from "./settings/defaults";
import { State } from "./state";

Vue.use(Vuex);

const storeOptions: StoreOptions<State> = {
  modules: {
    main: mainModule,
    data: dataModule,
    settings: settingsModule,
  },
};

export const store = new Vuex.Store<State>(storeOptions);

store.subscribe((mutation, state: State) => {
  if (mutation.type === "updateSettings" || mutation.type === "resetSettings") {
    saveSettings(state.settings);
  }
});

export default store;

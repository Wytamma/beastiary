import { DataState } from "./data/state";
import { MainState } from "./main/state";
import { SettingsState } from "./settings/state";

export interface State {
  main: MainState;
  data: DataState;
  settings: SettingsState;
}

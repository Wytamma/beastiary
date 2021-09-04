import { DataState } from './data/state';
import { MainState } from './main/state';

export interface State {
    main: MainState;
    data: DataState;
}

import { MainState } from './main/state';
import { DataState } from './data/state';

export interface State {
    main: MainState;
    data: DataState;
}

import { State } from '@/store/state';
import { Store } from 'vuex'; // path to store file

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $store: Store<State>;
  }
}

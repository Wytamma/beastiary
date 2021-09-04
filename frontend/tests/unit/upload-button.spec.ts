import UploadButton from '@/components/UploadButton.vue';
import '@/plugins/vuetify';
import { shallowMount } from '@vue/test-utils';

describe('UploadButton.vue', () => {
  it('renders props.title when passed', () => {
    const title = 'upload a file';
    const wrapper = shallowMount(UploadButton, {
      slots: {
        default: title,
      },
    });
    expect(wrapper.text()).toMatch(title);
  });
});

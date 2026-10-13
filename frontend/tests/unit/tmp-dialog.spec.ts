import SettingsDialog from "@/components/SettingsDialog.vue";
import store from "@/store";
import { mount } from "@vue/test-utils";
import Vue from "vue";
import Vuetify from "vuetify";

Vue.use(Vuetify);

describe("SettingsDialog tmp", () => {
  it("mounts and opens", async () => {
    const errors: any[] = [];
    const spyE = jest.spyOn(console, "error").mockImplementation((...a) => {
      errors.push(a);
    });
    const spyW = jest.spyOn(console, "warn").mockImplementation((...a) => {
      errors.push(a);
    });
    const div = document.createElement("div");
    div.setAttribute("data-app", "true");
    document.body.appendChild(div);
    const wrapper = mount(SettingsDialog, {
      store,
      vuetify: new Vuetify(),
      attachTo: div,
    } as any);
    (wrapper.vm as any).dialog = true;
    await Vue.nextTick();
    await Vue.nextTick();
    const text = document.body.textContent || "";
    spyE.mockRestore();
    spyW.mockRestore();
    console.log(
      text.length,
      text.slice(0, 600),
      errors.map((e) => String(e[0]).slice(0, 500)),
    );
  });
});

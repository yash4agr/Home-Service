import { createStore } from "vuex"; // Correct import for Vuex 4
import thisismodule1 from "./modules/module1";
import thisismodule2 from "./modules/module2";
import admin from "./modules/admin";
import professional from "./modules/professional"

const store = createStore({
  modules: {
    module1: thisismodule1,
    module2: thisismodule2,
    admin: admin,
    professional: professional,
  },
});

export default store;
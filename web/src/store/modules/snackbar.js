// src/store/modules/snackbar.js
const state = {
  snackbar: {
    visible: false,
    message: "",
    color: "success",
    timeout: 3000,
  },
};

const mutations = {
  SHOW_SNACKBAR(state, payload) {
    state.snackbar.visible = true;
    state.snackbar.message = payload.message;
    state.snackbar.color = payload.color || "success";
    state.snackbar.timeout = payload.timeout || 3000;
  },
  HIDE_SNACKBAR(state) {
    state.snackbar.visible = false;
  },
};

const actions = {
  showSnackbar({ commit }, payload) {
    commit("SHOW_SNACKBAR", payload);
  },
  hideSnackbar({ commit }) {
    commit("HIDE_SNACKBAR");
  },
};

const getters = {
  snackbar: (state) => state.snackbar,
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};

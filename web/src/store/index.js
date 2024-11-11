// src/store/index.js
import { createStore } from 'vuex';

export default createStore({
  state: {
    appTitle: '准备就绪',
    pageTitle: '准备就绪',
  },
  mutations: {
    setAppTitle(state, title) {
      state.appTitle = title;
    },
    setPageTitle(state, title) {
      state.pageTitle = title;
    },
  },
});

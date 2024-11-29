// src/store/index.js
import { createStore } from 'vuex';
import axios from "axios";

export default createStore({
  state: {
    userId: null,
    user: null,
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
    setUserId(state, userId) {
      state.userId = userId;
      localStorage.setItem("userId", userId);
    },
    setUserInfo(state, user) {
      state.user = user;
      console.log(user);
      localStorage.setItem("user", JSON.stringify(user));
    },
    cleanUserId(state) {
      state.userId = null;
      state.user = null;
      localStorage.removeItem("userId");
      localStorage.removeItem("user");
      delete axios.defaults.headers.common["Authorization"];
    }
  },
  getters: {
    isAuthenticated: (state) => !!state.user,
    userRole: (state) => {
      if (state.user) {
        return state.user.role;
      } else {
        return -100;
      }
    },
    getUserId: (state) => {
      if (state.user) {
        return state.userId;
      } else {
        return -114514;
      }
    },
  },
});

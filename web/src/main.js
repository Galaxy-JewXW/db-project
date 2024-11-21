/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'
import axios from "axios";

// Components
import App from './App.vue'
import './assets/global.css';
import store from './store';

import VueMarkdownEditor from '@kangc/v-md-editor';
import '@kangc/v-md-editor/lib/style/base-editor.css';

import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';

// highlightjs
import hljs from 'highlight.js';
import createKatexPlugin from '@kangc/v-md-editor/lib/plugins/katex/cdn';
import createLineNumbertPlugin from '@kangc/v-md-editor/lib/plugins/line-number/index';

VMdPreview.use(githubTheme, {
  Hljs: hljs,
});
VMdPreview.use(createKatexPlugin());
VMdPreview.use(createLineNumbertPlugin());

import Prism from 'prismjs';

VueMarkdownEditor.use(githubTheme, {
  Prism,
  Hljs: hljs,
});
VueMarkdownEditor.use(createKatexPlugin());
VueMarkdownEditor.use(createLineNumbertPlugin());

const userId = localStorage.getItem("userId");
if (userId) {
  console.log("got userId");
  axios.defaults.headers.common["Authorization"] = `Bearer ${userId}`;
  store.commit("setUserId", userId);
  const user = JSON.parse(localStorage.getItem("user"));
  if (user) {
    console.log("got User");
    store.commit("setUserInfo", user);
  }
}

// Composables
import { createApp } from 'vue'
const app = createApp(App)

registerPlugins(app)
app.use(store)
app.use(VMdPreview)
app.use(VueMarkdownEditor)
app.mount('#app')

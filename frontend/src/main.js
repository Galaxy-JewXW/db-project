/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'
import './assets/global.css';
import store from './store';

import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';

// highlightjs
import hljs from 'highlight.js';
import createKatexPlugin from '@kangc/v-md-editor/lib/plugins/katex/cdn';

VMdPreview.use(githubTheme, {
  Hljs: hljs,
});
VMdPreview.use(createKatexPlugin());

// Composables
import { createApp } from 'vue'
const app = createApp(App)

registerPlugins(app)
app.use(store)
app.use(VMdPreview)
app.mount('#app')

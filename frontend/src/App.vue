<!-- App.vue -->
<template>
  <v-app>
    <!-- 左侧可扩展侧边栏 -->
    <v-navigation-drawer app expand-on-hover rail permanent>
      <v-list>
        <v-list-item
          prepend-avatar="https://randomuser.me/api/portraits/women/85.jpg"
          title="时间的彷徨"
          subtitle="计算机学院 2025级"
        ></v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <v-list-item
          v-for="item in menuItems"
          :key="item.value"
          :prepend-icon="item.icon"
          :to="item.value"
          link
        >
          <v-list-item-title class="text-subtitle-1">{{
            item.title
          }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- 顶部标题栏 -->
    <v-app-bar app class="pl-0">
      <v-app-bar-title>{{ appTitle }}</v-app-bar-title>
      <v-spacer></v-spacer>
      <div class="time-display">
        <span class="date-part">{{ datePart }}</span>
        <span class="weekday">{{ weekday }}</span>
        <span class="time-part">{{ timePart }}</span>
      </div>
      <!-- 显示时间 -->
    </v-app-bar>

    <!-- 主要内容区域 -->
    <v-main>
      <v-container fluid>
        <v-row>
          <v-col cols="12">
            <router-view></router-view>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "App",
  data() {
    return {
      datePart: "",
      weekday: "",
      timePart: "",
      // appTitle 已经从 Vuex 中获取，不需要在 data 中定义
    };
  },
  computed: {
    ...mapState(["appTitle", "pageTitle"]),
    menuItems() {
      // 根据当前路由是否为 '/login' 动态修改第四个 item
      const isLoginRoute = this.$route.path === "/login";
      return [
        { title: "首页", icon: "mdi-home", value: "/home" },
        { title: "题库", icon: "mdi-database", value: "/problemset" },
        { title: "讨论区", icon: "mdi-forum", value: "/discussions" },
        { title: "个人中心", icon: "mdi-account-circle", value: "/profile" },
        isLoginRoute
          ? { title: "登录", icon: "mdi-login", value: "/login" }
          : { title: "注销", icon: "mdi-logout", value: "/login" },
      ];
    },
  },
  created() {
    this.updateTime();
    this.timer = setInterval(this.updateTime, 1000);
    // 设置初始浏览器标签页标题
    document.title = this.pageTitle || "标题";
  },
  beforeUnmount() {
    clearInterval(this.timer);
  },
  watch: {
    pageTitle(newTitle) {
      document.title = newTitle || "标题";
    },
    // 如果需要监听路由变化，可以保留以下代码
    // '$route'(to) {
    //     // 可以在这里处理路由变化时的逻辑
    // }
  },
  methods: {
    updateTime() {
      const now = new Date();
      const dateOptions = { year: "numeric", month: "2-digit", day: "2-digit" };
      this.datePart = now.toLocaleDateString("zh-CN", dateOptions);
      const weekdayOptions = { weekday: "long" };
      this.weekday = now.toLocaleDateString("zh-CN", weekdayOptions);
      this.timePart = now.toLocaleTimeString("zh-CN");
    },
    // 已经不需要 setTitle 方法，因为标题由 Vuex 管理
  },
};
</script>

<style scoped>
.time-display {
  font-size: 1.25rem;
  margin-right: 16px;
  white-space: nowrap;
  display: flex;
  align-items: center;
}

.date-part {
  margin-right: 12px;
}

.weekday {
  margin-right: 12px;
}

.v-navigation-drawer {
  z-index: 1000;
  /* 确保侧边栏在顶部标题栏之上 */
}

.v-app-bar {
  z-index: 999;
  /* 确保顶部标题栏在侧边栏之下 */
}
</style>

<style>
/* 全局样式 */

html,
body {
  overflow-y: hidden;
}

/* Markdown 内容的全局样式 */
.markdown-content h1 {
  border-bottom: 2px solid #eaecef;
  padding-bottom: 0.3rem;
  margin-bottom: 1rem;
}

.markdown-content pre {
  background-color: #2d2d2d;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  color: #fff;
}

.markdown-content code {
  font-family: "Source Code Pro", monospace;
  font-size: 0.9rem;
}

.markdown-content ul {
  padding-left: 1.5rem;
}

.markdown-content ul li {
  list-style-type: disc;
  margin-left: 0.5rem;
}

/* 表格样式 */
.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
}

.markdown-content table th,
.markdown-content table td {
  padding: 0.75rem;
  border: 1px solid #ddd;
}

.markdown-content table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

/* 链接样式 */
.markdown-content a {
  color: #3498db;
  text-decoration: none;
}

.markdown-content a:hover {
  text-decoration: underline;
}

/* 自定义链接样式，确保链接不影响列表项样式 */
.text-decoration-none {
  text-decoration: none;
  color: inherit;
  display: block;
  width: 100%;
  height: 100%;
}
</style>

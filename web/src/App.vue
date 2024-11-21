<!-- App.vue -->
<template>
  <v-app>
    <!-- 左侧可扩展侧边栏 -->
    <v-navigation-drawer v-if="!isLoginRoute" app expand-on-hover rail permanent>
      <v-list>
        <v-list-item prepend-avatar="https://randomuser.me/api/portraits/women/85.jpg" title="时间的彷徨"
          subtitle="计算机学院 2025级"></v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <v-list-item v-for="item in menuItems" :key="item.value" :prepend-icon="item.icon" :to="item.value" link>
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
    isLoginRoute() {
      return this.$route.path === "/login";
    },
    menuItems() {
      const isLoginRoute = this.isLoginRoute;
      return [
        { title: "首页", icon: "mdi-home", value: "/home" },
        { title: "题库", icon: "mdi-database", value: "/problemset" },
        { title: "模拟测试", icon: "mdi-file-sign", value: "/exam" },
        { title: "讨论区", icon: "mdi-forum", value: "/forum" },
        { title: "个人中心", icon: "mdi-account-details", value: "/profile" },
        isLoginRoute
          ? { title: "登录", icon: "mdi-login", value: "/login" }
          : { title: "注销", icon: "mdi-logout", value: "/logout" },
      ];
    },
  },
  created() {
    this.updateTime();
    this.timer = setInterval(this.updateTime, 1000);
    document.title = this.pageTitle || "标题";
  },
  beforeUnmount() {
    clearInterval(this.timer);
  },
  watch: {
    pageTitle(newTitle) {
      document.title = newTitle || "标题";
    },
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
}

.v-app-bar {
  z-index: 999;
}
</style>

<style>
html,
body {
  overflow-y: hidden;
}

.text-decoration-none {
  text-decoration: none;
  color: inherit;
  display: block;
  width: 100%;
  height: 100%;
}
</style>

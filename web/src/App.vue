<!-- App.vue -->
<template>
  <v-app>
    <!-- 左侧可扩展侧边栏 -->
    <v-navigation-drawer v-if="!isLoginRoute" app expand-on-hover rail permanent>
      <v-list>
        <v-list-item :prepend-avatar="userAvatar" :title="userTitle" :subtitle="userSubtitle"></v-list-item>
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
    };
  },
  computed: {
    ...mapState(["appTitle", "pageTitle", "user"]),
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
    userAvatar() {
      // 如果 user 存在并且包含 urls.avatar 字段，则使用它，否则提供默认头像
      return this.user && this.user.urls
        ? this.user.urls
        : "https://randomuser.me/api/portraits/lego/1.jpg";
    },
    userTitle() {
      // 如果 user 存在并且有 name 字段，则返回 name，否则提供默认名称
      return this.user && this.user.name ? this.user.name : "未登录用户";
    },
    userSubtitle() {
      // 如果 user 存在，则格式化 entry_year 和 college，否则提供默认副标题
      return this.user && this.user.entry_year && this.user.college
        ? `${this.user.college} ${this.user.entry_year}级`
        : "请登录";
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

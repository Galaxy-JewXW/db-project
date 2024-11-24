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
      <v-menu v-if="canChangeRole">
        <template v-slot:activator="{ props }">
          <v-btn :prepend-icon="icons[currentRole]" variant="text" v-bind="props">切换角色</v-btn>
        </template>
        <v-list>
          <v-list-item v-for="(item, index) in items" :key="index" :value="index" @click="selectRole(item.title)">
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <div class="info-display ml-2">
        <span class="date-part">{{ datePart }}</span>
        <span class="weekday">{{ weekday }}</span>
        <span class="time-part">{{ timePart }}</span>
      </div>
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
import store from '@/store';

export default {
  name: "App",
  data() {
    return {
      datePart: "",
      weekday: "",
      timePart: "",
      items: [
        { title: '学生' },
        { title: '辅导师' }
      ],
      icons: {
        '学生': 'mdi-account-school', '辅导师': 'mdi-cast-education'
      },
      currentRole: '学生',
    };
  },
  computed: {
    ...mapState(["appTitle", "pageTitle", "user"]),
    isLoginRoute() {
      return this.$route.path === "/login";
    },
    canChangeRole() {
      const userRole = store.getters.userRole ? store.getters.userRole : -1;
      return userRole >= 1;
    },
    menuItems() {
      const isLoginRoute = this.isLoginRoute;

      if (this.currentRole === '辅导师') {
        // 如果是辅导师，返回特殊的菜单项
        return [
          { title: "首页", icon: "mdi-home", value: "/admin/home" },
          { title: "题目管理", icon: "mdi-file-edit", value: "/admin/exercise" },
          { title: "题库管理", icon: "mdi-database-edit", value: "/admin/problemset" },
          { title: "模拟测试管理", icon: "mdi-arrange-send-backward", value: "/admin/exam" },
          { title: "模拟测试评分", icon: "mdi-abugida-devanagari", value: "/admin/judge" },
          { title: "讨论区", icon: "mdi-forum", value: "/admin/forum" },
          { title: "个人中心", icon: "mdi-account-details", value: "/admin/profile" },
          isLoginRoute
            ? { title: "登录", icon: "mdi-login", value: "/login" }
            : { title: "注销", icon: "mdi-logout", value: "/logout" },
        ];
      } else {
        // 默认菜单项 (学生)
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
      }
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
        ? `${this.user.entry_year}级 ${this.user.college}`
        : "请登录";
    },
  },
  created() {
    this.updateTime();
    this.timer = setInterval(this.updateTime, 1000);
    document.title = this.pageTitle || "标题";
    this.setRoleBasedOnRoute();
  },
  beforeUnmount() {
    clearInterval(this.timer);
  },
  watch: {
    $route(to, from) {
      this.setRoleBasedOnRoute();
    },
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
    selectRole(role) {
      if (role === "辅导师") {
        if (this.currentRole !== role) {
          this.$router.push("/admin/home");
        }
        this.currentRole = role;
        console.log(this.currentRole);
      } else if (role === "学生") {
        if (this.currentRole !== role) {
          this.$router.push("/");
        }
        this.currentRole = role;
        console.log(this.currentRole);
      } else {
        this.$router.push("/404");
      }
    },
    setRoleBasedOnRoute() {
      // 根据路由中是否包含 "/admin" 来设置 currentRole
      if (this.$route.path.includes("/admin")) {
        this.currentRole = '辅导师';
      } else {
        this.currentRole = '学生';
      }
    },
  },
};
</script>

<style scoped>
.info-display {
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

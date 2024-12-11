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
      <template v-slot:append>
        <v-menu v-if="!isLoginRoute" :close-on-content-click="false" location="bottum" open-on-hover>
          <template v-slot:activator="{ props }">
            <v-btn icon="mdi-bell" v-bind="props"></v-btn>
          </template>
          <v-card style="min-width: 475px; max-width: 500px;">
            <v-card-title>
              <v-row class="fill-height pt-2 pb-2" align="center" justify="space-between">
                <span class="pl-2">系统通知</span>
                <v-btn icon variant="text" @click="markAllAsRead">
                  <v-icon>mdi-check-all</v-icon>
                </v-btn>
              </v-row>
            </v-card-title>
            <v-divider></v-divider>
            <v-tabs v-model="tab" color="primary" density="compact" grow>
              <v-tab value="unread">未读消息</v-tab>
              <v-tab value="read">已读消息</v-tab>
            </v-tabs>
            <v-card-text class="pa-0">
              <v-tabs-window v-model="tab">
                <v-tabs-window-item value="unread">
                  <div v-if="unreadmessages.length > 0">
                    <!-- 未读消息分页 -->
                    <v-pagination v-if="totalPagesUnread > 1" v-model="currentPageUnread" :length="totalPagesUnread"
                      total-visible="5" class="mt-2"></v-pagination>
                    <v-list lines="two" class="pa-0">
                      <v-list-item v-for="notice in paginatedUnreadMessages" :key="notice.id"
                        @click="openMessageDialog(notice)">
                        <v-list-item-title class="font-weight-medium">
                          <v-row align="center">
                            <v-col cols="auto">
                              {{ notice.sender }}
                            </v-col>
                            <v-col cols="auto" class="text-body-2">
                              {{ formatDate(notice.sendTime) }}
                            </v-col>
                          </v-row>
                        </v-list-item-title>
                        <v-list-item-subtitle>
                          {{ getMessagePreview(notice.content) }}
                        </v-list-item-subtitle>
                        <template v-slot:append>
                          <v-btn icon variant="text" @click.stop="markAsRead(notice)">
                            <v-icon>mdi-check</v-icon>
                          </v-btn>
                        </template>
                      </v-list-item>
                    </v-list>
                  </div>
                  <div class="no-results" v-else>
                    暂无未读消息
                  </div>
                </v-tabs-window-item>
                <v-tabs-window-item value="read">
                  <div v-if="readmessages.length > 0">
                    <v-pagination v-if="totalPagesRead > 1" v-model="currentPageRead" :length="totalPagesRead"
                      total-visible="5" class="mt-2"></v-pagination>
                    <v-list lines="two" class="pa-0">
                      <v-list-item v-for="notice in paginatedReadMessages" :key="notice.id"
                        @click="openMessageDialog(notice)">
                        <v-list-item-title class="font-weight-medium">
                          <v-row align="center">
                            <v-col cols="auto">
                              {{ notice.sender }}
                            </v-col>
                            <v-col cols="auto" class="text-body-2">
                              {{ formatDate(notice.sendTime) }}
                            </v-col>
                          </v-row>
                        </v-list-item-title>
                        <v-list-item-subtitle>
                          {{ getMessagePreview(notice.content) }}
                        </v-list-item-subtitle>
                        <template v-slot:append>
                          <v-btn icon variant="text" @click.stop="markAsUnread(notice)">
                            <v-icon>mdi-close</v-icon>
                          </v-btn>
                        </template>
                      </v-list-item>
                    </v-list>
                  </div>
                  <div class="no-results" v-else>
                    暂无已读消息
                  </div>
                </v-tabs-window-item>
              </v-tabs-window>
            </v-card-text>
          </v-card>
        </v-menu>
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
      </template>
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

    <v-snackbar v-model="snackbar.visible" :timeout="snackbar.timeout" :color="snackbar.color" min-width="25%"
      style="z-index: 100000;">
      <div style="font-size: 16px">{{ snackbar.message }}</div>
      <template #actions>
        <v-btn icon @click="hideSnackbar">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>

    <v-dialog v-model="messageDialogVisible" max-width="60%">
      <v-card>
        <v-card-title class="dialog-title">{{ selectedMessage.sender }}</v-card-title>
        <v-card-subtitle class="dialog-subtitle">
          {{ formatDate(selectedMessage.sendTime) }}
        </v-card-subtitle>
        <v-card-text>
          <v-md-preview :text="selectedMessage.content"></v-md-preview>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="closeMessageDialog">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import { mapState, mapGetters, mapActions } from "vuex";
import store from '@/store';
import axios from 'axios';

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
      allmessages: [],
      readmessages: [],
      unreadmessages: [],
      tab: null,
      messageDialogVisible: false,
      selectedMessage: null,
      itemsPerPage: 5, // 每页显示5个通知
      currentPageUnread: 1, // 未读消息的当前页
      currentPageRead: 1, // 已读消息的当前页
    };
  },
  computed: {
    ...mapState(["appTitle", "pageTitle", "user"]),
    ...mapGetters('snackbar', ['snackbar']),
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
          { title: "模拟测试评分", icon: "mdi-chart-arc", value: "/admin/judge" },
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
    paginatedUnreadMessages() {
      const start = (this.currentPageUnread - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.unreadmessages.slice(start, end);
    },
    paginatedReadMessages() {
      const start = (this.currentPageRead - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.readmessages.slice(start, end);
    },
    totalPagesUnread() {
      return Math.ceil(this.unreadmessages.length / this.itemsPerPage);
    },
    totalPagesRead() {
      return Math.ceil(this.readmessages.length / this.itemsPerPage);
    },
  },
  created() {
    this.updateTime();
    this.timer = setInterval(this.updateTime, 1000);
    document.title = this.pageTitle || "标题";
    this.setRoleBasedOnRoute();
    if (!this.isLoginRoute) {
      this.fetchNotice();
    }
  },
  beforeUnmount() {
    clearInterval(this.timer);
  },
  watch: {
    $route(to, from) {
      this.setRoleBasedOnRoute();
      if (!this.isLoginRoute) {
        this.fetchNotice();
      }
    },
    pageTitle(newTitle) {
      document.title = newTitle || "标题";
    },
  },
  methods: {
    ...mapActions('snackbar', ['hideSnackbar', 'showSnackbar']),
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
      // After changing role, refetch notices to ensure correct message sorting
      if (!this.isLoginRoute) {
        this.fetchNotice();
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
    formatDate(dateString) {
      const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false, // 使用24小时制
      };
      const date = new Date(dateString);
      return date.toLocaleString("zh-CN", options).replace(/\//g, "-");
    },
    openMessageDialog(message) {
      this.selectedMessage = message;
      this.messageDialogVisible = true;
    },
    closeMessageDialog() {
      this.messageDialogVisible = false;
    },
    getMessagePreview(content) {
      const maxLength = 26;
      if (content.length <= maxLength) {
        return content;
      }
      return content.substring(0, maxLength) + "...";
    },
    async markAsRead(notice) {
      notice.read = true;
      this.unreadmessages = this.unreadmessages.filter(item => item.id !== notice.id);
      this.readmessages.push(notice);
      this.sortMessages(this.readmessages);
      const userId = this.$store.getters.getUserId;
      const requestData = {
        user_id: userId,
        message_id: notice.id
      };
      let url = 'http://127.0.0.1:8000/api/message/read_message/';
      const response = await axios.post(url, requestData, {
        headers: {
          'Content-Type': 'application/json',  // 指定请求体的格式为 JSON
        }
      });
      this.showSnackbar({
        message: `已将“${notice.sender}”设置为已读`,
        color: 'success',
        timeout: 2000
      });
    },
    async markAsUnread(notice) {
      notice.read = false;
      this.readmessages = this.readmessages.filter(item => item.id !== notice.id);
      this.unreadmessages.push(notice);
      this.sortMessages(this.unreadmessages);
      const userId = this.$store.getters.getUserId;
      const requestData = {
        user_id: userId,
        message_id: notice.id
      };
      let url = 'http://127.0.0.1:8000/api/message/unread_message/';
      const response = await axios.post(url, requestData, {
        headers: {
          'Content-Type': 'application/json',  // 指定请求体的格式为 JSON
        }
      });
      this.showSnackbar({
        message: `已将“${notice.sender}”设置为未读`,
        color: 'warning',
        timeout: 2000
      });
    },
    async markAllAsRead() {
      this.unreadmessages.forEach(notice => {
        notice.read = true;
        this.readmessages.push(notice);
      });
      const userId = this.$store.getters.getUserId;
      const requestData = {
        user_id: userId,
      };
      let url = 'http://127.0.0.1:8000/api/message/read_all_message/';
      const response = await axios.post(url, requestData, {
        headers: {
          'Content-Type': 'application/json',  // 指定请求体的格式为 JSON
        }
      });
      this.unreadmessages = [];
      this.sortMessages(this.readmessages);
      this.showSnackbar({
        message: '已将所有通知设置为已读',
        color: 'success',
        timeout: 2000
      });
    },
    async fetchNotice() {
      const requestData = {
        user_id: store.getters.getUserId
      };
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/board/', requestData, {
          headers: {
            'Content-Type': 'application/json',
          }
        });
        const messages_data = response.data.data.messages;
        console.log(messages_data);
        this.readmessages = [];
        this.unreadmessages = [];
        this.allmessages = [];
        messages_data.forEach((m) => {
          const message = {
            id: m.id,
            sender: m.sender,
            sendTime: m.sent_at,
            content: m.content,
            avatar: m.sender_avatar,
            read: m.is_read || false,
          };
          if (m.is_read === false || m.is_read === undefined) {
            this.unreadmessages.push(message);
          } else {
            this.readmessages.push(message);
          }
          this.allmessages.push(message);
        });
        // Sort both unread and read messages by sendTime descending
        this.sortMessages(this.unreadmessages);
        this.sortMessages(this.readmessages);
        this.currentPageRead = 1;
        this.currentPageUnread = 1;
      } catch (error) {
        console.error('Error fetching messages:', error);
      }
    },
    sortMessages(messagesArray) {
      messagesArray.sort((a, b) => new Date(b.sendTime) - new Date(a.sendTime));
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

.no-results {
  font-size: 1rem;
  color: #777;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  padding-top: 10px;
  padding-bottom: 10px;
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

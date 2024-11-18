<template>
  <div class="scroll-container">
    <!-- 主讨论卡片 -->
    <v-card class="mx-auto main-card" max-width="85%">
      <v-card-item :prepend-avatar="mainDiscussion.avatar">
        <v-card-item-title class="text-h6 font-weight-regular">
          <v-row align="center" no-gutters>
            <v-col cols="auto">
              {{ mainDiscussion.publisher }}
            </v-col>
          </v-row>
        </v-card-item-title>
        <v-card-item-subtitle>
          <v-row align="center" no-gutters>
            <v-col cols="auto" class="text-body-1 text-disabled">
              {{ formatDate(mainDiscussion.publishTime) }}
            </v-col>
          </v-row>
        </v-card-item-subtitle>
        <template v-slot:append>
          <v-icon v-if="isLiked.main" color="#ee3f4d">mdi-thumb-up</v-icon>
          <v-icon v-if="isSubscribed" color="#fbc02d">mdi-bell</v-icon>
        </template>
      </v-card-item>
      <v-card-text>
        <v-divider style="padding-top: 10px; padding-bottom: 0px"></v-divider>
        <!-- 显示内容 -->
        <div style="margin-left: -29px">
          <v-md-preview :text="mainDiscussion.content"></v-md-preview>
        </div>
      </v-card-text>
      <!-- 订阅和点赞按钮区域 -->
      <v-divider></v-divider>
      <!-- Wrap buttons in a v-row for horizontal layout -->
      <v-row no-gutters>
        <v-col cols="auto">
          <v-btn
            @click="toggleLike('main')"
            class="like-btn"
            :variant="isLiked.main ? 'tonal' : 'text'"
            :color="'#ee3f4d'"
          >
            <v-icon>{{
              isLiked.main ? "mdi-thumb-up" : "mdi-thumb-up-outline"
            }}</v-icon>
            {{ isLiked.main ? "取消点赞" : "点赞" }}
          </v-btn>
        </v-col>
        <v-col cols="auto">
          <v-btn
            @click="toggleSubscription"
            class="subscribe-btn"
            :variant="isSubscribed ? 'tonal' : 'text'"
            :color="'#fbc02d'"
          >
            <v-icon>{{ isSubscribed ? "mdi-bell-off" : "mdi-bell" }}</v-icon>
            {{ isSubscribed ? "取消订阅" : "订阅" }}
          </v-btn>
        </v-col>
      </v-row>
    </v-card>

    <!-- 跟随的讨论列表 -->
    <div v-for="discussion in followDiscussion" :key="discussion.id">
      <v-card class="mx-auto follow-card" max-width="85%">
        <v-card-item :prepend-avatar="discussion.avatar">
          <v-card-item-title class="text-h6 font-weight-regular">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                {{ discussion.publisher }}
              </v-col>
            </v-row>
          </v-card-item-title>
          <v-card-item-subtitle>
            <v-row align="center" no-gutters>
              <v-col cols="auto" class="text-body-1 text-disabled">
                {{ formatDate(discussion.publishTime) }}
              </v-col>
            </v-row>
          </v-card-item-subtitle>
          <template v-slot:append>
            <v-icon v-if="isLiked[discussion.id]" color="#ee3f4d"
              >mdi-thumb-up</v-icon
            >
          </template>
        </v-card-item>
        <v-card-text>
          <v-divider style="padding-top: 10px; padding-bottom: 0px"></v-divider>
          <!-- 显示跟随讨论内容 -->
          <div style="margin-left: -29px">
            <v-md-preview :text="discussion.content"></v-md-preview>
          </div>
        </v-card-text>
        <!-- 点赞按钮区域 -->
        <v-divider></v-divider>
        <v-btn
          @click="toggleLike(discussion.id)"
          class="like-btn"
          :variant="isLiked[discussion.id] ? 'tonal' : 'text'"
          :color="'#ee3f4d'"
        >
          <v-icon>{{
            isLiked[discussion.id] ? "mdi-thumb-up" : "mdi-thumb-up-outline"
          }}</v-icon>
          {{ isLiked[discussion.id] ? "取消点赞" : "点赞" }}
        </v-btn>
      </v-card>
    </div>
  </div>

  <v-btn class="floating-btn" fab color="primary" @click="returnForum()">
    <v-icon size="32">mdi-arrow-collapse-left</v-icon>
  </v-btn>
</template>

<script>
import { mapMutations } from "vuex";

export default {
  name: "ForumContent",
  data() {
    return {
      mainDiscussion: {
        id: 2,
        title: "离散数学在计算机科学中的应用",
        publisher: "李四",
        avatar: "https://randomuser.me/api/portraits/women/40.jpg",
        publishTime: "2024-09-25T15:30:00",
        lastUpdated: "2024-11-15T15:30:00",
        tag: "离散数学（信息类）",
        content: `
  # Markdown 测试文档
  ...
  `, // 保持原始内容
      },
      isSubscribed: false, // 订阅状态
      isLiked: {
        main: false, // 主讨论的点赞状态
        // 跟随讨论的点赞状态，按讨论 ID 存储
        3: false,
        30: false,
      },
      followDiscussion: [
        {
          id: 3,
          publisher: "李四2",
          avatar: "https://randomuser.me/api/portraits/women/10.jpg",
          publishTime: "2024-09-25T15:30:00",
          lastUpdated: "2024-11-15T15:30:00",
          content: "内容1",
        },
        {
          id: 30,
          publisher: "李四3",
          avatar: "https://randomuser.me/api/portraits/women/98.jpg",
          publishTime: "2024-09-25T15:30:00",
          lastUpdated: "2024-11-15T15:30:00",
          content: "内容2",
        },
      ],
    };
  },
  mounted() {
    // 更新标题
    const title = `讨论 - ${this.mainDiscussion.title}`; // 动态设置标题
    this.setAppTitle(title); // 设置应用的标题
    this.setPageTitle(title); // 设置页面的标题
  },
  methods: {
    ...mapMutations(["setAppTitle", "setPageTitle"]),
    formatDate(dateStr) {
      const options = {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      };
      return new Date(dateStr).toLocaleString(undefined, options);
    },
    returnForum() {
      this.$router.push(`/forum`);
    },
    toggleSubscription() {
      this.isSubscribed = !this.isSubscribed;
    },
    toggleLike(discussionId) {
      if (discussionId === "main") {
        // 切换主讨论的点赞状态
        this.isLiked.main = !this.isLiked.main;
      } else {
        // 直接修改 isLiked 对象的点赞状态
        this.isLiked[discussionId] = !this.isLiked[discussionId];
      }
    },
  },
};
</script>

<style scoped>
.scroll-container {
  flex: 1 1 auto;
  overflow-y: auto;
  padding: 16px;
  padding-bottom: 80px;
  height: 98vh;
  max-height: 98vh;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scroll-container::-webkit-scrollbar {
  display: none;
}

.floating-btn {
  position: fixed;
  right: 4%;
  bottom: 10%;
  z-index: 9999;
  border-radius: 75%;
  width: 64px;
  height: 64px;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 增加主讨论和跟随讨论之间的间隔 */
.main-card {
  margin-bottom: 30px;
}

.follow-card {
  margin-bottom: 30px;
}

.subscribe-btn,
.like-btn {
  width: auto;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  margin-top: 0px;
}
</style>

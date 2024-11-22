<template>
  <div class="scroll-container">
    <!-- 主讨论卡片和评论卡片作为一个整体 -->
    <v-card class="mx-auto main-card" max-width="85%">
      <!-- 主讨论部分 -->
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
          <v-icon v-if="mainDiscussion.isLiked" color="#ee3f4d">mdi-thumb-up</v-icon>
          <v-icon v-if="isSubscribed" color="#fbc02d">mdi-bell</v-icon>
        </template>
      </v-card-item>
      <v-card-text>
        <v-divider style="padding-top: 10px; padding-bottom: 0px"></v-divider>
        <!-- 显示主讨论内容 -->
        <div style="margin-left: -29px">
          <v-md-preview :text="mainDiscussion.content"></v-md-preview>
        </div>
      </v-card-text>

      <!-- 订阅和点赞按钮区域 -->
      <v-divider></v-divider>
      <v-row no-gutters>
        <v-col cols="auto">
          <v-btn rounded="0" @click="toggleLike('main')" class="like-btn"
            :variant="mainDiscussion.isLiked ? 'tonal' : 'text'" :color="'#ee3f4d'">
            <v-icon>{{ mainDiscussion.isLiked ? "mdi-thumb-up" : "mdi-thumb-up-outline" }}</v-icon>
            {{ mainDiscussion.isLiked ? "取消点赞" : "点赞" }}
          </v-btn>
        </v-col>
        <v-col cols="auto">
          <v-btn rounded="0" @click="toggleSubscription" class="subscribe-btn"
            :variant="isSubscribed ? 'tonal' : 'text'" :color="'#fbc02d'">
            <v-icon>{{ isSubscribed ? "mdi-bell-off" : "mdi-bell-outline" }}</v-icon>
            {{ isSubscribed ? "取消订阅" : "订阅" }}
          </v-btn>
        </v-col>
        <v-col cols="auto">
          <v-btn rounded="0" variant="text" :color="'#574266'">
            <v-icon left>mdi-comment-outline</v-icon>
            评论
          </v-btn>
        </v-col>
        <v-col cols="auto">
          <v-btn rounded="0" variant="text" :color="'#1867c0'">
            <v-icon left>mdi-pencil</v-icon>
            编辑
          </v-btn>
        </v-col>
      </v-row>

    </v-card>

    <div v-for="discussion in followDiscussion" :key="discussion.id">
      <v-card class="mx-auto follow-card" max-width="85%" style="margin-bottom: 20px;">
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
            <v-icon v-if="discussion.isLiked" color="#ee3f4d">mdi-thumb-up</v-icon>
          </template>
        </v-card-item>
        <v-card-text>
          <v-divider style="padding-top: 10px; padding-bottom: 0px"></v-divider>
          <!-- 显示跟随讨论内容 -->
          <div style="margin-left: -29px">
            <v-md-preview :text="discussion.content"></v-md-preview>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-row no-gutters>
          <v-col cols="auto">
            <v-btn rounded="0" @click="toggleLike(discussion.id)" class="like-btn"
              :variant="discussion.isLiked ? 'tonal' : 'text'" :color="'#ee3f4d'">
              <v-icon>{{ discussion.isLiked ? "mdi-thumb-up" : "mdi-thumb-up-outline" }}</v-icon>
              {{ discussion.isLiked ? "取消点赞" : "点赞" }}
            </v-btn>
          </v-col>
          <v-col cols="auto">
            <v-btn rounded="0" variant="text" :color="'#574266'">
              <v-icon left>mdi-comment-outline</v-icon>
              评论
            </v-btn>
          </v-col>
          <v-col cols="auto">
            <v-btn rounded="0" variant="text" :color="'#1867c0'">
              <v-icon left>mdi-pencil</v-icon>
              编辑
            </v-btn>
          </v-col>
        </v-row>
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
  `,
        isLiked: false,
      },
      isSubscribed: false,
      followDiscussion: [
        {
          id: 3,
          publisher: "李四2",
          avatar: "https://randomuser.me/api/portraits/women/10.jpg",
          publishTime: "2024-09-25T15:30:00",
          lastUpdated: "2024-11-15T15:30:00",
          content: "内容1",
          isLiked: false,
        },
        {
          id: 30,
          publisher: "李四3",
          avatar: "https://randomuser.me/api/portraits/women/98.jpg",
          publishTime: "2024-09-25T15:30:00",
          lastUpdated: "2024-11-15T15:30:00",
          content: "内容2",
          isLiked: false,
        },
      ],
    };
  },
  mounted() {
    const title = `讨论 - ${this.mainDiscussion.title}`;
    this.setAppTitle(title);
    this.setPageTitle(title);
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
        this.mainDiscussion.isLiked = !this.mainDiscussion.isLiked;
      } else {
        // 检查是否是跟随讨论的ID
        const discussion = this.followDiscussion.find(
          (d) => d.id === discussionId
        );
        if (discussion) {
          discussion.isLiked = !discussion.isLiked;
          return;
        }
        // 如果ID未找到，抛出错误或忽略
        console.warn(`未找到对应的讨论或评论，ID: ${discussionId}`);
      }
    },
  },
};
</script>

<style scoped>
.scroll-container {
  flex-direction: column;
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

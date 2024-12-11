<template>
  <v-container v-if="loading" class="scroll-container">
    <v-skeleton-loader class="mx-auto border main-card" max-width="100%"
      type="card-avatar, actions"></v-skeleton-loader>
  </v-container>
  <div v-else class="scroll-container">
    <!-- 主讨论卡片和评论卡片作为一个整体 -->
    <v-card class="mx-auto main-card" max-width="85%">
      <!-- 主讨论部分 -->
      <v-card-item :prepend-avatar="mainDiscussion.avatar">
        <template v-slot:title class="text-h6 font-weight-regular">
          <v-row align="center" no-gutters>
            <v-col cols="auto">
              {{ mainDiscussion.publisher }}
            </v-col>
          </v-row>
        </template>
        <template v-slot:subtitle>
          <v-row align="center" no-gutters>
            <v-col cols="auto" class="text-body-1 text-disabled">
              {{ formatDate(mainDiscussion.publishTime) }}
            </v-col>
          </v-row>
        </template>
        <template v-slot:append>
          <v-icon v-if="mainDiscussion.isLiked" color="#ee3f4d">mdi-thumb-up</v-icon>
          <v-icon v-if="isSubscribed" color="#fbc02d">mdi-bell</v-icon>
        </template>
      </v-card-item>
      <v-divider></v-divider>
      <v-card-text>
        <!-- 显示主讨论内容 -->
        <div style="margin-left: -29px">
          <v-md-preview :text="mainDiscussion.content"></v-md-preview>
        </div>
      </v-card-text>
      <v-divider></v-divider>
      <div class="pl-4 text-body-2 text-medium-emphasis pt-2 pb-2">
        最近更新于 {{ formatDate(mainDiscussion.lastUpdated) }}
      </div>
      <!-- 订阅和点赞按钮区域 -->
      <v-divider></v-divider>
      <v-row no-gutters>
        <v-col cols="auto">
          <v-btn rounded="0" @click="toggleLike('main')" class="like-btn"
            :variant="mainDiscussion.isLiked ? 'tonal' : 'text'" color="#ee3f4d">
            <v-icon>{{
              mainDiscussion.isLiked ? "mdi-thumb-up" : "mdi-thumb-up-outline"
            }}</v-icon>
            &nbsp;{{ mainDiscussion.like_count }}
          </v-btn>
        </v-col>
        <v-col cols="auto">
          <v-btn rounded="0" @click="toggleSubscription" class="subscribe-btn"
            :variant="isSubscribed ? 'tonal' : 'text'" :color="'#fbc02d'">
            <v-icon>{{
              isSubscribed ? "mdi-bell-off" : "mdi-bell-outline"
            }}</v-icon>
            &nbsp;{{ mainDiscussion.sub_count }}
          </v-btn>
        </v-col>
        <v-col cols="auto">
          <v-btn rounded="0" variant="text" :color="'#574266'"
            @click="commentDiscussion(mainDiscussion.id, true, true)">
            <v-icon left>mdi-comment-outline</v-icon>
            评论
          </v-btn>
        </v-col>
        <v-col v-if="mainDiscussion.publisherId == currentUserId" cols="auto" @click="
          editDiscussion(
            mainDiscussion.id,
            mainDiscussion.content,
            true,
            false
          )
          ">
          <v-btn rounded="0" variant="text" :color="'#1867c0'">
            <v-icon left>mdi-pencil</v-icon>
            编辑
          </v-btn>
        </v-col>
        <v-col v-if="mainDiscussion.publisherId == currentUserId" cols="auto">
          <v-btn rounded="0" variant="text" :color="'red'" @click="confirmDelete(1, true)">
            <v-icon left>mdi-trash-can-outline</v-icon>
            删除
          </v-btn>
        </v-col>
      </v-row>
    </v-card>

    <div v-for="discussion in followDiscussion" :key="discussion.id">
      <v-card class="mx-auto follow-card" max-width="85%" style="margin-bottom: 20px">
        <v-card-item :prepend-avatar="discussion.avatar">
          <template v-slot:title class="text-h6 font-weight-regular">
            <v-row align="center" no-gutters>
              <v-col cols="auto">
                {{ discussion.publisher }}
              </v-col>
            </v-row>
          </template>
          <template v-slot:subtitle>
            <v-row align="center" no-gutters>
              <v-col cols="auto" class="text-body-1 text-disabled">
                {{ formatDate(discussion.publishTime) }}
              </v-col>
            </v-row>
          </template>
          <template v-slot:append>
            <v-icon v-if="discussion.isLiked" color="#ee3f4d">mdi-thumb-up</v-icon>
          </template>
        </v-card-item>
        <v-divider></v-divider>
        <v-card-text>
          <!-- 显示跟随讨论内容 -->
          <div style="margin-left: -29px">
            <v-md-preview :text="discussion.content"></v-md-preview>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <div class="pl-4 text-body-2 text-medium-emphasis pt-2 pb-2">
          最近更新于 {{ formatDate(discussion.lastUpdated) }}
        </div>
        <v-divider></v-divider>
        <v-row no-gutters>
          <v-col cols="auto">
            <v-btn rounded="0" @click="toggleLike(discussion.id)" class="like-btn"
              :variant="discussion.isLiked ? 'tonal' : 'text'" :color="'#ee3f4d'">
              <v-icon>{{
                discussion.isLiked ? "mdi-thumb-up" : "mdi-thumb-up-outline"
              }}</v-icon>
              &nbsp;{{ discussion.like_count }}
            </v-btn>
          </v-col>
          <v-col cols="auto">
            <v-btn rounded="0" variant="text" :color="'#574266'" @click="commentDiscussion(discussion.id, false, true)">
              <v-icon left>mdi-comment-outline</v-icon>
              评论
            </v-btn>
          </v-col>
          <v-col v-if="discussion.publisherId == currentUserId" cols="auto">
            <v-btn rounded="0" variant="text" :color="'#1867c0'" @click="
              editDiscussion(discussion.id, discussion.content, false, false)
              ">
              <v-icon left>mdi-pencil</v-icon>
              编辑
            </v-btn>
          </v-col>
          <v-col v-if="discussion.publisherId == currentUserId" cols="auto">
            <v-btn rounded="0" variant="text" :color="'red'" @click="confirmDelete(discussion.id, false)">
              <v-icon left>mdi-trash-can-outline</v-icon>
              删除
            </v-btn>
          </v-col>
        </v-row>
      </v-card>
    </div>
  </div>

  <v-btn class="floating-btn" fab color="primary" @click="returnForum()">
    <v-icon size="32">mdi-arrow-collapse-left</v-icon>
  </v-btn>

  <v-dialog v-model="editDialog" height="45%" width="60%">
    <v-card title="编辑">
      <v-md-editor v-model="text" height="325px" width="20%"
        left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | link image code"
        right-toolbar="preview toc sync-scroll"></v-md-editor>
      <v-spacer></v-spacer>
      <v-card-actions>
        <v-btn color="primary" variant="text" @click="emitEdit">提交</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog v-model="commentDialog" height="45%" width="60%">
    <v-card title="评论">
      <v-md-editor v-model="text" height="325px" width="20%"
        left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | link image code"
        right-toolbar="preview toc sync-scroll"></v-md-editor>
      <v-spacer></v-spacer>
      <v-card-actions>
        <v-btn color="primary" variant="text" @click="emitEdit">提交</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog v-model="confirmDialog" max-width="400px">
    <v-card>
      <v-card-title>
        <v-icon color="primary">mdi-alert-circle-outline</v-icon>
        <span class="headline ml-2">操作不可逆</span>
      </v-card-title>
      <v-card-text>确定删除{{ this.toDeleteContent.content }}吗？
        <div v-if="this.toDeleteContent.isMainDiscussion">
          注意：删除讨论贴后，所有的评论也会被删除。
        </div>
      </v-card-text>
      <v-card-actions>
        <v-btn color="red" variant="text" @click="
          deleted(
            this.toDeleteContent.id,
            this.toDeleteContent.isMainDiscussion
          ); this.confirmDialog = false;
        ">
          确定
        </v-btn>
        <v-btn variant="plain" @click="confirmDialog = false"> 取消 </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from "axios";
import { mapMutations, mapActions } from "vuex";
import { mapState } from "vuex/dist/vuex.cjs.js";
import store from "@/store";
export default {
  name: "ForumContent",
  inheritAttrs: false,
  data() {
    return {
      currentUserId: null,
      editDialog: false,
      commentDialog: false,
      confirmDialog: false,
      isMainDiscussion: false,
      isComment: false,
      emitId: null,
      text: "",
      mainDiscussion: {},
      isSubscribed: false,
      followDiscussion: [{}],
      toDeleteContent: {},
      // 加载动画
      loading: true,
    };
  },
  created() {
    const title = `讨论`;
    this.loading = true;
    this.setAppTitle(title);
    this.setPageTitle(title);
    this.currentUserId = store.getters.getUserId;
    this.sendDataToBackend();
  },
  methods: {
    ...mapMutations(["setAppTitle", "setPageTitle"]),
    ...mapState(["userId"]),
    ...mapActions("snackbar", ["showSnackbar"]),
    async sendDataToBackend() {
      try {
        // 获取 user_id 和 dis_id
        const userId = this.$store.getters.getUserId; // 假设你使用 Vuex 获取 user_id
        const disId = this.$route.params.id; // 从路由获取 dis_id

        // 打包请求数据
        const requestData = {
          user_id: userId,
          dis_id: disId,
        };

        // 发送 POST 请求到后端 API，并指定请求头为 application/json
        const response = await axios.post(
          "http://127.0.0.1:8000/api/discussions/get_discussion/",
          requestData,
          {
            headers: {
              "Content-Type": "application/json", // 指定请求体的格式为 JSON
            },
          }
        );
        if (response.data.success) {
          console.log(response.data);
          this.mainDiscussion = response.data.discussion;
          this.followDiscussion = response.data.replies;
          this.isSubscribed = response.data.discussion.isSubscribed;
          this.isMarked = response.data.discussion.isMarked;
          const title = `讨论 - ${this.mainDiscussion.title}`;
          this.setAppTitle(title);
          this.setPageTitle(title);
          // 处理后端响应
          console.log("请求成功:", response.data);
          this.currentUserId = store.getters.getUserId;
          this.loading = false;
        } else {
          console.log("请求失败");
        }
      } catch (error) {
        // 请求失败时处理错误
        console.error("请求失败:", error);
      }
    },
    formatDate(dateString) {
      const options = {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false, // 使用24小时制
      };
      const date = new Date(dateString);
      return date.toLocaleString("zh-CN", options).replace(/\//g, "-");
    },
    returnForum() {
      this.$router.push(`/forum`);
    },
    async toggleSubscription() {
      this.isSubscribed = !this.isSubscribed;
      if (this.isSubscribed) {
        this.mainDiscussion.sub_count++;
      } else {
        this.mainDiscussion.sub_count--;
      }
      try {
        const userId = this.$store.getters.getUserId; // 假设你使用 Vuex 获取 user_id
        const disId = this.$route.params.id; // 使用传入的 discussionId 作为 dis_id

        const requestData = {
          user_id: userId,
          dis_id: disId,
        };
        let url = "http://127.0.0.1:8000/api/discussions/subscribe_discussion/";
        // 发送 POST 请求到后端 API，并指定请求头为 application/json
        const response = await axios.post(url, requestData, {
          headers: {
            "Content-Type": "application/json", // 指定请求体的格式为 JSON
          },
        });
        console.log("请求成功:", response.data);
      } catch (error) {
        console.error("请求失败:", error);
      }
    },
    async toggleLike(discussionId) {
      // 更新讨论的 isLiked 状态
      if (discussionId === "main") {
        this.mainDiscussion.isLiked = !this.mainDiscussion.isLiked;
        if (this.mainDiscussion.isLiked) {
          this.mainDiscussion.like_count++;
        } else {
          this.mainDiscussion.like_count--;
        }
      } else {
        // 检查是否是跟随讨论的ID
        const discussion = this.followDiscussion.find(
          (d) => d.id === discussionId
        );
        if (discussion) {
          discussion.isLiked = !discussion.isLiked;
          if (discussion.isLiked) {
            discussion.like_count++;
          } else {
            discussion.like_count--;
          }
        } else {
          // 如果ID未找到，抛出警告
          console.warn(`未找到对应的讨论或评论，ID: ${discussionId}`);
          return; // 退出方法，防止继续执行后面的请求
        }
      }

      try {
        // 获取 user_id 和 dis_id
        const userId = this.$store.getters.getUserId; // 假设你使用 Vuex 获取 user_id
        const disId = this.$route.params.id; // 使用传入的 discussionId 作为 dis_id

        // 打包请求数据
        const requestData = {
          user_id: userId,
          dis_id: discussionId == "main" ? disId : discussionId,
        };
        let url = "";
        // 根据discussionId决定URL
        if (discussionId === "main") {
          url = "http://127.0.0.1:8000/api/discussions/like_discussion/";
        } else {
          url = "http://127.0.0.1:8000/api/discussions/like_reply/";
        }
        // 发送 POST 请求到后端 API，并指定请求头为 application/json
        const response = await axios.post(url, requestData, {
          headers: {
            "Content-Type": "application/json", // 指定请求体的格式为 JSON
          },
        });

        // 处理后端响应
        console.log("请求成功:", response.data);
      } catch (error) {
        // 请求失败时处理错误
        console.error("请求失败:", error);
      }
    },
    editDiscussion(id, content, isMainDiscussion, isComment) {
      this.editDialog = true;
      this.text = content;
      this.emitId = id;
      this.isMainDiscussion = isMainDiscussion;
      this.isComment = isComment;
    },
    commentDiscussion(id, isMainDiscussion, isComment) {
      this.commentDialog = true;
      this.text = "";
      this.emitId = id;
      this.isMainDiscussion = isMainDiscussion;
      this.isComment = isComment;
    },
    confirmDelete(id, isMainDiscussion) {
      this.confirmDialog = true;
      const data = {
        content: isMainDiscussion ? "讨论贴" : "评论",
        id: id,
        isMainDiscussion: isMainDiscussion,
      };
      console.log(data);
      this.toDeleteContent = data;
    },
    async deleted(id, isMainDiscussion) {
      console.log(id);
      const requestData = {
        user_id: this.$store.getters.getUserId,
        discussion_id: !isMainDiscussion ? id : this.$route.params.id,
      };
      let url = "";
      // 根据 isComment 和 isMaindiscussion 决定 url 的值
      if (isMainDiscussion) {
        url = "http://127.0.0.1:8000/api/discussions/delete_discussion/";
      } else {
        url = "http://127.0.0.1:8000/api/discussions/delete_reply/";
      }
      try {
        const response = await axios.post(url, requestData, {
          headers: {
            "Content-Type": "application/json", // 指定请求体的格式为 JSON
            // 'Authorization': 'Bearer <token>'  // 如果需要身份验证 token
          },
        });
        console.log(response.status);
        // 处理响应
        if (response.status === 200) {
          if (isMainDiscussion) this.$router.push(`/forum`);
          else this.sendDataToBackend();
        }
      } catch (error) {
        console.error("发送通知时出错:", error);
      }
    },
    async emitEdit() {
      const requestData = {
        user_id: this.$store.getters.getUserId,
        discussion_id:
          !this.isComment || this.isMainDiscussion
            ? this.emitId
            : this.$route.params.id,
        content: this.text,
      };

      let url = "";
      let message = "";
      // 根据 isComment 和 isMaindiscussion 决定 url 的值
      if (this.isComment) {
        url = "http://127.0.0.1:8000/api/discussions/create_reply/";
        message = "回复发送";
      } else if (this.isMainDiscussion) {
        url = "http://127.0.0.1:8000/api/discussions/edit_discussion/";
        message = "修改讨论贴";
      } else {
        url = "http://127.0.0.1:8000/api/discussions/edit_reply/";
        message = "修改回复";
      }
      try {
        // 发送 POST 请求
        const response = await axios.post(url, requestData, {
          headers: {
            "Content-Type": "application/json", // 指定请求体的格式为 JSON
            // 'Authorization': 'Bearer <token>'  // 如果需要身份验证 token
          },
        });
        console.log(response.status);
        // 处理响应
        if (response.status === 200) {
          console.log(11);
          this.showSnackbar({
            message: message + "成功",
            color: "success",
            timeout: 2000,
          });
          console.log("df");

          this.sendDataToBackend();
        }
      } catch (error) {
        console.error("发送通知时出错:", error);
        this.showSnackbar({
          message: message + "时出错",
          color: "error",
          timeout: 2000,
        });
      }
      console.log(this.emitId);
      console.log(this.text);

      this.commentDialog = false;
      this.editDialog = false;
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

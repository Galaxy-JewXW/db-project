<template>
  <v-banner sticky icon="mdi-plus" lines="one">
    <template v-slot:text>
      <div class="text-subtitle-1">作为辅导师，你可发布新的公告。</div>
    </template>

    <template v-slot:actions>
      <v-btn color="primary" class="mr-5" @click="postNewNoti()">
        <div class="text-subtitle-1">发布新公告</div>
      </v-btn>
    </template>
  </v-banner>
  <v-container v-if="!loading" class="scroll-container">
    <v-row>
      <v-col v-for="notice in notices" :key="notice.id" cols="12">
        <v-card>
          <v-card-title>
            <div>
              <div class="notice-title">{{ notice.title }}</div>
              <div class="notice-subtitle">
                {{ notice.publisher }}&nbsp;&nbsp;{{
                  formatDate(notice.releaseTime)
                }}
              </div>
            </div>
          </v-card-title>
          <v-divider></v-divider>
          <div style="margin-left: -15px">
            <v-md-preview :text="notice.content"></v-md-preview>
          </div>
          <v-divider></v-divider>
          <v-row no-gutters>
            <v-col cols="auto">
              <v-btn
                rounded="0"
                variant="text"
                :color="'#1867c0'"
                @click="editNotice(notice)"
              >
                <v-icon left>mdi-pencil</v-icon>
                编辑此公告
              </v-btn>
            </v-col>
            <v-col cols="auto">
              <v-btn
                rounded="0"
                variant="text"
                color="#ee3f4d"
                @click="confirmDelete(notice)"
              >
                <v-icon left>mdi-close</v-icon>
                删除此公告
              </v-btn>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  <div v-else>
    <v-skeleton-loader
      class="mx-auto main-card"
      max-width="100%"
      type="list-item-avatar-three-line, list-item-avatar-three-line, list-item-avatar-three-line"
    ></v-skeleton-loader>
  </div>
  <v-dialog
    v-model="editDialogOpen"
    transition="dialog-bottom-transition"
    fullscreen
  >
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="editDialogOpen = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>编辑公告</v-toolbar-title>
      </v-toolbar>
      <div class="scroll-container">
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-row>
            <v-col>
              <v-text-field
                v-model="currentNotice.title"
                label="标题"
                :rules="[rules.required]"
                variant="outlined"
              />
            </v-col>
          </v-row>
        </v-form>

        <!-- 表单和编辑器之间的分割线 -->
        <v-divider></v-divider>

        <!-- Markdown 编辑器 -->
        <v-md-editor
          v-model="currentNotice.content"
          height="325px"
          left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | link image code"
          right-toolbar="preview toc sync-scroll"
        ></v-md-editor>

        <!-- 按钮行 -->
        <v-row class="btns">
          <v-btn color="primary" @click="confirmNotice">发布</v-btn>
          <v-btn variant="plain" @click="clearNotice">清除</v-btn>
        </v-row>
      </div>
    </v-card>
  </v-dialog>
  <v-dialog v-model="submitDialogOpen" max-width="400px">
    <v-card>
      <v-card-title>
        <v-icon color="primary">mdi-alert-circle-outline</v-icon>
        <span class="headline ml-2">确定提交你的更改吗？</span>
      </v-card-title>
      <v-card-actions>
        <v-btn color="primary" variant="text" @click="submitNotice">
          确定
        </v-btn>
        <v-btn variant="plain" @click="submitDialogOpen = false"> 取消 </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <v-dialog v-model="deleteDialogOpen" max-width="400px">
    <v-card>
      <v-card-title>
        <v-icon color="primary">mdi-alert-circle-outline</v-icon>
        <span class="headline ml-2">操作不可逆</span>
      </v-card-title>
      <v-card-text>
        确定删除题库“{{ this.toDeleteNotice.title }}”吗？
      </v-card-text>
      <v-card-actions>
        <v-btn color="red" variant="text" @click="deleteNotice"> 确定 </v-btn>
        <v-btn variant="plain" @click="deleteDialogOpen = false"> 取消 </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapMutations, mapActions } from "vuex";
import axios from "axios";
export default {
  name: "AdminBoard",
  data() {
    return {
      notices: [],
      rules: {
        required: (value) => !!value || "该字段为必填项",
      },
      valid: false,
      editDialogOpen: false,
      currentNotice: {
        id: null,
        title: "",
        publisher: "",
        releaseTime: "",
        content: "",
      },
      originalNotice: {},
      toDeleteNotice: null,
      submitDialogOpen: false,
      deleteDialogOpen: false,
      loading: true,
    };
  },
  created() {
    // 更新标题
    this.loading = true;
    const title = "主页";
    this.setAppTitle(title);
    this.setPageTitle(title);
    this.fetchData();
    // 按发布时间对 notices 进行排序，越新的排在最前面
  },
  methods: {
    ...mapMutations(["setAppTitle", "setPageTitle"]),
    ...mapActions("snackbar", ["showSnackbar"]),
    // 格式化日期
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
    editNotice(notice) {
      this.currentNotice = { ...notice };
      this.originalNotice = { ...notice };
      this.editDialogOpen = true;
    },
    postNewNoti() {
      this.$router.push("/admin/new-notification");
    },
    hasChanges() {
      return (
        this.currentNotice.title !== this.originalNotice.title ||
        this.currentNotice.content !== this.originalNotice.content
      );
    },
    confirmDelete(notice) {
      this.toDeleteNotice = notice;
      this.deleteDialogOpen = true;
    },
    async deleteNotice() {
      this.deleteDialogOpen = false;
      const requestData = {
        user_id: this.$store.getters.getUserId,
        broadcast_id: this.toDeleteNotice.id,
      };
      try {
        // 发送 POST 请求
        const response = await axios.post(
          "http://127.0.0.1:8000/api/broadcast/delete_broadcast/",
          requestData,
          {
            headers: {
              "Content-Type": "application/json", // 指定请求体的格式为 JSON
              // 'Authorization': 'Bearer <token>'  // 如果需要身份验证 token
            },
          }
        );

        // 处理响应
        if (response.status === 200) {
          console.log("df");
          // 假设后端返回了创建的通知信息
          this.fetchData();
        }
      } catch (error) {
        console.error("发送通知时出错:", error);
        this.showSnackbar({
          message: "删除公告时出错",
          color: "error",
          timeout: 2000,
        });
      }
      this.showSnackbar({
        message: `已删除公告 ${this.toDeleteNotice.id} "${this.toDeleteNotice.title}"`,
        color: "success",
        timeout: 2000,
      });
      this.toDeleteNotice = null;
    },
    confirmNotice() {
      if (!this.currentNotice.title || !this.currentNotice.content) {
        this.showSnackbar({
          message: "标题或内容不能为空",
          color: "error",
          timeout: 2000,
        });
        return;
      }
      if (this.hasChanges()) {
        this.submitDialogOpen = true;
      } else {
        this.showSnackbar({
          message: "修改公告成功",
          color: "success",
          timeout: 2000,
        });
        this.editDialogOpen = false;
        this.submitDialogOpen = false;
      }
    },
    async fetchData() {
      const requestData = {
        user_id: this.$store.getters.getUserId,
      };
      try {
        // 发送 POST 请求
        const response = await axios.post(
          "http://127.0.0.1:8000/api/broadcast/get_all_broadcasts/",
          requestData,
          {
            headers: {
              "Content-Type": "application/json", // 指定请求体的格式为 JSON
              // 'Authorization': 'Bearer <token>'  // 如果需要身份验证 token
            },
          }
        );
        this.notices = response.data.broadcasts;
        this.notices.sort(
          (a, b) => new Date(b.releaseTime) - new Date(a.releaseTime)
        );
        this.loading = false;
      } catch (error) {
        console.error("发送通知时出错:", error);
      }
    },
    async submitNotice() {
      // 执行提交逻辑
      console.log(this.currentNotice);
      const requestData = {
        user_id: this.$store.getters.getUserId,
        broadcast_id: this.currentNotice.id,
        new_title: this.currentNotice.title,
        publisher: this.currentNoticepublisher,
        content: this.currentNotice.content,
      };
      try {
        // 发送 POST 请求
        const response = await axios.post(
          "http://127.0.0.1:8000/api/broadcast/edit_broadcast/",
          requestData,
          {
            headers: {
              "Content-Type": "application/json", // 指定请求体的格式为 JSON
              // 'Authorization': 'Bearer <token>'  // 如果需要身份验证 token
            },
          }
        );

        // 处理响应
        if (response.status === 200) {
          console.log("df");
          // 假设后端返回了创建的通知信息
          this.fetchData();
        }
      } catch (error) {
        console.error("发送通知时出错:", error);
      }
      this.showSnackbar({
        message: "发布公告成功",
        color: "success",
        timeout: 2000,
      });
      this.editDialogOpen = false;
      this.submitDialogOpen = false;
    },

    // 清除公告内容
    clearNotice() {
      this.currentNotice.title = "";
      this.currentNotice.content = "";
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
  height: 90vh;
  max-height: 90vh;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scroll-container::-webkit-scrollbar {
  display: none;
}

/* 公告列表样式 */
.notice-title {
  font-size: 1.35rem;
  /* 增大字体 */
  margin-bottom: 4px;
}

.notice-subtitle {
  font-size: 1rem;
  /* 增大字体 */
  color: rgba(0, 0, 0, 0.6);
}

.notice-publisher {
  font-size: 1.1rem;
  /* 增大字体 */
}

.notice-time {
  font-size: 1rem;
  /* 保持时间字体大小不变 */
  color: rgba(0, 0, 0, 0.6);
}

.notice-item {
  padding: 4px 0;
}

.notice-item:hover {
  background-color: #f5f5f5;
  cursor: pointer;
}

.btns {
  margin-top: 16px;
  padding-left: 16px;
}
</style>

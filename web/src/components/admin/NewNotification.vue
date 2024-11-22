<template>
  <!-- 顶部的 Banner -->
  <v-banner sticky icon="mdi-plus" lines="one">
    <template v-slot:text>
      <div class="text-subtitle-1">作为辅导师，你可发布新的通知。</div>
    </template>

    <template v-slot:actions>
      <v-btn color="primary" class="mr-5" @click="confirmReturn">
        <div class="text-subtitle-1">返回</div>
      </v-btn>
    </template>
  </v-banner>

  <!-- 表单区域 -->
  <div class="scroll-container">
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-row>
        <v-col>
          <v-text-field v-model="title" label="标题" :rules="[rules.required]" variant="outlined" />
        </v-col>
      </v-row>
    </v-form>

    <!-- 表单和编辑器之间的分割线 -->
    <v-divider></v-divider>

    <!-- Markdown 编辑器 -->
    <v-md-editor v-model="text" height="325px" width="20%"
      left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | link image code"
      right-toolbar="preview toc sync-scroll"></v-md-editor>

    <!-- 按钮行 -->
    <v-row class="btns">
      <v-btn color="primary" @click="confirmSubmit">发布</v-btn>
      <v-btn variant="plain" @click="confirmClear">清除</v-btn>
    </v-row>
  </div>

  <!-- Snackbar -->
  <v-snackbar v-model="snackbarOpen" :timeout="snackbarTimeout" :color="snackbarColor" min-width="25%">
    <div style="font-size: 16px">{{ snackbarMessage }}</div>
    <template #actions>
      <v-btn icon @click="snackbarOpen = false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </template>
  </v-snackbar>

  <v-dialog v-model="returnDialogOpen" max-width="400px">
    <v-card>
      <v-card-title>
        <v-icon color="primary">mdi-alert-circle-outline</v-icon>
        <span class="headline ml-2">确定不保存修改直接返回吗？</span>
      </v-card-title>
      <v-card-actions>
        <v-btn color="primary" variant="text" @click="returnForum">
          确定
        </v-btn>
        <v-btn variant="plain" @click="returnDialogOpen = false">
          取消
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- Confirm Dialogs -->
  <!-- 确认发布的对话框 -->
  <v-dialog v-model="confirmDialogOpen" max-width="400px">
    <v-card>
      <v-card-title>
        <v-icon color="primary">mdi-alert-circle-outline</v-icon>
        <span class="headline ml-2">确定发布吗？</span>
      </v-card-title>
      <v-card-actions>
        <v-btn color="primary" variant="text" @click="submitPost">
          确定
        </v-btn>
        <v-btn variant="plain" @click="confirmDialogOpen = false">
          取消
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- 确认清除的对话框 -->
  <v-dialog v-model="clearDialogOpen" max-width="400px">
    <v-card>
      <v-card-title>
        <v-icon color="primary">mdi-alert-circle-outline</v-icon>
        <span class="headline ml-2">确定不保存你的更改吗？</span>
      </v-card-title>
      <v-card-actions>
        <v-btn color="primary" variant="text" @click="clearForm">
          确定
        </v-btn>
        <v-btn variant="plain" @click="clearDialogOpen = false">
          取消
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapMutations } from "vuex"; // 引入 mapMutations

export default {
  name: "NewNotification",
  data() {
    return {
      title: "",
      text: "",
      valid: false,
      rules: {
        required: (value) => !!value || "该字段为必填项",
      },
      snackbarOpen: false,
      snackbarMessage: "",
      snackbarColor: "error",
      snackbarTimeout: 1000,
      // Dialog 控制
      confirmDialogOpen: false,  // 确认发布的对话框
      clearDialogOpen: false,    // 确认清除的对话框
      returnDialogOpen: false,
    };
  },
  mounted() {
    const title = "发布新通知";
    this.setAppTitle(title);
    this.setPageTitle(title);
  },
  methods: {
    ...mapMutations(["setAppTitle", "setPageTitle"]), // 映射 Vuex 的 mutations

    // 返回确认弹窗
    confirmReturn() {
      if (this.title || this.text) {
        this.returnDialogOpen = true;  // 如果有内容，显示清除确认弹窗
      } else {
        this.$router.push(`/admin/home`);
      }
    },

    // 发布确认弹窗
    confirmSubmit() {
      if (this.$refs.form.validate() && this.text.length !== 0) {
        // 如果表单没有错误，弹出确认发布对话框
        this.confirmDialogOpen = true;  // 显示确认发布的对话框
      } else {
        // 如果表单有错误，显示错误提示 Snackbar
        this.snackbarMessage = "标题和内容为必填项";
        this.snackbarColor = "error";
        this.snackbarOpen = true;
      }
    },

    // 发布功能
    async submitPost() {
      console.log("标题:", this.title);
      console.log("内容:", this.text);

      // 显示成功的 Snackbar
      this.snackbarMessage = "提交成功";
      this.snackbarColor = "success";
      this.snackbarOpen = true;

      this.returnForum();
      this.confirmDialogOpen = false; // 关闭确认发布的对话框
    },

    // 清除确认弹窗
    confirmClear() {
      if (this.title || this.text) {
        this.clearDialogOpen = true;  // 如果有内容，显示清除确认弹窗
      } else {
        this.clearForm();
      }
    },

    // 清除表单内容
    clearForm() {
      this.title = "";
      this.text = "";
      this.$refs.form.reset();
      this.clearDialogOpen = false;  // 关闭清除确认弹窗
    },

    // 返回首页
    returnForum() {
      this.$router.push(`/admin/home`);
    },
  },
};
</script>

<style scoped>
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

.v-icon {
  color: white;
}

.scroll-container {
  flex: 1 1 auto;
  overflow-y: auto;
  padding-top: 20px;
  height: 98vh;
  max-height: 98vh;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scroll-container::-webkit-scrollbar {
  display: none;
}

.btns {
  margin-top: 16px;
  padding-left: 16px;
}
</style>

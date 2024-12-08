<template>
  <v-alert color="#1867c0" icon="mdi-comment-multiple-outline" title="欢迎你畅所欲言！" text="在讨论区发布贴文，表示你已阅读并同意我们的讨论区规范。">
  </v-alert>

  <div class="scroll-container">
    <!-- 表单区域 -->
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-row>
        <!-- 标题输入框 -->
        <v-col cols="12" md="6">
          <v-text-field v-model="title" label="标题" :rules="[rules.required]" variant="outlined" />
        </v-col>

        <!-- 所属科目下拉选择 -->
        <v-col cols="12" md="6">
          <v-autocomplete v-model="subject" :items="subjects" label="所属科目" :rules="[rules.required]" variant="outlined"
            clearable />
        </v-col>
      </v-row>
    </v-form>

    <!-- 返回按钮 -->
    <v-btn class="floating-btn" fab color="primary" @click="returnForum()">
      <v-icon size="32">mdi-arrow-collapse-left</v-icon>
    </v-btn>

    <!-- 表单和编辑器之间的分割线 -->
    <v-divider></v-divider>

    <!-- Markdown 编辑器 -->
    <v-md-editor v-model="text" height="325px" width="20%"
      left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | link image code"
      right-toolbar="preview toc sync-scroll"></v-md-editor>

    <!-- 按钮行 -->
    <v-row class="btns">
      <v-btn color="primary" @click="submitPost">发布</v-btn>
      <v-btn variant="plain" @click="clearForm">清除</v-btn>
    </v-row>
  </div>
</template>

<script>
import { mapMutations } from "vuex"; // 引入 mapMutations
import store from "@/store";
import axios from 'axios';

export default {
  name: "DiscussionsContent",
  data() {
    return {
      title: "",
      text: "",
      subject: null,
      subjects: [
        "工科数学分析（上）",
        "工科数学分析（下）",
        "工科高等代数",
        "离散数学（信息类）",
        "基础物理学A",
      ],
      valid: false,
      rules: {
        required: (value) => !!value || "该字段为必填项",
      },
    };
  },
  mounted() {
    const title = "发布新讨论贴";
    this.setAppTitle(title);
    this.setPageTitle(title);
  },
  computed: {
    requestData() {
      return {
        user_id: store.getters.getUserId || "",
        title: this.title || "",
        content: this.text || "",
        tag: this.subject || "",
      };
    },
  },
  methods: {
    ...mapMutations(["setAppTitle", "setPageTitle"]), // 映射 Vuex 的 mutations

    returnForum() {
      this.$router.push(`/forum`);
    },

    // 发布功能
    async submitPost() {
      const valid = await this.$refs.form.validate();
      if (valid.valid) {
        console.log("nmd");
        try {
          // 发起 POST 请求
          console.log(this.requestData);
          const response = await axios.post('http://127.0.0.1:8000/api/discussions/create_discussion/', this.requestData, {
            headers: {
              'Content-Type': 'application/json', // 指定JSON格式
            }
          });
          this.showSnackbar({
            message: '发布成功',
            color: 'success',
            timeout: 2000
          });
        } catch (error) {
          if (error.response && error.response.status === 400) {
            this.$toast.error('标题和内容不能为空！');
          } else if (error.response && error.response.status === 404) {
            this.$toast.error('用户不存在！');
          } else {
            this.$toast.error('创建讨论失败，请稍后重试。');
          }
          console.error('提交失败:', error);
        }
        this.returnForum();
      } else {
        console.log("nmd1");
        // 如果表单验证失败，获取验证失败的字段错误信息
        let errorMessage = "";

        // 根据验证失败的字段给出具体的错误信息
        if (!this.title) {
          errorMessage += "标题为必填项";
        } else if (!this.subject) {
          errorMessage += "所属科目为必填项";
        } else if (this.text.length === 0) {
          errorMessage += "内容不能为空";
        }

        this.showSnackbar({
          message: errorMessage,
          color: 'error',
          timeout: 2000
        });
      }
    },

    // 清除表单内容
    clearForm() {
      this.title = "";
      this.text = "";
      this.subject = null;
      this.$refs.form.reset();
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

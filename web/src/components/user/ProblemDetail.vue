<template>
  <v-container fluid>
    <v-row justify="start">
      <!-- 左侧内容区域，占 8 列（约 70%） -->
      <v-col cols="12" md="8">
        <div class="markdown-container">
          <v-md-preview :text="problem.content" class="markdown-content" v-if="problem"></v-md-preview>
        </div>
      </v-col>

      <!-- 右侧卡片区域，占 4 列（约 30%） -->
      <v-col cols="12" md="4">
        <v-card class="info-card" outlined>
          <v-card-text class="card-text">
            <div class="problem-header" v-if="problem">
              <h1>题目 - {{ problem.id }}</h1>
              <v-chip class="ma-2 chip-item" color="primary" variant="outlined">
                {{ problem.type }}
              </v-chip>
            </div>

            <!-- 添加题目相关信息 -->
            <div class="info-item">
              <v-icon>mdi-school</v-icon>
              <span class="info-title">学科：</span>
              <span>{{ problem.subject }}</span>
            </div>
            <div class="info-item">
              <v-icon>mdi-calendar</v-icon>
              <span class="info-title">添加时间：</span>
              <span>{{ problem.addedAt }}</span>
            </div>
            <div class="info-item">
              <v-icon>mdi-source-branch</v-icon>
              <span class="info-title">来源：</span>
              <span>{{ problem.source }}</span>
            </div>
            <div class="info-item">
              <v-icon>mdi-tag</v-icon>
              <span class="info-title">标签：</span>
              <span>{{ problem.tags }}</span>
            </div>
            <div class="info-item">
              <v-icon>mdi-star-outline</v-icon>
              <span class="info-title">难度：</span>
              <span>{{ problem.difficulty }}</span>
            </div>

            <!-- 按钮区域，放置在同一行 -->
            <v-row class="ma-2">
              <v-btn prepend-icon="mdi-lightbulb" color="primary" @click="viewAnswer" block>
                查看答案
              </v-btn>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 答案对话框 -->
    <v-dialog v-model="dialog" transition="dialog-bottom-transition" fullscreen>
      <v-card>
        <v-toolbar dark color="primary">
          <v-btn icon @click="closeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>答案</v-toolbar-title>
        </v-toolbar>

        <!-- 根据用户选择显示内容 -->
        <div v-if="!answerResult">
          <!-- 做对了、做错了按钮 -->
          <v-card flat elevation="0" class="ma-4" style="max-width: 100%;">
            <v-card-title class="headline text-h5 font-weight-bold">你做对了吗？</v-card-title>
            <v-card-text class="d-flex justify-start">
              <v-btn color="success" class="ma-2" outlined @click="handleAnswer(true)">
                <v-icon left>mdi-check</v-icon> 做对了
              </v-btn>
              <v-btn color="error" class="ma-2" outlined @click="handleAnswer(false)">
                <v-icon left>mdi-close</v-icon> 做错了
              </v-btn>
            </v-card-text>
          </v-card>
        </div>
        <div v-else>
          <!-- 显示对应的提示信息 -->
          <v-alert :type="answerResult === 'correct' ? 'success' : 'error'" class="ma-4" title="回答情况已记录"
            style="max-width: 100%;">
            {{ alertMessage }}
          </v-alert>
        </div>

        <!-- Markdown 内容显示区域 -->
        <v-card-text>
          <div class="markdown-content" style="margin-left: -20px;" v-if="answer">
            <v-md-preview :text="answer" />
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { mapMutations } from "vuex";
import axios from "axios";
export default {
  name: "ProblemDetail",
  data() {
    return {
      problem: {}, // 存储题目信息
      dialog: false, // 控制答案弹框显示与隐藏
      answer: null, // 存储答案内容
      answerResult: null, // 存储用户的答案结果
      alertMessage: "", // 存储提示信息
    };
  },
  mounted() {
    const problemId = this.$route.params.id;
    this.fetchProblemData(problemId);
  },
  methods: {
    ...mapMutations(["setAppTitle", "setPageTitle"]),

    // 获取题目信息
    async fetchProblemData(problemId) {
      this.loading = true;
      this.error = null;

      try {
        // 使用 axios 发起 POST 请求
        const response = await axios.post("http://127.0.0.1:8000/api/questions/get_question_by_id/", {
          user_id: this.$store.getters.getUserId,
          question_id: problemId,
        });

        // 检查后端返回的数据
        if (response.data && response.data.success) {
          const mockProblemData = response.data.question;
          // console.log(mockProblemData.id);
          // console.log(mockProblemData.type);
          // console.log(mockProblemData.content);
          // console.log(mockProblemData.subject)
          // 更新组件的数据
          this.problem = {
            id: mockProblemData.id,
            type: mockProblemData.type,
            content: mockProblemData.content,
            subject: mockProblemData.subject,
            addedAt: mockProblemData.addedAt,
            source: mockProblemData.source,
            tags: mockProblemData.tags.join(","),
            difficulty: mockProblemData.difficulty,
            addedAt: mockProblemData.added_at,
          };
          this.answer = mockProblemData.answer;
          // 使用 Vuex 更新 appTitle 和 pageTitle
          const title = `题目详情 - ${problemId}`;
          this.setAppTitle(title);
          this.setPageTitle(title);
        } else {
          throw new Error("获取题目数据失败");
        }
      } catch (error) {
        console.error("获取题目数据失败：", error);
        this.error = "获取题目数据失败";
      } finally {
        this.loading = false;
      }
    },

    // 查看答案
    async viewAnswer() {
      this.dialog = true;
    },

    // 处理用户点击“做对了”或“做错了”
    handleAnswer(isCorrect) {
      if (isCorrect) {
        this.answerResult = 'correct';
        this.alertMessage = '恭喜你，回答正确！';
      } else {
        this.answerResult = 'incorrect';
        this.alertMessage = '别灰心，下次再接再厉！';
      }
    },

    // 关闭对话框并重置状态
    closeDialog() {
      this.dialog = false;
      this.answerResult = null;
    },
  },
};
</script>

<style scoped>
h1 {
  margin-bottom: 8px;
  text-align: left;
}

.problem-header {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: flex-start;
}

.chip-item {
  display: flex;
  align-items: center;
  margin: 0;
}

.markdown-container {
  max-height: calc(100vh - 150px);
  overflow-y: auto;
  margin-left: -29px;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.markdown-container::-webkit-scrollbar {
  display: none;
}

.markdown-content {
  margin-top: 16px;
  text-align: left;
  overflow-wrap: break-word;
  word-wrap: break-word;
}

.info-card {
  height: 50vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.card-text {
  padding-left: 16px;
  padding-top: 16px;
  text-align: left;
  overflow: hidden;
}

.info-card .v-btn {
  margin-top: 8px;
}

.info-item {
  display: flex;
  align-items: center;
  margin-top: 8px;
  gap: 8px;
  font-size: 16px;
  text-align: left;
}

.info-title {
  font-weight: bold;
}

.v-dialog {
  z-index: 200;
}

/* 隐藏 v-card 的边框 */
.v-card {
  border: none;
}
</style>

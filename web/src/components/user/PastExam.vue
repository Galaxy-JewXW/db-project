<template>
  <div class="problem-set-detail" v-if="examData">
    <v-alert type="success">
      <v-alert-title> 本次测试成绩已公布。 </v-alert-title>
      你做对了{{ this.totalQuestions }}题中的{{ finishedQuestions.length }}题。
    </v-alert>
    <!-- 题库名称 -->
    <h1 style="padding-top: 10px">{{ examData.name }}</h1>

    <!-- 信息芯片 -->
    <div class="chips-row" style="padding-bottom: 5px; margin-bottom: 5px">
      <v-chip v-for="(chip, index) in chips" :key="index" :color="chip.color" class="ma-1 chip-item">
        <v-icon left class="chip-icon">{{ chip.icon }}</v-icon>
        {{ chip.label }}: {{ chip.value }}
      </v-chip>
    </div>

    <!-- 可滚动的题目列表区域 -->
    <div class="questions-container">
      <v-expansion-panels>
        <v-expansion-panel v-for="(group, index) in questions" :key="index">
          <v-expansion-panel-title>
            <template v-slot:default="{ expanded }">
              <v-row no-gutters>
                <v-col class="d-flex justify-start text-bold" cols="4">
                  {{ group.type }}
                </v-col>
                <v-col class="text-grey" cols="8">
                  <v-fade-transition leave-absolute>
                    <span>
                      本部分共 {{ group.ids.length }} 题， 你已做对
                      {{
                        finishedQuestions.filter((qid) =>
                          group.ids.includes(qid)
                        ).length
                      }}
                      题
                    </span>
                  </v-fade-transition>
                </v-col>
              </v-row>
            </template>
          </v-expansion-panel-title>

          <!-- 题目按钮及分页控件 -->
          <v-expansion-panel-text>
            <v-row no-gutters>
              <div class="question-squares">
                <v-btn v-for="questionId in getPaginatedIds(group)" :key="questionId" :class="[
                  'question-square',
                  { finished: finishedQuestions.includes(questionId) },
                ]" :color="finishedQuestions.includes(questionId)
                  ? 'green'
                  : 'blue-darken-4'
                  " rounded="0" @click="goToQuestionDetail(questionId)">
                  <v-responsive class="text-truncate">{{
                    questionId
                  }}</v-responsive>
                </v-btn>
              </div>
            </v-row>
            <!-- 分页控件 -->
            <v-row justify="center" class="mt-2">
              <v-pagination v-model="group.currentPage" :total-visible="7"
                :length="Math.ceil(group.ids.length / pageSize)"
                @input="handlePageChange(group, $event)"></v-pagination>
            </v-row>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </div>

    <v-dialog v-model="dialog" transition="dialog-bottom-transition" fullscreen>
      <v-card class="fullscreen-card">
        <v-toolbar dark color="primary">
          <v-btn icon @click="closeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>
            {{ questionType }}：题目 - {{ currentQuestionId }}
          </v-toolbar-title>
        </v-toolbar>

        <v-card-text>
          <v-row>
            <v-col cols="8">
              <div v-if="question" class="markdown-content">
                <v-md-preview :text="question" />
              </div>
              <!-- 加载或错误状态 -->
              <v-alert v-else type="info" class="ma-4">正在加载...</v-alert>
            </v-col>

            <v-col cols="4">
              <v-card class="pa-4" outlined>
                <v-card-title style="padding-left: 0" class="text-h5 font-weight-regular">
                  标准答案
                </v-card-title>
                <v-card-text>
                  <div style="margin-left: -45px">
                    <v-md-preview :text="stdanswer"></v-md-preview>
                  </div>
                </v-card-text>
              </v-card>
              <v-card class="pa-4" outlined>
                <v-card-title style="padding-left: 0" class="text-h5 font-weight-regular">
                  你的提交
                </v-card-title>
                <v-card-text>
                  <div style="margin-left: -45px">
                    <v-md-preview :text="answer"></v-md-preview>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapMutations, mapActions } from "vuex";
import axios from "axios";

export default {
  name: "ProblemSetDetail",
  data() {
    return {
      examData: null,
      questions: [],
      loading: false,
      error: null,
      dialog: false, // 控制dialog显示
      question: "", // 存储题面的Markdown文本
      stdanswer: "",
      answer: "", // 存储答案显示
      loadingQuestion: false, // 控制加载状态
      finishedQuestions: [], // 做对的题目
      text: "",
      pageSize: 10, // 每页显示的题目数量
      questionType: "", // 当前题目的类型
      currentQuestionId: null, // 当前题目ID
    };
  },
  computed: {
    totalQuestions() {
      return (
        this.questions?.reduce((total, group) => {
          return total + group.ids.length;
        }, 0) || 0
      );
    },
    chips() {
      return [
        {
          color: "primary",
          icon: "mdi-book-open",
          label: "所属科目",
          value: this.examData?.subject || "N/A",
        },
        {
          color: "secondary",
          icon: "mdi-clock-outline",
          label: "时长",
          value: `${this.examData?.duration || 0} 分钟`,
        },
        {
          color: "success",
          icon: "mdi-calendar",
          label: "测试开始时间",
          value: this.formatDate2S(this.examData?.starttime),
        },
        {
          color: "warning",
          icon: "mdi-format-list-numbered",
          label: "题目数量",
          value: `${this.totalQuestions} 题`,
        },
      ];
    },
  },
  mounted() {
    const id = this.$route.params.id;
    this.fetchExamResult(id);
  },
  methods: {
    ...mapMutations(["setAppTitle", "setPageTitle", "setProblemType"]),
    ...mapActions("snackbar", ["showSnackbar"]),
    async fetchExamResult(examId) {
      console.log(`Fetching problem set data for ID: ${examId}`);
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/exams/view_exam_questions_result/', {
          user_id: this.$store.getters.getUserId,
          exam_id: this.$route.params.id,
        });
        const data = response.data;
        this.examData = {
          id: data.exam_id,
          name: data.name,
          subject: data.subject,
          starttime: data.starttime,
          duration: data.duration,
        };
        const title = "模拟测试成绩详情 - " + this.examData.name;
        this.finishedQuestions = data.finished;
        this.setAppTitle(title);
        this.setPageTitle(title);
        this.fetchQuestionsById(examId); // 获取题目列表
        this.loading = false;
      } catch (e) {
        console.error("获取模拟测试数据失败", e);
        this.error = "获取模拟测试数据失败";
        this.loading = false;
      }
    },

    async fetchQuestionsById(examId) {
      console.log(`Fetching questions for problem set ID: ${examId}`);
      this.loading = true;
      this.error = null;
      try {
        // 模拟从后端获取数据
        const response = await axios.post('http://127.0.0.1:8000/api/exams/get_exam_questions/', {
          user_id: this.$store.getters.getUserId,
          exam_id: this.$route.params.id,
        });
        const questions = response.data.qsdata;
        this.questions = questions; // 更新组件本地的题目列表数据
        this.loading = false;
      } catch (e) {
        console.error("获取题目数据失败", e);
        this.error = "获取题目数据失败";
        this.loading = false;
      }
    },

    formatDate(dateStr) {
      if (!dateStr) return "N/A";
      const options = { year: "numeric", month: "2-digit", day: "2-digit" };
      return new Date(dateStr).toLocaleDateString(undefined, options);
    },

    formatDate2S(dateString) {
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

    formatDuration(ms) {
      const totalSeconds = Math.floor(ms / 1000);
      const hours = Math.floor(totalSeconds / 3600);
      const minutes = Math.floor((totalSeconds % 3600) / 60);
      const seconds = totalSeconds % 60;
      return `${hours}:${minutes.toString().padStart(2, "0")}:${seconds
        .toString()
        .padStart(2, "0")}`;
    },

    getQuestionTypeById(id) {
      for (const group of this.questions) {
        if (group.ids.includes(id)) {
          return group.type;
        }
      }
      return null;
    },

    async goToQuestionDetail(questionId) {
      this.questionType = this.getQuestionTypeById(questionId);
      console.log(
        `Fetching question for question ID: ${questionId} ${this.questionType}`
      );
      this.loadingQuestion = true;
      this.currentQuestionId = questionId;
      // 模拟从后端获取Markdown文本数据
      const response = await axios.post('http://127.0.0.1:8000/api/exams/view_question_result/', {
          user_id: this.$store.getters.getUserId,
          exam_id: this.$route.params.id,
          question_id: questionId,

        });
      const data = response.data;
      this.question = data.question_data.content;
      this.stdanswer = data.question_data.answer;
      this.answer = data.answer_now;
      this.loadingQuestion = false;
      this.dialog = true; // 打开Dialog
    },

    closeDialog() {
      this.dialog = false; // 关闭Dialog
      this.question = ""; // 清空题面
    },

    // 获取当前页的题目ID
    getPaginatedIds(group) {
      const start = (group.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return group.ids.slice(start, end);
    },

    // 处理分页变化
    handlePageChange(group, newPage) {
      group.currentPage = newPage;
    },
  },
};
</script>

<style scoped>
.problem-set-detail {
  padding: 16px;
}

.chips-row {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 16px;
  align-items: center;
}

.chip-item {
  display: flex;
  align-items: center;
  margin-right: 8px;
}

.chip-item:last-child {
  margin-right: 0;
}

.chip-icon {
  margin-right: 4px;
}

.questions-container {
  max-height: calc(100vh - 300px);
  overflow-y: auto;
  padding: 16px 16px 32px;
  display: flex;
  flex-direction: column;
  scrollbar-width: none;
}

.questions-container::-webkit-scrollbar {
  display: none;
}

.question-squares {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 16px;
}

.question-square {
  width: 70px;
  height: 70px;
  font-size: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  border-radius: 0;
  overflow-wrap: break-word;
  word-wrap: break-word;
  cursor: pointer;
}

.question-square:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.v-responsive {
  max-width: 100%;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  font-size: 14px;
}

.v-expansion-panel {
  margin-bottom: 0px;
}

.markdown-content {
  padding: 16px;
  font-size: 16px;
}

.v-card {
  margin-top: 16px;
}

.v-card-title {
  font-size: 18px;
  font-weight: bold;
}

.v-card-text {
  font-size: 14px;
}

.fullscreen-card {
  width: 100vw;
  height: 100vh;
  max-width: 100vw;
  max-height: 100vh;
  margin: 0;
}
</style>

<template>
  <v-container v-if="loading">
    <v-skeleton-loader class="mx-auto main-card" max-width="100%"
      type="list-item-avatar-three-line, list-item-avatar-three-line, list-item-avatar-three-line"></v-skeleton-loader>
  </v-container>
  <div v-else>
    <div class="problem-set-detail" v-if="problemSetData">
      <v-scroll-y-transition mode="out-in">
        <!-- 测试进行中且未完成所有题目 -->
        <div v-if="remainingTime > 0 && finishedQuestions.length < totalQuestions" style="padding-bottom: 15px">
          <v-alert type="info" icon="mdi-clock-outline">
            <v-alert-title>
              测试进行中，剩余时间：{{ formatDuration(remainingTime) }}
            </v-alert-title>
            你已完成{{ totalQuestions }}题中的{{ finishedQuestions.length }}题。
          </v-alert>
        </div>

        <!-- 测试进行中且已完成所有题目 -->
        <div v-else-if="remainingTime > 0 && finishedQuestions.length === totalQuestions" style="padding-bottom: 15px">
          <v-alert type="success">
            <v-alert-title>
              测试进行中，剩余时间：{{ formatDuration(remainingTime) }}
            </v-alert-title>
            你已完成本次测试的所有题目。
          </v-alert>
        </div>

        <!-- 测试已结束 -->
        <div v-else-if="remainingTime === 0" style="padding-bottom: 15px">
          <v-alert type="error">
            <v-alert-title>测试已结束</v-alert-title>
            公布成绩前，你无法再次查看测试题。
          </v-alert>
        </div>
      </v-scroll-y-transition>

      <!-- 进度条 -->
      <v-progress-linear v-if="remainingTime > 0" :model-value="progressPercentage" color="primary" height="9" rounded
        style="margin-bottom: 10px"></v-progress-linear>

      <!-- 题库名称 -->
      <h1 style="padding-top: 10px">{{ problemSetData.name }}</h1>

      <!-- 信息芯片 -->
      <div class="chips-row" style="padding-bottom: 5px; margin-bottom: 5px">
        <v-chip v-for="(chip, index) in chips" :key="index" :color="chip.color" class="ma-1 chip-item">
          <v-icon left class="chip-icon">{{ chip.icon }}</v-icon>
          {{ chip.label }}: {{ chip.value }}
        </v-chip>
      </div>

      <!-- 可滚动的题目列表区域 -->
      <div v-if="remainingTime > 0" class="questions-container">
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
                        本部分共 {{ group.ids.length }} 题， 你已完成
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
                    <v-responsive class="text-truncate">{{ questionId }}</v-responsive>
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

      <!-- 测试已结束时的提示 -->
      <div v-else>本次测试已结束，你无法再查看题目。</div>

      <!-- 全屏对话框用于显示和回答题目 -->
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
                <div class="markdown-content">
                  <v-md-preview :text="question" />
                </div>
              </v-col>
              <v-col cols="4">
                <v-card class="pa-4" outlined>
                  <v-card-title style="padding-left: 0" class="text-h5 font-weight-regular">
                    提交题目 - {{ currentQuestionId }}
                  </v-card-title>
                  <div class="pb-2">
                    <v-chip color="primary" variant="outlined">
                      {{ questionType }}
                    </v-chip>
                  </div>
                  <v-divider></v-divider>
                  <div class="pt-2" v-if="choices === -1">
                    <v-btn v-if="lastAnswer.length" :href="lastAnswer" target="_blank" class="text-subtitle-1"
                      color="primary" variant="outlined" prepend-icon="mdi-file-download-outline">
                      查看上一次提交
                    </v-btn>
                    <!-- 文件上传 -->
                    <v-file-input v-model="files" label="提交答案" variant="underlined" counter show-size chips
                      accept=".jpg,.png,.jpeg">
                    </v-file-input>
                    <v-btn color="primary" variant="text" @click="uploading = !uploading; uploadFiles()"
                      :disabled="!files" :loading="uploading">
                      上传答案
                    </v-btn>
                  </div>
                  <div class="pt-2" v-else-if="
                    choices >= 3 && questionType === '单项选择题'
                  ">
                    最近一次的提交：{{ this.lastAnswer }}
                    <!-- 单项选择题 -->
                    <v-row no-gutters>
                      <v-radio-group v-model="selectedOption" inline>
                        <v-radio v-for="index in choices" :key="index" :label="getOptionLetter(index)"
                          :value="getOptionLetter(index)" dense />
                      </v-radio-group>
                    </v-row>

                    <v-row no-gutters>
                      <v-card-actions>
                        <v-btn color="primary" text="提交" variant="text" :disabled="!selectedOption"
                          @click="submitAnswer"></v-btn>
                        <v-btn text="清除" variant="plain" @click="clearSelection"></v-btn>
                      </v-card-actions>
                    </v-row>
                  </div>
                  <div class="pt-2" v-else-if="
                    choices >= 3 && questionType === '多项选择题'
                  ">
                    最近一次的提交：{{ this.lastAnswer }}
                    <!-- 多项选择题 -->
                    <v-row no-gutters>
                      <v-container>
                        <v-checkbox v-for="index in choices" v-model="selectedOptions" :key="index"
                          :label="getOptionLetter(index)" :value="getOptionLetter(index)"
                          style="margin-bottom: -30px" />
                      </v-container>
                    </v-row>

                    <v-row no-gutters>
                      <v-card-actions>
                        <v-btn color="primary" text="提交" variant="text" :disabled="selectedOptions.length === 0"
                          @click="submitAnswer"></v-btn>
                        <v-btn text="清除" variant="plain" @click="clearSelection"></v-btn>
                      </v-card-actions>
                    </v-row>
                  </div>
                  <div class="pt-2" v-else-if="questionType === '判断题'">
                    <!-- 判断题 -->
                    <div v-if="this.lastAnswer">最近一次的提交：{{ this.lastAnswer === "True" ? "正确" : "错误" }}</div>
                    <v-row no-gutters>
                      <v-radio-group v-model="selectedOption" inline>
                        <v-radio label="正确" value="True" dense />
                        <v-radio label="错误" value="False" dense />
                      </v-radio-group>
                    </v-row>
                    <v-row no-gutters>
                      <v-card-actions>
                        <v-btn color="primary" text="提交" variant="text" :disabled="!selectedOption"
                          @click="submitAnswer">
                          提交
                        </v-btn>
                        <v-btn text="清除" variant="plain" @click="clearSelection">
                          清除
                        </v-btn>
                      </v-card-actions>
                    </v-row>
                  </div>
                  <div class="pt-2" v-else-if="questionType === '填空题'">
                    <!-- 填空题 -->
                    <v-card-text style="padding-left: 0" class="text-subtitle-3 font-weight-regular">
                      使用markdown在左侧输入框输入答案，右侧为预览。
                      <br />
                      <a href="https://freeopen.github.io/mathjax/">在markdown中写数学公式</a>
                    </v-card-text>

                    <v-md-editor v-model="text" height="200px" left-toolbar="" right-toolbar=""></v-md-editor>
                    <v-row no-gutters>
                      <v-card-actions>
                        <v-btn color="primary" text="提交" variant="text" :disabled="!text" @click="submitAnswer">
                          提交
                        </v-btn>
                        <v-btn text="清除" variant="plain" @click="clearSelection">
                          清除
                        </v-btn>
                      </v-card-actions>
                    </v-row>
                  </div>
                  <div class="pt-2" v-else>暂无提交方式。请联系负责人。</div>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script>
import { mapMutations, mapActions } from "vuex";
import axios from "axios";
export default {
  name: "ProblemSetDetail",
  data() {
    return {
      problemSetData: null,
      questions: [],
      loading: true,
      error: null,
      currentTime: new Date(), // 当前时间
      intervalId: null, // 定时器ID
      dialog: false, // 控制dialog显示
      question: "", // 存储题面的Markdown文本
      finishedQuestions: [], // 完成的题目
      files: null, // File对象
      choices: -2,
      selectedOption: null, // 单项选择题
      selectedOptions: [], // 多项选择题
      text: "",
      pageSize: 10, // 每页显示的题目数量
      questionType: "", // 当前题目的类型
      currentQuestionId: null, // 当前题目ID
      lastAnswer: "",
      uploading: false,
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
          value: this.problemSetData?.subject || "N/A",
        },
        {
          color: "secondary",
          icon: "mdi-clock-outline",
          label: "时长",
          value: `${this.problemSetData?.duration || 0} 分钟`,
        },
        {
          color: "success",
          icon: "mdi-calendar",
          label: "测试开始时间",
          value: this.formatDate2S(this.problemSetData?.starttime),
        },
        {
          color: "warning",
          icon: "mdi-format-list-numbered",
          label: "题目数量",
          value: `${this.totalQuestions} 题`,
        },
      ];
    },
    remainingTime() {
      if (!this.problemSetData) return 0;
      const startTime = new Date(this.problemSetData.starttime);
      const durationMinutes = this.problemSetData.duration || 0; // duration in minutes
      const endTime = new Date(startTime.getTime() + durationMinutes * 60000); // convert to milliseconds
      const timeRemaining = endTime - this.currentTime; // in milliseconds

      return Math.max(timeRemaining, 0); // return 0 if timeRemaining is negative
    },
    progressPercentage() {
      if (!this.problemSetData) return 0;
      const startTime = new Date(this.problemSetData.starttime);
      const durationMinutes = this.problemSetData.duration || 0; // duration in minutes
      const endTime = new Date(startTime.getTime() + durationMinutes * 60000); // convert to milliseconds
      const totalDuration = endTime - startTime;

      const elapsedTime = this.currentTime - startTime;

      // Calculate the progress as a percentage
      return Math.min((elapsedTime / totalDuration) * 100, 100); // Prevent it from going over 100%
    },
    // 根据筛选条件过滤后的题目（移除筛选逻辑）
    filteredExercises() {
      return this.questions;
    },
  },
  mounted() {
    const id = this.$route.params.id;
    this.fetchProblemSetData(id);
    // 开始一个定时器，每秒更新一次当前时间
    this.intervalId = setInterval(() => {
      this.currentTime = new Date();
    }, 1000); // 每秒更新一次
  },
  beforeDestroy() {
    // 组件销毁前清除定时器
    clearInterval(this.intervalId);
  },
  methods: {
    ...mapMutations(["setAppTitle", "setPageTitle", "setProblemType"]),
    ...mapActions('snackbar', ['showSnackbar']),
    async fetchProblemSetData(problemSetId) {
      console.log(`Fetching problem set data for ID: ${problemSetId}`);
      this.loading = true;
      this.error = null;
      // 模拟从后端获取模拟测试数据
      const response = await axios.post('http://127.0.0.1:8000/api/exams/get_exam_questions/', {
        user_id: this.$store.getters.getUserId,
        exam_id: problemSetId
      });
      const data = response.data;
      this.problemSetData = {
        id: data.id,
        name: data.name,
        subject: data.subject,
        starttime: data.starttime,
        duration: data.duration,
      };
      const title = "模拟测试详情 - " + this.problemSetData.name;
      this.finishedQuestions = data.finish;
      this.setAppTitle(title);
      this.setPageTitle(title);
      this.fetchQuestionsById(problemSetId); // 获取题目列表
    },

    async fetchQuestionsById(problemSetId) {
      console.log(`Fetching questions for problem set ID: ${problemSetId}`);
      this.error = null;

      try {
        // 模拟从后端获取数据
        const response = await axios.post('http://127.0.0.1:8000/api/exams/get_exam_questions/', {
          user_id: this.$store.getters.getUserId,
          exam_id: problemSetId
        });
        this.questions = response.data.qsdata; // 更新组件本地的题目列表数据
        this.loading = false;
        // 模拟延迟
      } catch (e) {
        console.error("获取题目数据失败", e);
        this.error = "获取题目数据失败";
        this.loading = false;
      }
    },

    formatDate(dateStr) {
      if (!dateStr) return "N/A";
      const options = { year: "numeric", month: '2-digit', day: '2-digit' };
      return new Date(dateStr).toLocaleDateString(undefined, options);
    },

    formatDate2S(dateString) {
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

    parseAnswer(markdownString) {
      const regex = /!\[Alt]\((.+?)\)/; // 正则匹配 ![Alt](...)
      const match = markdownString.match(regex);
      return match ? match[1] : null; // 如果匹配到，返回第一个捕获组，否则返回 null
    },

    async goToQuestionDetail(questionId) {
      this.questionType = this.getQuestionTypeById(questionId);
      this.clearSelection();
      console.log(
        `Fetching question for question ID: ${questionId} ${this.questionType}`
      );
      this.currentQuestionId = questionId;
      // 模拟从后端获取Markdown文本数据
      const response = await axios.post('http://127.0.0.1:8000/api/exams/get_exam_student_questions/', {
        user_id: this.$store.getters.getUserId,
        exam_id: this.$route.params.id,
        question_id: questionId
      });
      console.log(response.data);
      this.question = response.data.question_data.content;
      this.lastAnswer = response.data.answer_now;
      if (response.data.question_data.type === "填空题") {
        this.text = this.lastAnswer;
      }

      if (response.data.question_data.type === '解答题' && this.lastAnswer.length > 0) {
        console.log(this.lastAnswer);
        this.lastAnswer = this.parseAnswer(this.lastAnswer);
        console.log(this.lastAnswer);
      }

      if (this.questionType === "单项选择题") {
        this.choices = response.data.question_data.option_count;
      } else if (this.questionType === "解答题") {
        this.choices = -1;
      } else if (this.questionType === "多项选择题") {
        this.choices = response.data.question_data.option_count;
      } else if (this.questionType === "判断题") {
        this.choices = 2;
      } else {
        this.choices = -3;
      }
      this.dialog = true; // 打开Dialog
    },

    closeDialog() {
      this.dialog = false; // 关闭Dialog
      this.question = ""; // 清空题面
      this.clearSelection(); // 清空选择缓存
    },

    getOptionLetter(index) {
      return String.fromCharCode(64 + index); // 65对应'A'
    },

    clearSelection() {
      if (
        this.questionType === "单项选择题" ||
        this.questionType === "判断题"
      ) {
        this.selectedOption = null;
      } else if (this.questionType === "多项选择题") {
        this.selectedOptions = [];
      } else if (this.questionType === "填空题") {
        this.text = "";
      }
    },

    async submitAnswer() {
      // 处理提交逻辑
      let result = "";
      this.dialog = false;
      if (this.questionType === "单项选择题") {
        console.log("提交的单项选择答案:", this.selectedOption);
        result = this.selectedOption == null ? "null" : String(this.selectedOption);
        this.lastAnswer = result;
      } else if (this.questionType === "多项选择题") {
        console.log("提交的多项选择答案:", [...this.selectedOptions].sort());
        result = ([...this.selectedOptions].sort()).join(',');
        this.lastAnswer = result;
      } else if (this.questionType === "判断题") {
        console.log("提交的判断答案:", this.selectedOption);
        result = this.selectedOption == null ? "null" : (this.selectedOption ? "正确" : "错误");
        this.lastAnswer = result;
      } else if (this.questionType === "填空题") {
        console.log(`提交的填空题答案: ${JSON.stringify(this.text)}`);
        result = this.text;
      } else if (this.questionType === "解答题") {
        console.log("提交了解答题答案");
        result = this.text;
      }
      console.log(this.lastAnswer);
      const response = await axios.post('http://127.0.0.1:8000/api/exams/submit_answer/', {
        user_id: this.$store.getters.getUserId,
        exam_id: this.$route.params.id,
        question_id: this.currentQuestionId,
        submitted_answer: result,
      });
      this.selectedOption = null; // 单项选择题
      this.selectedOptions = []; // 多项选择题
      // 设置 Snackbar 的提示信息和颜色
      this.showSnackbar({
        message: `题目 - ${this.currentQuestionId} 提交成功`,
        color: 'success',
        timeout: 2000
      });
      this.fetchProblemSetData(this.$route.params.id);
    },

    // 文件上传逻辑
    async uploadFiles() {
      console.log(this.files);
      if (!this.files) {
        console.log("没有选择文件");
        return;
      }
      const acceptedTypes = ['image/jpeg', 'image/png', 'image/jpg'];
      const file = this.files;
      if (!acceptedTypes.includes(file.type)) {
        this.showSnackbar({
          message: "提交文件类型仅限.jpg，.png，.jpeg格式",
          color: 'error',
          timeout: 2000
        });
        this.files = null;
        return;
      }
      // 创建一个 FormData 对象
      const formData = new FormData();
      // 将选中的文件添加到 FormData 中
      formData.append("files", file);
      console.log(formData);
      const response = await fetch("http://127.0.0.1:8000/api/images/upload-image/", {
        method: "POST",
        body: formData
      });
      const result = await response.json();
      this.text = String(result.url);
      this.text = `![Alt](${this.text})`;
      console.log(this.text);
      this.files = null;
      this.submitAnswer();
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
  watch: {
    uploading(val) {
      if (!val) return;

      setTimeout(() => (this.uploading = false), 2000)
    },
    remainingTime(newVal) {
      if (newVal === 0 && this.dialog) {
        this.dialog = false;
      }
    },
  }
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

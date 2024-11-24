<template>
  <div class="problem-set-detail" v-if="problemSetData">
    <v-scroll-y-transition mode="out-in">
      <!-- 测试进行中且未完成所有题目 -->
      <div
        v-if="remainingTime > 0 && finishedQuestions.length < totalQuestions"
        style="padding-bottom: 15px"
      >
        <v-alert type="info" icon="mdi-clock-outline">
          <v-alert-title>
            测试进行中，剩余时间：{{ formatDuration(remainingTime) }}
          </v-alert-title>
          你已完成{{ totalQuestions }}题中的{{ finishedQuestions.length }}题。
        </v-alert>
      </div>

      <!-- 测试进行中且已完成所有题目 -->
      <div
        v-else-if="remainingTime > 0 && finishedQuestions.length === totalQuestions"
        style="padding-bottom: 15px"
      >
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
    <v-progress-linear
      v-if="remainingTime > 0"
      :value="progressPercentage"
      color="primary"
      height="9"
      rounded
      style="margin-bottom: 10px"
    ></v-progress-linear>

    <!-- 题库名称 -->
    <h1 style="padding-top: 10px">{{ problemSetData.name }}</h1>

    <!-- 信息芯片 -->
    <div class="chips-row" style="padding-bottom: 5px; margin-bottom: 5px">
      <v-chip
        v-for="(chip, index) in chips"
        :key="index"
        :color="chip.color"
        class="ma-1 chip-item"
      >
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
                <v-btn
                  v-for="questionId in getPaginatedIds(group)"
                  :key="questionId"
                  :class="[
                    'question-square',
                    { finished: finishedQuestions.includes(questionId) },
                  ]"
                  :color="
                    finishedQuestions.includes(questionId)
                      ? 'green'
                      : 'blue-darken-4'
                  "
                  rounded="0"
                  @click="goToQuestionDetail(questionId)"
                >
                  <v-responsive class="text-truncate">{{ questionId }}</v-responsive>
                </v-btn>
              </div>
            </v-row>
            <!-- 分页控件 -->
            <v-row justify="center" class="mt-2">
              <v-pagination
                v-model="group.currentPage"
                :total-visible="7"
                :length="Math.ceil(group.ids.length / pageSize)"
                @input="handlePageChange(group, $event)"
              ></v-pagination>
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
              <div v-if="question" class="markdown-content">
                <v-md-preview :text="question" />
              </div>
              <!-- 加载或错误状态 -->
              <v-alert v-else type="info" class="ma-4">正在加载...</v-alert>
            </v-col>

            <v-col cols="4">
              <v-card class="pa-4" outlined>
                <v-card-title
                  style="padding-left: 0"
                  class="text-h5 font-weight-regular"
                >
                  提交题目 - {{ currentQuestionId }}
                </v-card-title>
                <v-chip color="primary" variant="outlined">
                  {{ questionType }}
                </v-chip>
                <v-spacer></v-spacer>
                <div v-if="choices === -1">
                  <!-- 文件上传 -->
                  <v-file-input
                    v-model="files"
                    label="提交答案"
                    variant="underlined"
                    counter
                    multiple
                    show-size
                    accept=".pdf,.docx,.jpg,.png,.md"
                  >
                    <template v-slot:selection="{ fileNames }">
                      <template v-for="fileName in fileNames" :key="fileName">
                        <v-chip class="me-2" color="primary" size="small" label>
                          {{ fileName }}
                        </v-chip>
                      </template>
                    </template>
                  </v-file-input>
                  <v-btn
                    color="primary"
                    variant="text"
                    @click="uploadFiles"
                    :disabled="!files.length"
                  >
                    上传答案
                  </v-btn>
                </div>
                <div
                  v-else-if="
                    choices >= 3 && questionType === '单项选择题'
                  "
                >
                  <!-- 单项选择题 -->
                  <v-row no-gutters>
                    <v-radio-group v-model="selectedOption" inline>
                      <v-radio
                        v-for="index in choices"
                        :key="index"
                        :label="getOptionLetter(index)"
                        :value="getOptionLetter(index)"
                        dense
                      />
                    </v-radio-group>
                  </v-row>

                  <v-row no-gutters>
                    <v-card-actions>
                      <v-btn
                        color="primary"
                        text="提交"
                        variant="text"
                        :disabled="!selectedOption"
                        @click="submitAnswer"
                      ></v-btn>
                      <v-btn
                        text="清除"
                        variant="plain"
                        @click="clearSelection"
                      ></v-btn>
                    </v-card-actions>
                  </v-row>
                </div>
                <div
                  v-else-if="
                    choices >= 3 && questionType === '多项选择题'
                  "
                >
                  <!-- 多项选择题 -->
                  <v-row no-gutters>
                    <v-container>
                      <v-checkbox
                        v-for="index in choices"
                        v-model="selectedOptions"
                        :key="index"
                        :label="getOptionLetter(index)"
                        :value="getOptionLetter(index)"
                        style="margin-bottom: -30px"
                      />
                    </v-container>
                  </v-row>

                  <v-row no-gutters>
                    <v-card-actions>
                      <v-btn
                        color="primary"
                        text="提交"
                        variant="text"
                        :disabled="selectedOptions.length === 0"
                        @click="submitAnswer"
                      ></v-btn>
                      <v-btn
                        text="清除"
                        variant="plain"
                        @click="clearSelection"
                      ></v-btn>
                    </v-card-actions>
                  </v-row>
                </div>
                <div v-else-if="questionType === '判断题'">
                  <!-- 判断题 -->
                  <v-row no-gutters>
                    <v-radio-group v-model="selectedOption" inline>
                      <v-radio label="正确" value="True" dense />
                      <v-radio label="错误" value="False" dense />
                    </v-radio-group>
                  </v-row>
                  <v-row no-gutters>
                    <v-card-actions>
                      <v-btn
                        color="primary"
                        text="提交"
                        variant="text"
                        :disabled="!selectedOption"
                        @click="submitAnswer"
                      >
                        提交
                      </v-btn>
                      <v-btn text="清除" variant="plain" @click="clearSelection">
                        清除
                      </v-btn>
                    </v-card-actions>
                  </v-row>
                </div>
                <div v-else-if="questionType === '填空题'">
                  <!-- 填空题 -->
                  <v-card-text
                    style="padding-left: 0"
                    class="text-subtitle-3 font-weight-regular"
                  >
                    使用markdown在左侧输入框输入答案，右侧为预览。
                    <br />
                    <a href="https://freeopen.github.io/mathjax/">在markdown中写数学公式</a>
                  </v-card-text>

                  <v-md-editor
                    v-model="text"
                    height="200px"
                    left-toolbar=""
                    right-toolbar=""
                  ></v-md-editor>
                  <v-row no-gutters>
                    <v-card-actions>
                      <v-btn
                        color="primary"
                        text="提交"
                        variant="text"
                        :disabled="!text"
                        @click="submitAnswer"
                      >
                        提交
                      </v-btn>
                      <v-btn text="清除" variant="plain" @click="clearSelection">
                        清除
                      </v-btn>
                    </v-card-actions>
                  </v-row>
                </div>
                <div v-else>暂无提交方式。请联系负责人。</div>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Snackbar for notifications -->
    <v-snackbar v-model="snackbarOpen" :timeout="1000" :color="snackbarColor">
      <div style="font-size: 16px">{{ snackbarMessage }}</div>
      <template #actions>
        <v-btn icon @click="snackbarOpen = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { mapMutations } from "vuex";

export default {
  name: "ProblemSetDetail",
  data() {
    return {
      problemSetData: null,
      questions: [],
      loading: false,
      error: null,
      currentTime: new Date(), // 当前时间
      intervalId: null, // 定时器ID
      dialog: false, // 控制dialog显示
      snackbarOpen: false,
      snackbarMessage: "",
      snackbarColor: "",
      question: "", // 存储题面的Markdown文本
      loadingQuestion: false, // 控制加载状态
      finishedQuestions: [], // 完成的题目
      files: [],
      choices: -2,
      selectedOption: null, // 单项选择题
      selectedOptions: [], // 多项选择题
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
    if (id == 1) {
      this.fetchProblemSetData(id); // 获取模拟测试数据
    } else {
      console.log(id);
      console.error("模拟测试ID缺失，无法加载模拟测试数据");
      this.$router.push(`/404`);
    }

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

    async fetchProblemSetData(problemSetId) {
      console.log(`Fetching problem set data for ID: ${problemSetId}`);
      this.loading = true;
      this.error = null;

      try {
        // 模拟从后端获取模拟测试数据
        setTimeout(() => {
          this.problemSetData = {
            id: problemSetId,
            name: "2023-24数分上期中",
            subject: "工科数学分析（上）",
            starttime: "2024-11-24 15:00:00",
            duration: 140,
          };
          const title = "模拟测试详情 - " + this.problemSetData.name;
          this.finishedQuestions = [301, 302, 303, 441, 442, 1001, 9801, 1912, 1917, 1920];
          this.setAppTitle(title);
          this.setPageTitle(title);
          this.fetchQuestionsById(problemSetId); // 获取题目列表
          this.loading = false;
        }, 1000); // 模拟网络延迟
      } catch (e) {
        console.error("获取模拟测试数据失败", e);
        this.error = "获取模拟测试数据失败";
        this.loading = false;
      }
    },

    async fetchQuestionsById(problemSetId) {
      console.log(`Fetching questions for problem set ID: ${problemSetId}`);
      this.loading = true;
      this.error = null;

      try {
        // 模拟从后端获取数据
        setTimeout(() => {
          const questions = [
            {
              type: "单项选择题",
              ids: [301, 302, 303, 304, 305],
              currentPage: 1, // 当前页
            },
            {
              type: "多项选择题",
              ids: [441, 442, 443, 444, 445, 446],
              currentPage: 1,
            },
            {
              type: "判断题",
              ids: [595, 1001],
              currentPage: 1,
            },
            {
              type: "填空题",
              ids: [9801, 9802, 7002],
              currentPage: 1,
            },
            {
              type: "解答题",
              ids: [1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920], // 解答题
              currentPage: 1,
            },
          ];
          this.questions = questions; // 更新组件本地的题目列表数据
          this.loading = false;
        }, 100); // 模拟延迟
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

    goToQuestionDetail(questionId) {
      this.questionType = this.getQuestionTypeById(questionId);
      console.log(
        `Fetching question for question ID: ${questionId} ${this.questionType}`
      );
      this.loadingQuestion = true;
      this.currentQuestionId = questionId;
      // 模拟从后端获取Markdown文本数据
      setTimeout(() => {
        this.question = `## 这是题目 ${questionId} 的题面\n\n这是详细的Markdown格式题面说明。`;
        this.loadingQuestion = false;
        if (this.questionType === "单项选择题") {
          this.choices = 4;
        } else if (this.questionType === "解答题") {
          this.choices = -1;
        } else if (this.questionType === "多项选择题") {
          this.choices = 4;
        } else if (this.questionType === "判断题") {
          this.choices = 2;
        }
        this.dialog = true; // 打开Dialog
      }, 10); // 模拟网络延迟
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

    submitAnswer() {
      // 处理提交逻辑
      if (this.questionType === "单项选择题") {
        console.log("提交的单项选择答案:", this.selectedOption);
      } else if (this.questionType === "多项选择题") {
        console.log("提交的多项选择答案:", [...this.selectedOptions].sort());
      } else if (this.questionType === "判断题") {
        console.log("提交的判断答案:", this.selectedOption);
      } else if (this.questionType === "填空题") {
        console.log(`提交的填空题答案: ${JSON.stringify(this.text)}`);
      } else if (this.questionType === "解答题") {
        console.log("提交了解答题答案");
      }

      // 模拟提交结果，有50%的概率成功，50%的概率失败
      const isSuccess = Math.random() < 0.5;

      // 设置 Snackbar 的提示信息和颜色
      if (isSuccess) {
        this.snackbarMessage = "题目 - " + this.currentQuestionId + " 提交成功";
        this.snackbarColor = "success";
      } else {
        this.snackbarMessage = "题目 - " + this.currentQuestionId + " 提交失败";
        this.snackbarColor = "error";
      }
      this.snackbarOpen = true;
    },

    // 文件上传逻辑
    async uploadFiles() {
      if (!this.files.length) {
        console.log("没有选择文件");
        return;
      }

      // 创建一个 FormData 对象
      const formData = new FormData();

      // 将选中的文件添加到 FormData 中
      this.files.forEach((file) => {
        formData.append("files[]", file);
      });
      console.log("文件上传成功");
      this.files = [];
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

/* Snackbar styles */
.v-snackbar {
  font-size: 16px;
}
</style>

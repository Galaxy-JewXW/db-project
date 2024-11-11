<template>
  <div class="problem-set-detail" v-if="problemSetData">
    <h1>{{ problemSetData.name }}</h1>

    <!-- Chip row: contains all fields as Chips in the same row -->
    <div class="chips-row">
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

    <!-- Description -->
    <p>{{ problemSetData.description }}</p>

    <!-- Scrollable container for questions -->
    <div class="questions-container">
      <v-expansion-panels>
        <v-expansion-panel
          v-for="(group, index) in questions"
          :key="index"
        >
          <v-expansion-panel-title>
            <template v-slot:default="{ expanded }">
              <v-row no-gutters>
                <v-col class="d-flex justify-start text-bold" cols="4">
                  {{ group.type }}
                </v-col>
                <v-col class="text-grey" cols="8">
                  <v-fade-transition leave-absolute>
                    <span> 本部分共 {{ group.ids.length }} 题 </span>
                  </v-fade-transition>
                </v-col>
              </v-row>
            </template>
          </v-expansion-panel-title>

          <!-- List of buttons for each question ID inside the content -->
          <v-expansion-panel-text>
            <v-row no-gutters>
              <div class="question-squares">
                <v-btn
                  v-for="questionId in group.ids"
                  :key="questionId"
                  class="question-square text-none"
                  color="blue-darken-4"
                  rounded="0"
                  @click="goToQuestionDetail(questionId)"
                >
                  <v-responsive class="text-truncate">{{ questionId }}</v-responsive>
                </v-btn>
              </div>
            </v-row>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </div>
  </div>
  <!-- Loading indicator or error message -->
  <div v-else>
    <p v-if="loading">即将就绪……</p>
    <p v-else-if="error">{{ error }}</p>
  </div>
</template>

<script>
import { mapMutations } from 'vuex';

export default {
  name: "ProblemSetDetail",
  data() {
    return {
      problemSetData: null, // 本地存储题库数据
      questions: [],
      loading: false,
      error: null,
    };
  },
  computed: {
    totalQuestions() {
      return this.questions?.reduce((total, group) => {
        return total + group.ids.length;
      }, 0) || 0;
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
          label: "预计用时",
          value: `${this.problemSetData?.estimatedTime || 0} 分钟`,
        },
        {
          color: "success",
          icon: "mdi-calendar",
          label: "创建日期",
          value: this.formatDate(this.problemSetData?.createdAt),
        },
        {
          color: "info",
          icon: "mdi-account",
          label: "创建者",
          value: this.problemSetData?.createdBy || "N/A",
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
    if (id == 1) {
      this.fetchProblemSetData(id); // 获取题库数据
    } else {
      console.log(id);
      console.error("题库ID缺失，无法加载题库数据");
      this.$router.push(`/404`);
    }
  },
  methods: {
    ...mapMutations(["setAppTitle", "setPageTitle", "setProblemType"]),

    async fetchProblemSetData(problemSetId) {
      console.log(`Fetching problem set data for ID: ${problemSetId}`);
      this.loading = true;
      this.error = null;

      try {
        // 模拟从后端获取题库数据
        setTimeout(() => {
          this.problemSetData = {
            id: problemSetId,
            name: "2023-24数分上期中",
            createdAt: "2024-09-02",
            subject: "工科数学分析（上）",
            createdBy: "fysszlr",
            estimatedTime: 120,
            description: "2023-2024第一学期数分期中的真题，配套答案。",
          };
          const title = '题库详情 - ' + this.problemSetData.name;
          this.setAppTitle(title);
          this.setPageTitle(title);
          this.fetchQuestionsById(problemSetId); // 获取题目列表
          this.loading = false;
        }, 1000); // 模拟网络延迟
      } catch (e) {
        console.error("获取题库数据失败", e);
        this.error = "获取题库数据失败";
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
              type: "选择题",
              ids: [...Array(50).keys()].map((i) => i + 1), // 生成 50 道选择题
            },
            {
              type: "填空题",
              ids: [101, 102, 103], // 填空题
            },
            {
              type: "解答题",
              ids: [201, 202], // 解答题
            },
          ];
          this.questions = questions; // 更新组件本地的题目列表数据
          this.loading = false;
        }, 1000); // 模拟延迟
      } catch (e) {
        console.error("获取题目数据失败", e);
        this.error = "获取题目数据失败";
        this.loading = false;
      }
    },

    formatDate(dateStr) {
      if (!dateStr) return "N/A";
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(dateStr).toLocaleDateString(undefined, options);
    },

    goToQuestionDetail(questionId) {
      console.log(`Navigate to question detail for question ID: ${questionId}`);
      this.$router.push(`/exercise/id=${questionId}`);
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
  max-height: calc(100vh - 250px);
  overflow-y: auto;
  padding: 16px 16px 32px;
  display: flex;
  flex-direction: column;
  scrollbar-width: none;
}

.questions-container::-webkit-scrollbar {
  display: none;
}

.questions-container {
  -ms-overflow-style: none;
  scrollbar-width: none;
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
</style>

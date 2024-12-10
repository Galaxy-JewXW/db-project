<template>
  <div class="problem-set-detail" v-if="problemSetData">
    <h1>{{ problemSetData.name }}</h1>

    <!-- Chip row: contains all fields as Chips in the same row -->
    <div class="chips-row">
      <v-chip v-for="(chip, index) in chips" :key="index" :color="chip.color" class="ma-1 chip-item">
        <v-icon left class="chip-icon">{{ chip.icon }}</v-icon>
        {{ chip.label }}: {{ chip.value }}
      </v-chip>
    </div>

    <!-- Description -->
    <p>{{ problemSetData.description }}</p>

    <!-- Scrollable container for questions -->
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
                <v-btn v-for="questionId in getPaginatedIds(group)" :key="questionId" class="question-square text-none"
                  :color="finishedQuestions.includes(questionId) ? 'green' : 'blue-darken-4'" rounded="0"
                  @click="goToQuestionDetail(questionId)">
                  <v-responsive class="text-truncate">{{ questionId }}</v-responsive>
                </v-btn>
              </div>
            </v-row>
            <!-- 添加分页控件 -->
            <v-row justify="center" class="mt-2">
              <v-pagination v-model="group.currentPage" :total-visible="7"
                :length="Math.ceil(group.ids.length / pageSize)"
                @input="handlePageChange(group, $event)"></v-pagination>
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
import axios from "axios";
import store from "@/store";
export default {
  name: "ProblemSetDetail",
  data() {
    return {
      problemSetData: null, // 本地存储题库数据
      questions: [],
      loading: false,
      error: null,
      pageSize: 10, // 每页显示的题目数量
      finishedQuestions: [], // 完成的题目
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
    // TODO: 这里是调试逻辑，以后记得删除
    this.fetchProblemSetData(id); // 获取题库数据

  },
  methods: {
    ...mapMutations(["setAppTitle", "setPageTitle", "setProblemType"]),

    async fetchProblemSetData(problemSetId) {
      console.log(`Fetching problem set data for ID: ${problemSetId}`);
      this.loading = true;
      this.error = null;

      try {
        // 模拟从后端获取题库数据
        const response = await axios.post('http://127.0.0.1:8000/api/questions/get_questionbank/', {
          user_id: this.$store.getters.getUserId,
          question_bank_id: this.$route.params.id
        });
        const data=response.data.question_bank;
        this.problemSetData = {
          id: data.id,
          name: data.name,
          createdAt: data.created_at,
          subject: data.subject,
          createdBy: data.creator,
          estimatedTime: data.estimated_time, // 120 分钟
          description: data.description,
        };
        const title = '题库详情 - ' + this.problemSetData.name;
        this.setAppTitle(title);
        this.setPageTitle(title);
        this.fetchQuestionsById(problemSetId); // 获取题目列表
        this.loading = false;
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
        // 发送 POST 请求到后端获取数据
        const response = await axios.post('http://127.0.0.1:8000/api/questions/get_questions_by_questionbank/', {
          user_id: this.$store.getters.getUserId,
          question_bank_id: problemSetId
        });

        // 检查后端返回的响应
        if (response.data.success) {
          const data = response.data;

          // 将后端返回的题目信息映射到前端的 `questions` 结构
          const questions = data.questions.map((question) => {
            return {
              type: question.type, // 保留题型
              ids: question.ids.map((id) => (id)),
              currentPage: question.currentPage, // 保留当前页信息
            };
          });

          // 更新组件的题目数据
          this.questions = questions;
          this.loading = false;
          this.finishedQuestions = data.finish_question;
        } else {
          throw new Error("获取题目数据失败");
        }
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

    getPaginatedIds(group) {
      const start = (group.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return group.ids.slice(start, end);
    },

    handlePageChange(group, newPage) {
      group.currentPage = newPage;
    },

    goToQuestionDetail(questionId) {
      console.log(`Navigate to question detail for question ID: ${questionId}`);
      this.$router.push(`/exercise/${questionId}`);
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

.question-square.finished {
  opacity: 0.6;
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
</style>

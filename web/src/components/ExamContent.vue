<template>
  <v-container fluid class="problemset-container">
    <!-- Button to open Past Exams Dialog -->
    <v-btn class="align-self-start" color="primary" @click="showPastExamsDialog = true">
      查看过往测试
    </v-btn>

    <!-- Past Exams Dialog -->
    <v-dialog
      v-model="showPastExamsDialog"
      transition="dialog-bottom-transition"
      fullscreen
    >
      <v-card>
        <v-toolbar dark color="primary">
          <v-btn icon dark @click="showPastExamsDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>已结束的测试列表</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <!-- Display pastExams here -->
          <template v-if="pastExams.length > 0">
            <v-row dense class="justify-start">
              <v-col
                v-for="exam in pastExams"
                :key="exam.id"
                cols="12"
                sm="6"
                md="3"
                class="pa-1"
              >
                <v-card class="w-100" hover>
                  <v-card-text>
                    <p class="text-h5 font-weight-bold">{{ exam.name }}</p>
                    <div class="mt-2">
                      <div class="info-row">
                        <span>创建日期：</span>
                        <span>{{ formatDate2M(exam.createdAt) }}</span>
                      </div>
                      <div class="info-row">
                        <span>所属科目：</span>
                        <span>{{ exam.subject }}</span>
                      </div>
                      <div class="info-row">
                        <span>开始时间：</span>
                        <span>{{ formatDate2M(exam.starttime) }}</span>
                      </div>
                      <div class="info-row">
                        <span>时长：</span>
                        <span>{{ exam.duration }} 分钟</span>
                      </div>
                    </div>
                  </v-card-text>
                  <v-card-actions>
                    <v-btn
                      class="enter-button"
                      text
                      @click.stop="enterExam(exam)"
                    >
                      查看
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </template>
          <div v-else class="no-results">没有过往的测试</div>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Combined Exams Section -->
    <h2 style="padding-top: 20px;">测试列表</h2>
    <div class="scroll-container">
      <template v-if="combinedExams.length > 0">
        <v-row dense class="justify-start">
          <v-col
            v-for="exam in combinedExams"
            :key="exam.id"
            cols="12"
            sm="6"
            md="3"
            class="pa-1"
          >
            <v-card class="w-100" hover>
              <v-card-text>
                <p class="text-h5 font-weight-bold">{{ exam.name }}</p>

                <div class="mt-2">
                  <div class="info-row">
                    <span>创建日期：</span>
                    <span>{{ formatDate2D(exam.createdAt) }}</span>
                  </div>
                  <div class="info-row">
                    <span>所属科目：</span>
                    <span>{{ exam.subject }}</span>
                  </div>
                  <div class="info-row">
                    <span>开始时间：</span>
                    <span>{{ formatDate2M(exam.starttime) }}</span>
                  </div>
                  <div class="info-row">
                    <span>时长：</span>
                    <span>{{ exam.duration }} 分钟</span>
                  </div>
                </div>
              </v-card-text>
              <v-card-actions>
                <v-btn
                  class="enter-button"
                  text
                  :disabled="isExamComing(exam)"
                  @click.stop="enterExam(exam)"
                >
                {{ isExamComing(exam) ? "测试尚未开始" : "进入模拟测试" }}
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </template>
      <div v-else class="no-results">没有测试</div>
    </div>
  </v-container>
</template>

<script>
import { mapMutations } from "vuex";

export default {
  name: "ExamList",
  data() {
    return {
      showPastExamsDialog: false,
      ongoingExams: [
        {
          id: 1,
          name: "2023-24数分上期中",
          createdAt: "2024-09-02",
          subject: "工科数学分析（上）",
          starttime: "2024-11-13 19:00:00",
          duration: 120,
        },
      ],
      pastExams: [
        {
          id: 3,
          name: "2023-24数分上期末",
          createdAt: "2024-01-15",
          subject: "工科数学分析（上）",
          starttime: "2024-01-15 09:00:00",
          duration: 120,
        },
      ],
      comingExams: [
        {
          id: 2,
          name: "2023-24数分上期末",
          createdAt: "2024-12-01",
          subject: "工科数学分析（上）",
          starttime: "2024-12-15 09:00:00",
          duration: 120,
        },
      ],
    };
  },
  computed: {
    combinedExams() {
      return [...this.ongoingExams, ...this.comingExams];
    },
  },
  mounted() {
    const title = "模拟测试";
    this.setAppTitle(title);
    this.setPageTitle(title);
  },
  methods: {
    // 映射 Vuex 的 mutation
    ...mapMutations(["setAppTitle", "setPageTitle"]),

    formatDate2M(dateStr) {
      const options = {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      };
      return new Date(dateStr).toLocaleString(undefined, options);
    },
    formatDate2D(dateStr) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(dateStr).toLocaleDateString(undefined, options);
    },
    enterExam(exam) {
      // 导航到目标路由
      this.$router.push(`/exam/${exam.id}`);
    },
    isExamComing(exam) {
      return this.comingExams.some((e) => e.id === exam.id);
    },
  },
};
</script>

<style scoped>
/* Set box-sizing globally */
* {
  box-sizing: border-box;
}

.problemset-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.scroll-container {
  flex: 1 1 auto;
  overflow-y: auto;
  padding: 16px;
  padding-bottom: 80px;

  /* Hide scrollbar */
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scroll-container::-webkit-scrollbar {
  display: none;
}

.mt-2 {
  margin-top: 0.5rem;
}

.pa-1 {
  padding: 0.25rem !important;
}

.info-row {
  margin-bottom: 0.1rem;
}

.no-results {
  font-size: 1.2rem;
  color: #777;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.enter-button {
  color: #1867c0 !important;
}

@media (min-width: 960px) {
  .v-row {
    margin-left: -8px;
    margin-right: -8px;
  }
  .v-col.pa-1 {
    padding-left: 8px !important;
    padding-right: 8px !important;
  }
}
</style>

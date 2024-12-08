<!-- components/ExamList.vue -->
<template>
  <v-container fluid class="problemset-container">
    <!-- Button to open Past Exams Dialog -->
    <v-btn class="align-self-start" color="primary" @click="showPastExamsDialog = true">
      查看过往测试
    </v-btn>

    <!-- Past Exams Dialog -->
    <v-dialog v-model="showPastExamsDialog" transition="dialog-bottom-transition" fullscreen>
      <v-card>
        <v-toolbar dark color="primary">
          <v-btn icon dark @click="showPastExamsDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>已结束的测试列表</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <!-- Filter Section -->
          <div class="filter-container">
            <v-card class="filter-card" flat elevation="0">
              <v-card-text class="py-2">
                <v-row>
                  <!-- Subject Filter -->
                  <v-col cols="12" class="filter-section" style="padding-bottom: 0px">
                    <div class="filter-group">
                      <span class="filter-label">按科目筛选:</span>
                      <v-chip v-for="subject in subjects" :key="subject" class="ma-2" color="primary" variant="outlined"
                        :class="{
                          'selected-chip': selectedSubject === subject,
                        }" @click="toggleSubject(subject)">
                        {{ subject }}
                        <v-icon v-if="selectedSubject === subject" class="ml-2" small>
                          mdi-check
                        </v-icon>
                      </v-chip>
                    </div>
                  </v-col>

                  <!-- Time Filter -->
                  <v-col cols="12" class="filter-section" style="padding-top: 0px">
                    <div class="filter-group">
                      <span class="filter-label">按时间筛选:</span>
                      <v-chip v-for="range in timeRanges" :key="range.value" class="ma-2" color="primary"
                        variant="outlined" :class="{
                          'selected-chip': selectedTimeRange === range.value,
                        }" @click="toggleTimeRange(range.value)">
                        {{ range.text }}
                        <v-icon v-if="selectedTimeRange === range.value" class="ml-2" small>
                          mdi-check
                        </v-icon>
                      </v-chip>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </div>

          <!-- Display pastExams here -->
          <template v-if="filteredProblemSets.length > 0">
            <v-row dense class="justify-start">
              <v-col v-for="exam in filteredProblemSets" :key="exam.id" cols="12" sm="6" md="3" class="pa-1">
                <v-card class="w-100" hover>
                  <v-card-text>
                    <p class="text-h5 font-weight-bold">{{ exam.name }}</p>
                    <div class="mt-2">
                      <div class="info-row">
                        <span>创建日期：</span>
                        <span>{{ formatDate(exam.createdAt) }}</span>
                      </div>
                      <div class="info-row">
                        <span>所属科目：</span>
                        <span>{{ exam.subject }}</span>
                      </div>
                      <div class="info-row">
                        <span>开始时间：</span>
                        <span>{{ formatDate(exam.starttime) }}</span>
                      </div>
                      <div class="info-row">
                        <span>时长：</span>
                        <span>{{ exam.duration }} 分钟</span>
                      </div>
                    </div>
                  </v-card-text>
                  <v-card-actions>
                    <v-btn class="enter-button" text @click.stop="this.$router.push(`/exam/${exam.id}`)">
                      查看
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </template>
          <div v-else class="no-results">没有符合条件的测试</div>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Combined Exams Section -->
    <h2 style="padding-top: 20px">测试列表</h2>
    <div class="scroll-container">
      <template v-if="combinedExams.length > 0">
        <v-row dense class="justify-start">
          <v-col v-for="exam in combinedExams" :key="exam.id" cols="12" sm="6" md="3" class="pa-1">
            <v-card class="w-100" hover>
              <v-card-text>
                <p class="text-h5 font-weight-bold">{{ exam.name }}</p>

                <div class="mt-2">
                  <div class="info-row">
                    <span>创建日期：</span>
                    <span>{{ formatDate(exam.createdAt) }}</span>
                  </div>
                  <div class="info-row">
                    <span>所属科目：</span>
                    <span>{{ exam.subject }}</span>
                  </div>
                  <div class="info-row">
                    <span>开始时间：</span>
                    <span>{{ formatDate(exam.starttime) }}</span>
                  </div>
                  <div class="info-row">
                    <span>时长：</span>
                    <span>{{ exam.duration }} 分钟</span>
                  </div>
                </div>
              </v-card-text>
              <v-card-actions>
                <div v-if="isExamComing(exam)">
                  <v-btn class="enter-button" text @click.stop="modifyEnrollmentStatus(exam)">
                    {{
                      this.enrolledExams.includes(exam.id)
                        ? "取消报名"
                        : "报名测试"
                    }}
                  </v-btn>
                </div>
                <div v-else>
                  <div v-if="this.enrolledExams.includes(exam.id)">
                    <v-btn class="enter-button" @click.stop="enterExam(exam)">
                      进入测试
                    </v-btn>
                    <v-btn v-if="this.enrolledExams.includes(exam.id)" variant="plain"
                      @click.stop="modifyEnrollmentStatus(exam)">
                      取消报名
                    </v-btn>
                  </div>
                  <div v-else>
                    <v-btn class="enter-button" text @click.stop="enterExam(exam)">
                      {{
                        this.enrolledExams.includes(exam.id)
                          ? "进入测试"
                          : "报名测试"
                      }}
                    </v-btn>
                  </div>
                </div>
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
import { mapMutations, mapActions } from "vuex";

export default {
  name: "ExamList",
  data() {
    return {
      snackbarMessage: "",
      showPastExamsDialog: false,
      ongoingExams: [
        {
          id: 1,
          name: "2023-24数分上期中 a",
          createdAt: "2024-09-02 19:00:00",
          subject: "工科数学分析（上）",
          starttime: "2024-11-13 19:00:00",
          duration: 120,
        },
        {
          id: 11,
          name: "2023-24数分上期中",
          createdAt: "2024-09-02 19:00:00",
          subject: "工科数学分析（上）",
          starttime: "2024-11-13 19:00:00",
          duration: 120,
        },
      ],
      pastExams: [
        {
          id: 3,
          name: "2023-24数分上期末 a",
          createdAt: "2024-01-15 19:00:00",
          subject: "工科数学分析（上）",
          starttime: "2024-01-15 09:00:00",
          duration: 120,
        },
        {
          id: 31,
          name: "2023-24数分上期末",
          createdAt: "2024-01-15 19:00:00",
          subject: "工科数学分析（上）",
          starttime: "2024-01-15 09:00:00",
          duration: 120,
        },
        // ... 其他过往测试数据
      ],
      comingExams: [
        {
          id: 2,
          name: "2023-24数分期末模拟测试 a",
          createdAt: "2024-12-01 19:00:00",
          subject: "工科数学分析（上）",
          starttime: "2024-12-15 09:00:00",
          duration: 120,
        },
        {
          id: 21,
          name: "2023-24数分期末模拟测试",
          createdAt: "2024-12-01 19:00:00",
          subject: "工科数学分析（上）",
          starttime: "2024-12-15 09:00:00",
          duration: 120,
        },
        // ... 其他即将到来的测试数据
      ],
      subjects: [
        "工科数学分析（上）",
        "工科数学分析（下）",
        "工科高等代数",
        "离散数学（信息类）",
        "基础物理学A",
      ],
      timeRanges: [
        { text: "最近7天", value: "7d" },
        { text: "最近1个月", value: "1m" },
        { text: "最近半年", value: "6m" },
        { text: "最近一年", value: "1y" },
      ],
      selectedSubject: null, // 新增: 当前选择的科目
      selectedTimeRange: null, // 新增: 当前选择的时间范围
      enrolledExams: [2, 3],
    };
  },
  computed: {
    combinedExams() {
      return [...this.ongoingExams, ...this.comingExams];
    },
    filteredProblemSets() {
      let filtered = this.pastExams;

      // 按科目筛选
      if (this.selectedSubject) {
        filtered = filtered.filter((ps) => ps.subject === this.selectedSubject);
      }

      // 按时间筛选
      if (this.selectedTimeRange) {
        const now = new Date();
        let fromDate;

        switch (this.selectedTimeRange) {
          case "7d":
            fromDate = new Date();
            fromDate.setDate(now.getDate() - 7);
            break;
          case "1m":
            fromDate = new Date();
            fromDate.setMonth(now.getMonth() - 1);
            break;
          case "6m":
            fromDate = new Date();
            fromDate.setMonth(now.getMonth() - 6);
            break;
          case "1y":
            fromDate = new Date();
            fromDate.setFullYear(now.getFullYear() - 1);
            break;
          default:
            fromDate = null;
        }

        if (fromDate) {
          filtered = filtered.filter(
            (ps) => new Date(ps.createdAt) >= fromDate
          );
        }
      }

      return filtered;
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
    ...mapActions('snackbar', ['showSnackbar']),
    formatDate(dateString) {
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
    enterExam(exam) {
      // 导航到目标路由
      if (this.enrolledExams.includes(exam.id)) {
        this.$router.push(`/exam/${exam.id}`);
      } else {
        this.enrolledExams.push(exam.id);
        this.showSnackbar({
          message: `成功报名 ${exam.name}`,
          color: 'success',
          timeout: 2000
        });
      }
    },
    modifyEnrollmentStatus(exam) {
      if (this.enrolledExams.includes(exam.id)) {
        this.enrolledExams = this.enrolledExams.filter((id) => id !== exam.id);
        this.showSnackbar({
          message: `成功取消报名 ${exam.name}`,
          color: 'success',
          timeout: 2000
        });
      } else {
        this.enrolledExams.push(exam.id);
        this.showSnackbar({
          message: `成功报名 ${exam.name}`,
          color: 'success',
          timeout: 2000
        });
      }
    },
    isExamComing(exam) {
      return this.comingExams.some((e) => e.id === exam.id);
    },
    toggleSubject(subject) {
      if (this.selectedSubject === subject) {
        this.selectedSubject = null;
      } else {
        this.selectedSubject = subject;
      }
    },
    toggleTimeRange(range) {
      if (this.selectedTimeRange === range) {
        this.selectedTimeRange = null;
      } else {
        this.selectedTimeRange = range;
      }
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

/* Reduce vertical height of the filter card */
.filter-card {
  margin-bottom: 4px;
}

.filter-card .v-card-text {
  padding-top: 4px !important;
  padding-bottom: 4px !important;
}

/* Adjust the padding inside the filter sections */
.filter-section {
  margin-bottom: 0.1rem;
}

.filter-group {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 2px;
}

.filter-label {
  margin-right: 0.5rem;
  font-weight: bold;
}

.v-chip {
  margin: 1px;
  border: 1px solid #1867c0;
  cursor: pointer;
  color: #1867c0;
}

.selected-chip {
  background-color: #1867c0 !important;
  color: white !important;
}

.selected-chip .v-icon {
  color: white !important;
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
  height: 40%;
}

.enter-button {
  color: #1867c0 !important;
}

.total-count {
  margin-left: 16px;
  font-weight: bold;
  margin-bottom: 8px;
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

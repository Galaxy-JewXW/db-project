<!-- components/ProblemSet.vue -->
<template>
  <v-container fluid class="problemset-container">
    <!-- Filter Section -->
    <div class="filter-container">
      <v-card class="filter-card" flat elevation="0">
        <v-card-text class="py-2">
          <v-row>
            <!-- Subject Filter -->
            <v-col cols="12" class="filter-section" style="padding-bottom: 0px;">
              <div class="filter-group">
                <span class="filter-label">按科目筛选:</span>
                <v-chip v-for="subject in subjects" :key="subject" class="ma-2" color="primary" variant="outlined"
                  :class="{ 'selected-chip': selectedSubject === subject }" @click="toggleSubject(subject)">
                  {{ subject }}
                  <v-icon v-if="selectedSubject === subject" class="ml-2" small>
                    mdi-check
                  </v-icon>
                </v-chip>
              </div>
            </v-col>

            <!-- Time Filter -->
            <v-col cols="12" class="filter-section" style="padding-top: 0px;">
              <div class="filter-group">
                <span class="filter-label">按时间筛选:</span>
                <v-chip v-for="range in timeRanges" :key="range.value" class="ma-2" color="primary" variant="outlined"
                  :class="{
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

    <!-- Total Count -->
    <div class="total-count">
      共 {{ filteredProblemSets.length }} 个满足条件的题库
    </div>

    <!-- Scroll Container -->
    <div class="scroll-container">
      <template v-if="filteredProblemSets.length > 0">
        <!-- Problem Set Cards -->
        <v-row dense class="justify-start">
          <v-col v-for="problemSet in filteredProblemSets" :key="problemSet.id" cols="12" sm="6" md="3" class="pa-1">
            <v-card class="w-100" hover @click="openDialog(problemSet)">
              <v-card-text>
                <p class="text-h5 font-weight-bold">{{ problemSet.name }}</p>

                <div class="mt-2">
                  <div class="info-row">
                    <span>创建日期：</span>
                    <span>{{ formatDate(problemSet.createdAt) }}</span>
                  </div>
                  <div class="info-row">
                    <span>创建者：</span>
                    <span>{{ problemSet.createdBy }}</span>
                  </div>
                  <div class="info-row">
                    <span>所属科目：</span>
                    <span>{{ problemSet.subject }}</span>
                  </div>
                  <div class="info-row">
                    <span>预计用时：</span>
                    <span>{{ problemSet.estimatedTime }} 分钟</span>
                  </div>
                </div>
              </v-card-text>

              <v-card-actions>
                <v-btn class="enter-button" text @click.stop="enterProblemSet(problemSet)">
                  进入题库
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </template>

      <!-- No Results Message -->
      <div v-else class="no-results">没有满足条件的题库</div>
    </div>

    <!-- Details Dialog -->
    <v-dialog v-model="dialog" max-width="800px" scrollable>
      <v-card>
        <v-card-title class="headline">{{
          selectedProblemSet.name
        }}</v-card-title>
        <v-card-subtitle>
          <span class="text--secondary">创建者：{{ selectedProblemSet.createdBy }}</span>
          &nbsp;
          <span class="text--secondary">创建日期：{{ formatDate(selectedProblemSet.createdAt) }}</span>
          &nbsp;
          <span class="text--secondary">所属科目：{{ selectedProblemSet.subject }}</span>
        </v-card-subtitle>
        <v-card-text>
          <div class="info-row">
            <span>{{ selectedProblemSet.description }}</span>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="dialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { mapMutations } from "vuex";
import axios from 'axios';
export default {
  name: "ProblemSet",
  data() {
    return {
      problemSets: [
        // 示例数据，添加了 description 字段
        {
          id: 1,
          name: "2023-24数分上期中",
          createdAt: "2024-09-02",
          subject: "工科数学分析（上）",
          createdBy: "fysszlr",
          estimatedTime: 120,
          description: "2023-2024第一学期数分期中的真题，配套答案。",
        },
        // ... 其他题库数据
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
      selectedSubject: null,
      selectedTimeRange: null,
      dialog: false,
      selectedProblemSet: {},
    };
  },
  mounted() {
    const title = "题库";
    this.setAppTitle(title);
    this.setPageTitle(title);
    this.getAll();
  },
  computed: {
    filteredProblemSets() {
      let filtered = this.problemSets;

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
  methods: {
    // 映射 Vuex 的 mutation
    ...mapMutations(['setAppTitle', 'setPageTitle']),
    async getAll() {
      try {
        const userId = this.$store.getters.getUserId; 

        const requestData = {
          user_id: userId,
        };

        const response = await axios.post('http://127.0.0.1:8000/api/questions/get_all_question_banks/', requestData, {
          headers: {
            'Content-Type': 'application/json',  // 指定请求体的格式为 JSON
          }
        });
        if (response.data.success) {
          this.problemSets = response.data.question_banks;
          console.log('请求成功:', response.data);
        } else {
          console.log('请求失败');
        }
      } catch (error) {
        // 请求失败时处理错误
        console.error('请求失败:', error);
      }
    },
    formatDate(dateStr) {
      const options = { year: "numeric", month: '2-digit', day: '2-digit' };
      return new Date(dateStr).toLocaleDateString(undefined, options);
    },
    openDialog(problemSet) {
      this.selectedProblemSet = problemSet;
      this.dialog = true;
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
    enterProblemSet(problemSet) {
      // 导航到目标路由
      this.$router.push(`/problemset/${problemSet.id}`);
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

.filter-container {
  flex-shrink: 0;
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

/* Scroll Container */
.scroll-container {
  flex: 1 1 auto;
  overflow-y: auto;
  padding: 16px;
  padding-bottom: 80px;

  /* 隐藏滚动条 */
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scroll-container::-webkit-scrollbar {
  display: none;
}

/* Other styles */
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
  height: 100%;
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

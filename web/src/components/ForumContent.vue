<!-- components/DiscussionArea.vue -->
<template>
  <v-container fluid class="discussion-container">
    <!-- Filter Section -->
    <div class="filter-container">
      <v-card class="filter-card" flat elevation="0">
        <v-card-text class="py-2">
          <v-row>
            <!-- 标签筛选 -->
            <v-col cols="12" class="filter-section" style="padding-bottom: 0px">
              <div class="filter-group">
                <span class="filter-label">按标签筛选:</span>
                <v-chip
                  v-for="tag in subjects"
                  :key="tag"
                  class="ma-2"
                  color="primary"
                  variant="outlined"
                  :class="{ 'selected-chip': selectedTag === tag }"
                  @click="toggleTag(tag)"
                >
                  {{ tag }}
                  <v-icon v-if="selectedTag === tag" class="ml-2" small>
                    mdi-check
                  </v-icon>
                </v-chip>
              </div>
            </v-col>

            <!-- 时间筛选 -->
            <v-col cols="12" class="filter-section" style="padding-top: 0px">
              <div class="filter-group">
                <span class="filter-label">按时间筛选:</span>
                <v-chip
                  v-for="range in timeRanges"
                  :key="range.value"
                  class="ma-2"
                  color="primary"
                  variant="outlined"
                  :class="{
                    'selected-chip': selectedTimeRange === range.value,
                  }"
                  @click="toggleTimeRange(range.value)"
                >
                  {{ range.text }}
                  <v-icon
                    v-if="selectedTimeRange === range.value"
                    class="ml-2"
                    small
                  >
                    mdi-check
                  </v-icon>
                </v-chip>
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </div>

    <!-- 总数显示 -->
    <div class="total-count">
      共 {{ filteredDiscussions.length }} 个满足条件的讨论贴
    </div>

    <!-- Scroll Container -->
    <div class="scroll-container">
      <template v-if="filteredDiscussions.length > 0">
        <!-- 讨论贴卡片 -->
        <v-row dense class="justify-start">
          <v-col
            v-for="discussion in filteredDiscussions"
            :key="discussion.id"
            cols="12"
            sm="6"
            md="4"
            lg="3"
            class="pa-2"
          >
            <v-card class="w-100" hover @click="openDialog(discussion)">
              <v-card-text>
                <p class="text-h5 font-weight-bold">{{ discussion.title }}</p>

                <div class="mt-2">
                  <div class="info-row">
                    <span>发布者：</span>
                    <span>{{ discussion.publisher }}</span>
                  </div>
                  <div class="info-row">
                    <span>发布时间：</span>
                    <span>{{ formatDate(discussion.publishTime) }}</span>
                  </div>
                  <div class="info-row">
                    <span>标签：</span>
                    <v-chip small color="secondary" class="ma-1">
                      {{ discussion.tag }}
                    </v-chip>
                  </div>
                  <div class="info-row">
                    <span>概要：</span>
                    <span>{{ discussion.summary }}</span>
                  </div>
                </div>
              </v-card-text>

              <v-card-actions>
                <v-btn
                  class="view-button"
                  text
                  @click.stop="viewDiscussion(discussion)"
                >
                  查看详情
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </template>

      <!-- 无结果提示 -->
      <div v-else class="no-results">没有满足条件的讨论贴</div>
    </div>

    <!-- 详情对话框 -->
    <v-dialog v-model="dialog" max-width="800px" scrollable>
      <v-card>
        <v-card-title class="headline">{{
          selectedDiscussion.title
        }}</v-card-title>
        <v-card-subtitle>
          <span class="text--secondary"
            >发布者：{{ selectedDiscussion.publisher }}</span
          >
          &nbsp;
          <span class="text--secondary"
            >发布时间：{{ formatDate(selectedDiscussion.publishTime) }}</span
          >
          &nbsp;
          <span class="text--secondary"
            >标签：{{ selectedDiscussion.tag }}</span
          >
        </v-card-subtitle>
        <v-card-text>
          <div class="info-row">
            <span>{{ selectedDiscussion.description }}</span>
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

export default {
  name: "DiscussionArea",
  data() {
    return {
      discussions: [
        // 示例数据，包含 description 字段
        {
          id: 1,
          title: "关于工科数学分析的疑问",
          publisher: "张三",
          publishTime: "2024-10-01",
          tag: "工科数学分析（上）",
          summary:
            "在学习工科数学分析时，对积分部分有些疑问，特别是多重积分的应用。",
          description: "详细讨论工科数学分析中的多重积分应用及相关问题。",
        },
        {
          id: 2,
          title: "离散数学在计算机科学中的应用",
          publisher: "李四",
          publishTime: "2024-09-25",
          tag: "离散数学（信息类）",
          summary: "探讨离散数学在算法设计和数据结构中的实际应用。",
          description: "深入分析离散数学在计算机科学中的关键作用和具体案例。",
        },
        // ... 其他讨论贴数据
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
      selectedTag: null,
      selectedTimeRange: null,
      dialog: false,
      selectedDiscussion: {},
    };
  },
  mounted() {
    const title = "讨论区";
    this.setAppTitle(title);
    this.setPageTitle(title);
  },
  computed: {
    filteredDiscussions() {
      let filtered = this.discussions;

      // 按标签筛选
      if (this.selectedTag) {
        filtered = filtered.filter((d) => d.tag === this.selectedTag);
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
            (d) => new Date(d.publishTime) >= fromDate
          );
        }
      }

      return filtered;
    },
  },
  methods: {
    // 映射 Vuex 的 mutation
    ...mapMutations(["setAppTitle", "setPageTitle"]),

    formatDate(dateStr) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(dateStr).toLocaleDateString(undefined, options);
    },
    openDialog(discussion) {
      this.selectedDiscussion = discussion;
      this.dialog = true;
    },
    toggleTag(tag) {
      if (this.selectedTag === tag) {
        this.selectedTag = null;
      } else {
        this.selectedTag = tag;
      }
    },
    toggleTimeRange(range) {
      if (this.selectedTimeRange === range) {
        this.selectedTimeRange = null;
      } else {
        this.selectedTimeRange = range;
      }
    },
    viewDiscussion(discussion) {
      // 导航到讨论贴详情页，例如 /discussion/1
      this.$router.push(`/discussion/${discussion.id}`);
    },
  },
};
</script>

<style scoped>
/* 全局设置 box-sizing */
* {
  box-sizing: border-box;
}

.discussion-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.filter-container {
  flex-shrink: 0;
}

/* 减少过滤卡片的垂直高度 */
.filter-card {
  margin-bottom: 4px;
}

.filter-card .v-card-text {
  padding-top: 4px !important;
  padding-bottom: 4px !important;
}

/* 调整过滤部分的内边距 */
.filter-section {
  margin-bottom: 0.1rem;
}

/* 滚动容器 */
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

/* 其他样式 */
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

.pa-2 {
  padding: 0.5rem !important;
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

.view-button {
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
  .v-col.pa-2 {
    padding-left: 8px !important;
    padding-right: 8px !important;
  }
}
</style>

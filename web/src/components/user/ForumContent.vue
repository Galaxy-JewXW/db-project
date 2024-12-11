<template>
  <v-container fluid class="discussion-container">
    <!-- Filter Section -->
    <div class="filter-container">
      <v-card class="filter-card" flat elevation="0">
        <v-card-text class="py-2">
          <v-row>
            <!-- 标签筛选 -->
            <v-col cols="12" class="filter-section pa-0">
              <div class="filter-group">
                <span class="filter-label">按标签筛选:</span>
                <v-chip v-for="tag in subjects" :key="tag" class="ma-2" color="primary" variant="outlined"
                  :class="{ 'selected-chip': selectedTag === tag }" @click="toggleTag(tag)">
                  {{ tag }}
                  <v-icon v-if="selectedTag === tag" class="ml-2" small>
                    mdi-check
                  </v-icon>
                </v-chip>
              </div>
            </v-col>

            <!-- 时间筛选 -->
            <v-col cols="12" class="filter-section pa-0">
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
            <v-col cols="12" class="filter-section pa-0">
              <v-row>
                <v-col cols="auto">
                  <v-checkbox label="只查看精华帖" density="compact" v-model="onlyMarked"></v-checkbox>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </div>

    <!-- 总数显示 -->
    <div class="total-count pl-2">
      共 {{ filteredDiscussions.length }} 个满足条件的讨论贴
    </div>

    <!-- Scroll Container -->
    <div class="scroll-container">
      <template v-if="filteredDiscussions.length > 0">
        <!-- 讨论贴列表 -->
        <v-list dense density="compact">
          <template v-for="(discussion, index) in filteredDiscussions" :key="discussion.id">
            <v-list-item :prepend-avatar="discussion.avatar" @click="openDiscussion(discussion)">
              <v-list-item-title class="text-subtitle-1 font-weight-bold">
                <v-row align="center">
                  <v-col cols="auto">
                    {{ discussion.title }}
                  </v-col>
                  <v-col cols="auto" class="text-body-2">
                    @ {{ discussion.publisher }} 发布于
                    {{ formatDate(discussion.publishTime) }}
                  </v-col>
                </v-row>
              </v-list-item-title>
              <v-list-item-subtitle>
                <div class="info-row">
                  <v-chip size="small" class="ma-1" variant="outlined" color="primary" label>
                    {{ discussion.tag }}
                  </v-chip>
                  <v-chip v-if="discussion.isMarked" size="small" class="ma-1" color="orange" label>
                    精华
                  </v-chip>
                  {{
                    discussion.summary.length > 60
                      ? discussion.summary.slice(0, 60) + "..."
                      : discussion.summary
                  }}
                </div>
              </v-list-item-subtitle>

              <template v-slot:append>
                {{ formatLastUpdated(discussion.lastUpdated) }}
              </template>
            </v-list-item>
            <!-- 添加分割线，每个item后面 -->
            <v-divider v-if="index < filteredDiscussions.length - 1" />
          </template>
        </v-list>
      </template>

      <!-- 无结果提示 -->
      <div v-else class="no-results">没有满足条件的讨论贴</div>
    </div>
  </v-container>
  <v-btn class="floating-btn" fab color="primary" @click="openNewPost()">
    <v-icon size="32">mdi-plus</v-icon>
  </v-btn>
</template>

<script>
import { mapMutations } from "vuex";
import axios from 'axios';
export default {
  name: "DiscussionArea",
  data() {
    return {
      discussions: [],
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
      selectedDiscussion: {},
      onlyMarked: false,
    };
  },
  mounted() {
    const title = "讨论区";
    this.setAppTitle(title);
    this.setPageTitle(title);
    this.getAllDiscussions();
  },
  computed: {
    filteredDiscussions() {
      let filtered = this.discussions;

      if (this.onlyMarked) {
        filtered = filtered.filter((d) => d.isMarked);
      }

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

      // 按 lastUpdated 排序，最近更新的排在前面
      filtered = filtered.sort((a, b) => {
        const dateA = new Date(a.lastUpdated);
        const dateB = new Date(b.lastUpdated);
        return dateB - dateA; // 返回负数表示 a 排在前面，正数表示 b 排在前面
      });
      return filtered;
    },
  },
  methods: {
    ...mapMutations(["setAppTitle", "setPageTitle"]),
    async getAllDiscussions() {
      try {
        const requestData = {
          tag: this.tag,         // 当前选择的标签
          time_range: this.timeRange,  // 当前选择的时间范围
        };
        const response = await axios.post('http://127.0.0.1:8000/api/discussions/get_all_discussions/', requestData, {
          headers: { 'Content-Type': 'application/json' }
        });

        if (response.data.success) {
          console.log(response.data.discussions)
          this.discussions = response.data.discussions;
        }

      } catch (error) {
        console.error('请求失败:', error);
      }
    },

    // 选择标签时重新获取数据
    onTagChange(newTag) {
      this.tag = newTag;
      this.getAllDiscussions();  // 更新讨论数据
    },

    // 选择时间范围时重新获取数据
    onTimeRangeChange(newTimeRange) {
      this.timeRange = newTimeRange;
      this.getAllDiscussions();  // 更新讨论数据
    },
    formatDate(dateStr) {
      const options = { year: "numeric", month: '2-digit', day: '2-digit' };
      return new Date(dateStr).toLocaleDateString(undefined, options);
    },
    formatLastUpdated(dateString) {
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
    openDiscussion(discussion) {
      this.$router.push(`/discussion/${discussion.id}`);
    },
    openNewPost() {
      this.$router.push(`/discussion/new`);
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
  },
};
</script>

<style scoped>
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

.filter-card {
  margin-bottom: 4px;
}

.filter-card .v-card-text {
  padding-top: 4px !important;
  padding-bottom: 4px !important;
}

.filter-section {
  margin-bottom: 0.1rem;
}

.scroll-container {
  flex: 1 1 auto;
  overflow-y: auto;
  padding: 16px;
  padding-bottom: 80px;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scroll-container::-webkit-scrollbar {
  display: none;
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

.filter-card .v-chip {
  margin: 1px;
  border: 1px solid #1867c0;
  cursor: pointer;
  color: #1867c0;
}

.filter-card .selected-chip {
  background-color: #1867c0 !important;
  color: white !important;
}

.filter-card .selected-chip .v-icon {
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
  font-weight: bold;
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

.floating-btn {
  position: fixed;
  right: 4%;
  bottom: 10%;
  z-index: 9999;
  border-radius: 75%;
  width: 64px;
  height: 64px;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
}

.v-icon {
  color: white;
}
</style>

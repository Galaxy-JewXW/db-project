<template>
  <div v-if="loading">
    <v-skeleton-loader
      class="mx-auto main-card"
      max-width="100%"
      type="list-item-avatar-three-line, list-item-avatar-three-line, list-item-avatar-three-line"
    ></v-skeleton-loader>
  </div>
  <div v-else>
    <v-container>
      <v-row>
        <!-- 左侧公告列表和消息 -->
        <v-col
          cols="12"
          md="4"
          style="
            display: flex;
            flex-direction: column;
            height: calc(100vh - 85px);
          "
        >
          <!-- 公告列表 -->
          <v-card
            class="mb-4"
            outlined
            style="
              flex: 1;
              overflow-y: auto;
              display: flex;
              flex-direction: column;
            "
          >
            <v-card-title
              class="headline text-h5 sticky-title font-weight-bold"
            >
              公告列表
            </v-card-title>
            <v-divider></v-divider>
            <v-list lines="two" style="flex: 1" class="no-scrollbar">
              <template v-for="(group, index) in groupedNotices" :key="index">
                <v-list-subheader>
                  {{ group.label }}
                </v-list-subheader>
                <v-divider></v-divider>
                <v-list-item
                  v-for="notice in group.notices"
                  :key="notice.id"
                  @click="openDialog(notice)"
                  ripple
                  class="notice-item"
                >
                  <v-list-item-title class="font-weight-medium notice-title">
                    {{ notice.title }}
                  </v-list-item-title>
                  <v-list-item-subtitle class="notice-subtitle">
                    <span class="notice-publisher">{{ notice.publisher }}</span>
                    |
                    <span class="notice-time">{{
                      formatDate(notice.releaseTime)
                    }}</span>
                  </v-list-item-subtitle>
                </v-list-item>
                <v-divider v-if="group.notices.length > 1"></v-divider>
              </template>
            </v-list>
          </v-card>
        </v-col>
        <!-- 右侧雷达图和推荐练习 -->
        <v-col
          cols="12"
          md="8"
          style="
            display: flex;
            flex-direction: column;
            height: calc(100vh - 85px);
          "
        >
          <!-- 当前进度 -->
          <v-card
            class="mb-4 no-scrollbar"
            outlined
            style="
              flex: 0 0 auto;
              display: flex;
              flex-direction: column;
              overflow-y: auto;
            "
          >
            <div class="sticky-title">
              <v-card-title class="headline text-h5 font-weight-bold">
                当前进度
              </v-card-title>
              <v-divider></v-divider>
            </div>
            <!-- 进度雷达图 -->
            <div
              style="
                display: flex;
                flex-direction: row;
                align-items: flex-start;
                padding: 16px;
              "
            >
              <v-col cols="12" md="6">
                <div id="chart1"></div>
              </v-col>
              <v-col cols="12" md="6">
                <div
                  v-for="(item, index) in radarData"
                  :key="index"
                  style="margin-bottom: 12px"
                >
                  <div class="right-content-title">
                    {{ item.subject }}
                  </div>
                  <div>
                    <span class="large-number">{{ item.doneQuestions }}</span> /
                    <span class="medium-number">{{ item.totalQuestions }}</span>
                    -
                    <span class="font-weight-bold text-h6"
                      >{{ calculatePercentage(item) }}%</span
                    >
                  </div>
                </div>
              </v-col>
            </div>
          </v-card>

          <!-- 推荐练习 -->
          <v-card
            class="mb-4 no-scrollbar"
            outlined
            style="
              flex: 1;
              overflow-y: auto;
              display: flex;
              flex-direction: column;
            "
          >
            <div class="sticky-title">
              <v-card-title class="headline text-h5 font-weight-bold">
                推荐练习
              </v-card-title>
              <v-divider></v-divider>
            </div>
            <!-- 推荐练习内容 -->
            <div style="flex: 1; padding: 16px">
              <div class="recommended-exercises">
                <v-btn
                  v-for="exercise in recommendedExercises"
                  :key="exercise"
                  class="exercise-button text-none"
                  :style="{ backgroundColor: '#0D47A1', color: 'white' }"
                  rounded="0"
                  @click="goToExercise(exercise)"
                >
                  <v-responsive class="text-truncate">{{
                    exercise
                  }}</v-responsive>
                </v-btn>
              </div>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- 公告详情对话框 -->
    <v-dialog v-model="dialogVisible" max-width="60%">
      <v-card>
        <v-card-title class="dialog-title">{{
          selectedNotice.title
        }}</v-card-title>
        <v-card-subtitle class="dialog-subtitle">
          发布者：{{ selectedNotice.publisher }} &nbsp; 发布时间：{{
            formatDate(selectedNotice.releaseTime)
          }}
        </v-card-subtitle>
        <v-card-text>
          <v-md-preview :text="selectedNotice.content"></v-md-preview>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="closeDialog">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from "axios";
import { mapMutations } from "vuex";
import store from "@/store";
import ApexCharts from "apexcharts";

export default {
  name: "ForumContent",
  data() {
    return {
      notices: [
        {
          id: 1,
          title: "关于2024年春季学期开学的通知",
          publisher: "教务处",
          releaseTime: "2024-02-20T08:00:00",
          content:
            "各位同学，2024年春季学期将于2月20日正式开学，请提前做好返校准备。",
        },
        {
          id: 2,
          title: "国庆节放假安排",
          publisher: "校办",
          releaseTime: "2023-10-01T09:00:00",
          content: "根据国家规定，国庆节放假时间为10月1日至10月7日，共7天。",
        },
        // 更多公告数据
        {
          id: 3,
          title: "校园网络维护通知",
          publisher: "网络中心",
          releaseTime: "2023-10-12T00:00:00",
          content: "因设备升级，10月12日0:00-6:00校园网络将暂停服务。",
        },
      ],
      messages: [
        {
          id: 1,
          sender: "系统通知",
          sendTime: "2023-10-16T08:00:00",
          content: "您的密码即将过期，请及时更新。",
          avatar: "https://picsum.photos/250/300?image=660",
        },
        {
          id: 2,
          sender: "张老师",
          sendTime: "2023-10-15T17:45:00",
          content: "请注意，明天的课程时间有调整。",
          avatar: "https://picsum.photos/250/300?image=821",
        },
        // 更多消息数据
        {
          id: 3,
          sender: "李同学",
          sendTime: "2023-10-14T12:30:00",
          content: "请问你有上次课的笔记吗？",
          avatar: "https://picsum.photos/250/300?image=883",
        },
      ],
      dialogVisible: false,
      selectedNotice: {},
      radarData: [
        {
          subject: "工科数学分析（上）",
          doneQuestions: 87,
          totalQuestions: 692,
        },
        {
          subject: "工科数学分析（下）",
          doneQuestions: 78,
          totalQuestions: 472,
        },
        {
          subject: "工科高等代数",
          doneQuestions: 61,
          totalQuestions: 561,
        },
        {
          subject: "离散数学（信息类）",
          doneQuestions: 21,
          totalQuestions: 394,
        },
        {
          subject: "基础物理学A",
          doneQuestions: 8,
          totalQuestions: 721,
        },
      ],
      // 推荐练习数组
      recommendedExercises: [1, 2, 3, 4, 5, 6, 7],
      loading: true,
    };
  },
  computed: {
    groupedNotices() {
      const grouped = {};

      this.notices.forEach((notice) => {
        const timeLabel = this.getTimeGroup(notice.releaseTime);
        if (!grouped[timeLabel]) {
          grouped[timeLabel] = [];
        }
        grouped[timeLabel].push(notice);
      });

      return Object.keys(grouped)
        .map((label) => ({
          label,
          notices: grouped[label].sort(
            (a, b) => new Date(b.releaseTime) - new Date(a.releaseTime)
          ),
        }))
        .sort(
          (a, b) =>
            new Date(b.notices[0].releaseTime) -
            new Date(a.notices[0].releaseTime)
        );
    },
    groupedMessages() {
      const grouped = {};

      this.messages.forEach((message) => {
        const timeLabel = this.getTimeGroup(message.sendTime);
        if (!grouped[timeLabel]) {
          grouped[timeLabel] = {
            label: timeLabel,
            messages: [],
          };
        }
        grouped[timeLabel].messages.push(message);
      });

      return Object.values(grouped)
        .map((group) => ({
          ...group,
          messages: group.messages.sort(
            (a, b) => new Date(b.sendTime) - new Date(a.sendTime)
          ),
        }))
        .sort(
          (a, b) =>
            new Date(b.messages[0].sendTime) - new Date(a.messages[0].sendTime)
        );
    },
  },
  methods: {
    async fetchHomeData() {
      try {
        const requestData = {
          user_id: store.getters.getUserId, // 假设你已经知道用户的ID，替换为实际值
        };
        const response = await axios.post(
          "http://127.0.0.1:8000/api/board/",
          requestData,
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log(response);

        const backendNotices = response.data.data.notices;
        const messages_data = response.data.data.messages;
        const progress = response.data.data.progress;
        this.recommendedExercises = response.data.data.recommendedExercises;

        this.notices = backendNotices.map((notice) => ({
          id: notice.id,
          title: notice.title,
          publisher: notice.sender,
          releaseTime: notice.sent_at,
          content: notice.content,
        }));
        this.messages = messages_data.map((m) => ({
          id: m.id,
          sender: m.sender,
          sendTime: m.sent_at,
          content: m.content,
          avatar: m.sender_avatar,
        }));

        const parseProgressData = (progressData) => {
          const radarData = [];
          for (const subjectDisplay in progressData) {
            const data = progressData[subjectDisplay];
            radarData.push({
              subject: data.subject,
              doneQuestions: data.user_question_count,
              totalQuestions: data.total_question_count,
            });
          }
          return radarData;
        };

        this.radarData = parseProgressData(progress);

        // 设置 loading 为 false 后，使用 $nextTick 确保 DOM 已更新
        this.loading = false;
        this.$nextTick(() => {
          this.initApexChart();
        });
      } catch (error) {
        console.error("Error fetching messages:", error);
      }
    },
    ...mapMutations(["setAppTitle", "setPageTitle"]),
    openDialog(notice) {
      this.selectedNotice = notice;
      this.dialogVisible = true;
    },
    closeDialog() {
      this.dialogVisible = false;
    },
    getTimeGroup(date) {
      const today = new Date();
      const targetDate = new Date(date);
      const diffTime = today - targetDate;
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

      if (diffDays === 0) return "今天";
      if (diffDays === 1) return "昨天";
      if (diffDays === 2) return "前天";
      if (diffDays < 7) return `${diffDays}天前`;
      if (diffDays < 30) return `${Math.floor(diffDays / 7)}周前`;
      if (diffDays < 365) return `${Math.floor(diffDays / 30)}个月前`;
      return `${Math.floor(diffDays / 365)}年前`;
    },
    getMessagePreview(content) {
      const maxLength = 50;
      if (content.length <= maxLength) {
        return content;
      }
      return content.substring(0, maxLength) + "...";
    },
    calculatePercentage(item) {
      const ratio =
        item.totalQuestions === 0
          ? 0
          : (item.doneQuestions / item.totalQuestions) * 100;
      return ratio.toFixed(2);
    },
    goToExercise(exerciseId) {
      console.log(`Navigate to exercise ID: ${exerciseId}`);
      this.$router.push(`/exercise/${exerciseId}`);
    },
    formatDate(dateString) {
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
    initApexChart() {
      // 当 radarData 准备好后再计算并初始化图表
      const seriesData = this.radarData.map((item) => {
        const ratio =
          item.totalQuestions === 0
            ? 0
            : (item.doneQuestions / item.totalQuestions) * 100;
        return ratio.toFixed(2);
      });

      const labelsData = this.radarData.map((item) => item.subject);

      // 计算总的完成比例
      const totalDone = this.radarData.reduce(
        (sum, item) => sum + item.doneQuestions,
        0
      );
      const totalQuestions = this.radarData.reduce(
        (sum, item) => sum + item.totalQuestions,
        0
      );
      const totalRatio =
        totalQuestions === 0
          ? 0
          : ((totalDone / totalQuestions) * 100).toFixed(2);

      var options1 = {
        chart: {
          height: 280,
          type: "radialBar",
        },
        series: seriesData,
        labels: labelsData,
        plotOptions: {
          radialBar: {
            dataLabels: {
              total: {
                show: true,
                label: "总进度",
                formatter: function () {
                  return totalRatio + "%";
                },
              },
            },
          },
        },
      };
      // 每次重新初始化图表前，确保销毁旧图表，以防叠加
      const chartContainer = document.querySelector("#chart1");
      chartContainer.innerHTML = "";
      new ApexCharts(chartContainer, options1).render();
    },
  },
  mounted() {
    this.loading = true;
    const title = "主页";
    this.setAppTitle(title);
    this.setPageTitle(title);
    this.fetchHomeData();
  },
};
</script>

<style scoped>
#chart1 {
  width: 70%;
  margin: auto;
}

.sticky-title {
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: white;
}

.no-scrollbar {
  scrollbar-width: none;
  /* Firefox */
  -ms-overflow-style: none;
  /* IE and Edge */
}

.no-scrollbar::-webkit-scrollbar {
  width: 0;
  height: 0;
}

/* 公告列表样式 */
.notice-title {
  font-size: 1.35rem;
  /* 增大字体 */
  margin-bottom: 4px;
}

.notice-subtitle {
  font-size: 1.1rem;
  /* 增大字体 */
  color: rgba(0, 0, 0, 0.6);
}

.notice-publisher {
  font-size: 1.1rem;
  /* 增大字体 */
}

.notice-time {
  font-size: 1rem;
  /* 保持时间字体大小不变 */
  color: rgba(0, 0, 0, 0.6);
}

.notice-item {
  padding: 4px 0;
}

.notice-item:hover {
  background-color: #f5f5f5;
  cursor: pointer;
}

/* 消息通知列表样式 */
.v-list-item {
  cursor: pointer;
}

.v-list-item:hover {
  background-color: #f5f5f5;
}

.message-sender {
  font-size: 1rem;
  /* 增大字体 */
  font-weight: bold;
}

.message-time {
  font-size: 0.75rem;
  /* 保持时间字体大小不变 */
  color: rgba(0, 0, 0, 0.6);
}

.message-content {
  font-size: 0.9rem;
  /* 增大字体 */
  color: rgba(0, 0, 0, 0.87);
}

.v-divider {
  margin: 0;
}

.dialog-title {
  font-size: 1.5rem;
}

.dialog-subtitle {
  font-size: 1rem;
  color: rgba(0, 0, 0, 0.6);
}

/* 右侧内容区域样式 */
.right-content-title {
  font-weight: bolder;
  font-size: 12px;
  /* 调小字号 */
  color: gray;
}

.large-number {
  font-size: 26px;
  /* 放大前面的数字 */
  font-weight: bold;
}

.medium-number {
  font-size: 12px;
  /* 稍微放大后面的数字 */
  font-weight: medium;
}

/* 推荐练习按钮样式 */
.recommended-exercises {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.exercise-button {
  width: 60px;
  height: 60px;
  font-size: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  border-radius: 0;
  overflow-wrap: break-word;
  word-wrap: break-word;
  color: white !important;
}

.v-responsive {
  max-width: 100%;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  font-size: 14px;
}
</style>

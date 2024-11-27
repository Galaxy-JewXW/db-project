<template>
  <div>
    <v-container>
      <v-row>
        <!-- 左侧公告列表和消息 -->
        <v-col cols="12" md="4" style="
            display: flex;
            flex-direction: column;
            height: calc(100vh - 85px);
          ">
          <!-- 公告列表 -->
          <v-card class="mb-4" outlined style="
              flex: 1;
              overflow-y: auto;
              display: flex;
              flex-direction: column;
            ">
            <v-card-title class="headline text-h5 sticky-title font-weight-bold">
              公告列表
            </v-card-title>
            <v-divider></v-divider>
            <v-list lines="two" style="flex: 1" class="no-scrollbar">
              <template v-for="(group, index) in groupedNotices" :key="index">
                <v-list-subheader>
                  {{ group.label }}
                </v-list-subheader>
                <v-divider></v-divider>
                <v-list-item v-for="notice in group.notices" :key="notice.id" @click="openDialog(notice)" ripple
                  class="notice-item">
                  <v-list-item-title class="font-weight-medium notice-title">
                    {{ notice.title }}
                  </v-list-item-title>
                  <v-list-item-subtitle class="notice-subtitle">
                    <span class="notice-publisher">{{ notice.publisher }}</span>
                    |
                    <span class="notice-time">{{ formatDate(notice.releaseTime) }}</span>
                  </v-list-item-subtitle>
                </v-list-item>
                <v-divider v-if="group.notices.length > 1"></v-divider>
              </template>
            </v-list>
          </v-card>
          <!-- 消息列表 -->
          <v-card class="mb-4" outlined style="
              flex: 1;
              overflow-y: auto;
              display: flex;
              flex-direction: column;
            ">
            <v-card-title class="headline text-h5 sticky-title font-weight-bold">
              消息列表
            </v-card-title>
            <v-divider></v-divider>
            <v-list lines="two" style="flex: 1" class="no-scrollbar">
              <template v-for="(group, index) in groupedMessages" :key="index">
                <v-list-subheader>
                  {{ group.label }}
                </v-list-subheader>
                <v-divider></v-divider>
                <v-list-item v-for="message in group.messages" :key="message.id" :prepend-avatar="message.avatar"
                  @click="openMessageDialog(message)" ripple>
                  <template v-slot:title>
                    <div>
                      <span class="font-weight-bold message-sender">
                        {{ message.sender }}
                      </span>
                      <span class="message-time">
                        &nbsp;{{ formatDate(message.sendTime) }}
                      </span>
                    </div>
                  </template>
                  <template v-slot:subtitle>
                    <div class="message-content">
                      {{ getMessagePreview(message.content) }}
                    </div>
                  </template>
                </v-list-item>
              </template>
            </v-list>
          </v-card>
        </v-col>
        <!-- 右侧雷达图和推荐练习 -->
        <v-col cols="12" md="8" style="
            display: flex;
            flex-direction: column;
            height: calc(100vh - 85px);
          ">
          <!-- 当前进度 -->
          <v-card class="mb-4 no-scrollbar" outlined style="
              flex: 0 0 auto;
              display: flex;
              flex-direction: column;
              overflow-y: auto;
            ">
            <div class="sticky-title">
              <v-card-title class="headline text-h5 font-weight-bold">
                当前进度
              </v-card-title>
              <v-divider></v-divider>
            </div>
            <!-- 进度雷达图 -->
            <div style="
                display: flex;
                flex-direction: row;
                align-items: flex-start;
                padding: 16px;
              ">
              <!-- 雷达图 -->
              <div ref="radarChart" style="width: 400px; height: 300px"></div>
              <!-- 右侧内容区域 -->
              <div style="padding-left: 16px">
                <div v-for="(item, index) in radarData" :key="index" style="margin-bottom: 12px">
                  <div class="right-content-title">
                    {{ item.subject }}
                  </div>
                  <div>
                    <span class="large-number">{{ item.doneQuestions }}</span> /
                    <span class="medium-number">{{ item.totalQuestions }}</span>
                    - <span class="font-weight-bold text-h6">{{ calculatePercentage(item) }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </v-card>

          <!-- 推荐练习 -->
          <v-card class="mb-4 no-scrollbar" outlined style="
              flex: 1;
              overflow-y: auto;
              display: flex;
              flex-direction: column;
            ">
            <div class="sticky-title">
              <v-card-title class="headline text-h5 font-weight-bold">
                推荐练习
              </v-card-title>
              <v-divider></v-divider>
            </div>
            <!-- 推荐练习内容 -->
            <div style="flex: 1; padding: 16px">
              <div class="recommended-exercises">
                <v-btn v-for="exercise in recommendedExercises" :key="exercise" class="exercise-button text-none"
                  :style="{ backgroundColor: '#0D47A1', color: 'white' }" rounded="0" @click="goToExercise(exercise)">
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

    <!-- 消息详情对话框 -->
    <v-dialog v-model="messageDialogVisible" max-width="60%">
      <v-card>
        <v-card-title class="dialog-title">消息</v-card-title>
        <v-card-subtitle class="dialog-subtitle">
          发件人：{{ selectedMessage.sender }} &nbsp; 发送时间：{{
            formatDate(selectedMessage.sendTime)
          }}
        </v-card-subtitle>
        <v-card-text>
          <v-md-preview :text="selectedMessage.content"></v-md-preview>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="closeMessageDialog">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import { mapMutations } from "vuex";
import * as echarts from "echarts";

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
      messageDialogVisible: false,
      selectedNotice: {},
      selectedMessage: {},
      radarChart: null,
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
    ...mapMutations(["setAppTitle", "setPageTitle"]),
     async fetchHomeData() {
      try {
        // 确保请求路径和后端路由匹配
        const response = await axios.post('http://127.0.0.1:8000/api/board/', {
          user_id: 1, // 示例用户 ID
        }, {
          headers: {
            'Content-Type': 'application/json', // 设置请求头
          },
        });

        // 检查响应并更新数据
        if (response.status === 200) {
          this.messages = response.data.messages || [];
        } else {
          console.error('Unexpected response:', response);
        }
      } catch (error) {
        console.error('Error fetching messages:', error);
      }
    },
    openDialog(notice) {
      this.selectedNotice = notice;
      this.dialogVisible = true;
    },
    closeDialog() {
      this.dialogVisible = false;
    },
    openMessageDialog(message) {
      this.selectedMessage = message;
      this.messageDialogVisible = true;
    },
    closeMessageDialog() {
      this.messageDialogVisible = false;
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
      if (item.totalQuestions === 0) return 0;
      return ((item.doneQuestions / item.totalQuestions) * 100).toFixed(2);
    },
    initRadarChart() {
      // 初始化 ECharts 实例
      this.radarChart = echarts.init(this.$refs.radarChart);

      // 计算百分比数据
      const percentages = this.radarData.map((item) => {
        if (item.totalQuestions === 0) return 0;
        return (item.doneQuestions / item.totalQuestions) * 100;
      });

      // 为了在 formatter 中访问 radarData，将其赋值给局部变量
      const radarData = this.radarData;

      // 配置选项
      const option = {
        tooltip: {
          formatter: function (params) {
            let res = params.seriesName + "<br/>";
            for (let i = 0; i < params.value.length; i++) {
              let indicatorName = radarData[i].subject;
              let value = params.value[i].toFixed(2) + "%";
              res += indicatorName + "：" + value + "<br/>";
            }
            return res;
          },
        },
        radar: {
          indicator: this.radarData.map((item) => ({
            name: item.subject,
            max: 100,
          })),
          radius: "40%", // 调整雷达图大小
          center: ["50%", "50%"], // 居中显示
          name: {
            textStyle: {
              fontSize: 12, // 调整字体大小
              width: 40, // 设置文字宽度，根据需要调整
              overflow: "breakAll", // 自动换行
              lineHeight: 16, // 调整行高
            },
          },
        },
        series: [
          {
            name: "做题进度",
            type: "radar",
            data: [
              {
                value: percentages,
                name: "当前进度",
                areaStyle: {
                  color: "rgba(0, 128, 255, 0.3)",
                },
                lineStyle: {
                  color: "rgba(0, 128, 255, 0.5)",
                },
                symbol: "circle",
                symbolSize: 5,
                itemStyle: {
                  color: "rgba(0, 128, 255, 0.8)",
                },
              },
            ],
          },
        ],
      };

      // 设置选项
      this.radarChart.setOption(option);

      // 监听窗口大小变化，自动调整图表大小
      window.addEventListener("resize", this.handleResize);
    },

    handleResize() {
      if (this.radarChart) {
        this.radarChart.resize();
      }
    },
    goToExercise(exerciseId) {
      console.log(`Navigate to exercise ID: ${exerciseId}`);
      this.$router.push(`/exercise/${exerciseId}`);
    },
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
  },
  mounted() {
    const title = "主页";
    this.setAppTitle(title);
    this.setPageTitle(title);
    this.fetchHomeData();
    // 初始化雷达图
    this.initRadarChart();
  },
  beforeDestroy() {
    // 销毁图表实例，清理事件监听器
    if (this.radarChart) {
      this.radarChart.dispose();
    }
    window.removeEventListener("resize", this.handleResize);
  },
};
</script>

<style scoped>
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

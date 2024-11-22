<template>
    <v-banner
      sticky
      icon="mdi-plus"
      lines="one"
    >
      <template v-slot:text>
        <div class="text-subtitle-1">作为辅导师，你可发布新的通知。</div>
      </template>

      <template v-slot:actions>
        <v-btn color="primary" class="mr-5" @click="postNewNoti()">
            <div class="text-subtitle-1">发布新通知</div>
        </v-btn>
      </template>
    </v-banner>
    <v-container class="scroll-container">
        <v-row>
            <v-col v-for="notice in notices" :key="notice.id" cols="12">
                <v-card>
                    <v-card-title>
                        <div>
                            <div class="notice-title">{{ notice.title }}</div>
                            <div class="notice-subtitle">{{ notice.publisher }}&nbsp;&nbsp;{{
                                formatDate(notice.releaseTime) }}
                            </div>
                        </div>
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text>
                        <v-md-preview :text="notice.content"></v-md-preview>
                    </v-card-text>
                    <v-divider></v-divider>
                    <v-row no-gutters>
                        <v-col cols="auto">
                            <v-btn rounded="0" variant="text" :color="'#1867c0'">
                                <v-icon left>mdi-pencil</v-icon>
                                编辑
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { mapMutations } from 'vuex';

export default {
    name: 'AdminBoard',
    data() {
        return {
            notices: [
                {
                    id: 1,
                    title: "关于2024年春季学期开学的通知",
                    publisher: "教务处",
                    releaseTime: "2023-10-15T19:00:09",
                    content:
                        "# 草四你 \n  各位同学，2024年春季学期将于2月20日正式开学，请提前做好返校准备。",
                },
                {
                    id: 2,
                    title: "国庆节放假安排",
                    publisher: "校办",
                    releaseTime: "2023-09-28T19:00:09",
                    content: "根据国家规定，国庆节放假时间为10月1日至10月7日，共7天。",
                },
                {
                    id: 3,
                    title: "校园网络维护通知",
                    publisher: "网络中心",
                    releaseTime: "2023-10-10T19:00:09",
                    content: "因设备升级，10月12日0:00-6:00校园网络将暂停服务。",
                },
                {
                    id: 4,
                    title: "校园网络维护通知",
                    publisher: "网络中心",
                    releaseTime: "2023-10-12T19:00:09",
                    content: "因设备升级，10月13日0:00-6:00校园网络将暂停服务。",
                },
                {
                    id: 5,
                    title: "校园网络维护通知",
                    publisher: "网络中心",
                    releaseTime: "2023-10-08T19:00:09",
                    content: "因设备升级，10月9日0:00-6:00校园网络将暂停服务。",
                },
            ],
        };
    },
    mounted() {
        // 更新标题
        const title = '主页';
        this.setAppTitle(title);
        this.setPageTitle(title);

        // 按发布时间对 notices 进行排序，越新的排在最前面
        this.notices.sort((a, b) => new Date(b.releaseTime) - new Date(a.releaseTime));
    },
    methods: {
        ...mapMutations(['setAppTitle', 'setPageTitle']),

        // 格式化日期
        formatDate(dateString) {
            const date = new Date(dateString);
            const options = {
                year: 'numeric',
                month: 'numeric',
                day: 'numeric',
                hour: 'numeric',
                minute: 'numeric',
                second: 'numeric',
                hour12: false, // 使用24小时制
            };
            return new Intl.DateTimeFormat('zh-CN', options).format(date);
        },
        postNewNoti() {
            this.$router.push("/admin/new-notification");
        }
    },
};
</script>

<style scoped>
.scroll-container {
    flex-direction: column;
    flex: 1 1 auto;
    overflow-y: auto;
    padding: 16px;
    padding-bottom: 80px;
    height: 90vh;
    max-height: 90vh;
    -ms-overflow-style: none;
    scrollbar-width: none;
}

.scroll-container::-webkit-scrollbar {
    display: none;
}

/* 公告列表样式 */
.notice-title {
    font-size: 1.35rem;
    /* 增大字体 */
    margin-bottom: 4px;
}

.notice-subtitle {
    font-size: 1.0rem;
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

</style>

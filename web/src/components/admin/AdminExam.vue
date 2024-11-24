<template>
    <v-banner sticky icon="mdi-plus" lines="one">
        <template v-slot:text>
            <div class="text-subtitle-1">作为辅导师，你可创建新的模拟测试。</div>
        </template>

        <template v-slot:actions>
            <v-btn color="primary" class="mr-5">
                <div class="text-subtitle-1">创建模拟测试</div>
            </v-btn>
        </template>
    </v-banner>
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
                            <v-btn color="primary" text>编辑测试</v-btn>
                            <v-btn color="red" text>删除测试</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </template>
        <div v-else class="no-results">没有测试</div>
    </div>
</template>

<script>
import { mapMutations } from "vuex";

export default {
    name: "ProblemSet",
    data() {
        return {
            ongoingExams: [
                {
                    id: 1,
                    name: "2023-24数分上期中 a",
                    createdAt: "2024-09-02 09:00:00",
                    subject: "工科数学分析（上）",
                    starttime: "2024-11-13 19:00:00",
                    duration: 120,
                },
                {
                    id: 11,
                    name: "2023-24数分上期中",
                    createdAt: "2024-09-02 09:00:00",
                    subject: "工科数学分析（上）",
                    starttime: "2024-11-13 19:00:00",
                    duration: 120,
                },
            ],
            pastExams: [
                {
                    id: 3,
                    name: "2023-24数分上期末 a",
                    createdAt: "2024-01-15 09:00:00",
                    subject: "工科数学分析（上）",
                    starttime: "2024-01-15 09:00:00",
                    duration: 120,
                },
                {
                    id: 31,
                    name: "2023-24数分上期末",
                    createdAt: "2024-01-15 09:00:00",
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
                    createdAt: "2024-12-01 09:00:00",
                    subject: "工科数学分析（上）",
                    starttime: "2024-12-15 09:00:00",
                    duration: 120,
                },
                {
                    id: 21,
                    name: "2023-24数分期末模拟测试",
                    createdAt: "2024-12-01 09:00:00",
                    subject: "工科数学分析（上）",
                    starttime: "2024-12-15 09:00:00",
                    duration: 120,
                },
                // ... 其他即将到来的测试数据
            ],
        };
    },
    mounted() {
        const title = "模拟测试管理";
        this.setAppTitle(title);
        this.setPageTitle(title);
    },
    computed: {
        combinedExams() {
            return [...this.ongoingExams, ...this.comingExams];
        },
    },
    methods: {
        // 映射 Vuex 的 mutation
        ...mapMutations(['setAppTitle', 'setPageTitle']),
        formatDate(dateString) {
            const options = {
                year: 'numeric',
                month: 'numeric',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false,
            };
            const date = new Date(dateString);
            return date.toLocaleString("zh-CN", options).replace(/\//g, "-");
        },
    },
};
</script>

<style scoped>
/* Set box-sizing globally */
* {
    box-sizing: border-box;
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
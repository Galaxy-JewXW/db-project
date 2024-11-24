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
        <v-expansion-panels>
            <!-- Ongoing Exams -->
            <v-expansion-panel>
                <v-expansion-panel-title>进行中的测试</v-expansion-panel-title>
                <v-expansion-panel-text>

                    <v-row dense class="justify-start">
                        <v-col v-for="exam in paginatedExams(ongoingExams, ongoingPage)" :key="exam.id" cols="12" sm="6"
                            md="3" class="pa-1">
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
                    <v-pagination v-model="ongoingPage" :length="Math.ceil(ongoingExams.length / itemsPerPage)"
                        :total-visible="7" class="my-4"></v-pagination>
                </v-expansion-panel-text>
            </v-expansion-panel>

            <!-- Coming Exams -->
            <v-expansion-panel>
                <v-expansion-panel-title>即将进行的测试</v-expansion-panel-title>
                <v-expansion-panel-text>
                    <v-row dense class="justify-start">
                        <v-col v-for="exam in paginatedExams(comingExams, comingPage)" :key="exam.id" cols="12" sm="6"
                            md="3" class="pa-1">
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
                    <v-pagination v-model="comingPage" :length="Math.ceil(comingExams.length / itemsPerPage)"
                        :total-visible="7" class="my-4"></v-pagination>
                </v-expansion-panel-text>
            </v-expansion-panel>

            <!-- Past Exams -->
            <v-expansion-panel>
                <v-expansion-panel-title>已结束的测试</v-expansion-panel-title>
                <v-expansion-panel-text>

                    <v-row dense class="justify-start">
                        <v-col v-for="exam in paginatedExams(pastExams, pastPage)" :key="exam.id" cols="12" sm="6"
                            md="3" class="pa-1">
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
                    <v-pagination v-model="pastPage" :length="Math.ceil(pastExams.length / itemsPerPage)"
                        :total-visible="7" class="my-4"></v-pagination>
                </v-expansion-panel-text>
            </v-expansion-panel>
        </v-expansion-panels>
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
            itemsPerPage: 4, // 每页显示的测试数量
            ongoingPage: 1,
            comingPage: 1,
            pastPage: 1,
        };
    },
    mounted() {
        const title = "模拟测试管理";
        this.setAppTitle(title);
        this.setPageTitle(title);
    },
    computed: {
        combinedExams() {
            return [...this.ongoingExams, ...this.comingExams, ...this.pastExams];
        },
    },
    methods: {
        ...mapMutations(["setAppTitle", "setPageTitle"]),
        formatDate(dateString) {
            const options = {
                year: "numeric",
                month: "numeric",
                day: "2-digit",
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
                hour12: false,
            };
            const date = new Date(dateString);
            return date.toLocaleString("zh-CN", options).replace(/\//g, "-");
        },
        paginatedExams(exams, page) {
            const start = (page - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return exams.slice(start, end);
        },
    },
};
</script>

<style scoped>
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
</style>

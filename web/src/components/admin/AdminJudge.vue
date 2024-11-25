<!-- components/ExamList.vue -->
<template>
    <v-container fluid class="problemset-container">
        <div class="scroll-container">
            <template v-if="paginatedExams.length > 0">
                <v-row dense class="justify-start">
                    <v-col v-for="exam in paginatedExams" :key="exam.id" cols="12" sm="6" md="3" class="pa-1">
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
                                <v-btn class="enter-button" @click="enterExam(exam)">进入批改</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-col>
                </v-row>

                <!-- Pagination Controls -->
                <v-row justify="center" class="mt-4">
                    <v-pagination v-model="currentPage" :length="totalPages" :total-visible="7"
                        @input="onPageChange"></v-pagination>
                </v-row>
            </template>
            <div v-else class="no-results">暂无批改任务</div>
        </div>
    </v-container>
</template>

<script>
import { mapMutations } from "vuex";

export default {
    name: "ExamList",
    data() {
        return {
            exams: [
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
                {
                    id: 2,
                    name: "2023-24物理期中 a",
                    createdAt: "2024-09-05 10:30:00",
                    subject: "工科物理",
                    starttime: "2024-11-15 09:00:00",
                    duration: 90,
                },
                {
                    id: 3,
                    name: "2023-24化学期中 a",
                    createdAt: "2024-09-10 14:20:00",
                    subject: "化学基础",
                    starttime: "2024-11-20 13:00:00",
                    duration: 60,
                },
                // ... more exams
            ],
            currentPage: 1,
            itemsPerPage: 8, // Number of exams per page
        };
    },
    computed: {
        totalPages() {
            return Math.ceil(this.exams.length / this.itemsPerPage);
        },
        paginatedExams() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.exams.slice(start, end);
        },
        combinedExams() {
            return [...this.ongoingExams, ...this.comingExams];
        },
    },
    mounted() {
        const title = "模拟测试评分";
        this.setAppTitle(title);
        this.setPageTitle(title);
    },
    methods: {
        // 映射 Vuex 的 mutation
        ...mapMutations(["setAppTitle", "setPageTitle"]),

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
            this.$router.push(`/admin/judge/${exam.id}`);
        },
        onPageChange(page) {
            this.currentPage = page;
            // Optionally, scroll to top when page changes
            this.$nextTick(() => {
                const container = this.$el.querySelector(".scroll-container");
                if (container) {
                    container.scrollTop = 0;
                }
            });
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

/* Pagination Styling */
.v-pagination {
    /* Center the pagination */
    display: flex;
    justify-content: center;
}
</style>

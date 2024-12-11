<!-- components/ExamList.vue -->
<template>
    <div v-if="loading" class="scroll-container">
        <v-skeleton-loader class="mx-auto main-card" max-width="100%"
            type="list-item-avatar-three-line, list-item-avatar-three-line, list-item-avatar-three-line"></v-skeleton-loader>
    </div>
    <div v-else>
        <v-banner sticky icon="mdi-plus" lines="one">
            <template v-slot:text>
                <div class="text-subtitle-1">作为辅导师，你可对模拟测试进行批改，或公布已完成批改的测试成绩。</div>
            </template>
        </v-banner>

        <!-- 筛选条件区域 -->
        <v-card variant="text" class="pb-2 pl-2 pr-2" title="筛选模拟测试" subtitle="通过名称搜索或选择科目进行筛选"
            prepend-icon="mdi-filter">
            <v-row align="center" justify="start" no-gutters>
                <v-col cols="12" sm="6" md="4" class="pa-2">
                    <v-text-field v-model="filterName" label="考试名称" placeholder="输入考试名称" clearable
                        @input="resetPages"></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="4" class="pa-2">
                    <v-select v-model="filterSubject" :items="subjectOptions" label="科目" placeholder="选择科目" clearable
                        @change="resetPages"></v-select>
                </v-col>
                <v-col cols="12" sm="6" md="4" class="pa-2">
                    <v-select v-model="filterStatus" :items="statusOptions" label="状态" placeholder="选择测试状态" clearable
                        @change="resetPages"></v-select>
                </v-col>
            </v-row>
        </v-card>
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
                                    <v-btn v-if="!(exam.ready && exam.disclosed)" color="primary"
                                        @click="enterExam(exam)">进入批改</v-btn>
                                    <v-btn v-if="exam.ready && !exam.disclosed" color="red"
                                        @click="confirm(exam)">公布成绩</v-btn>
                                    <v-btn v-else-if="exam.ready && exam.disclosed" disabled>成绩已公布</v-btn>
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
        <v-dialog v-model="confirmDialogOpen" max-width="50%">
            <v-card>
                <v-card-title>
                    <v-icon color="primary">mdi-alert-circle-outline</v-icon>
                    <span class="headline ml-2">公布后无法修改成绩</span>
                </v-card-title>
                <v-card-text>确定公布测试 {{ this.toDiscloseExam.name }} 的成绩吗？</v-card-text>
                <v-card-actions>
                    <v-btn color="red" variant="text" @click="discloseExam">
                        确定
                    </v-btn>
                    <v-btn variant="plain" @click="confirmDialogOpen = false">
                        取消
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import { mapMutations, mapActions } from "vuex";
import axios from "axios";
export default {
    name: "ExamList",
    data() {
        return {
            exams: [],
            filterName: "",
            filterSubject: "",
            currentPage: 1,
            itemsPerPage: 8, // Number of exams per page
            confirmDialogOpen: false,
            toDiscloseExam: null,
            filterStatus: '全部',
            statusOptions: [
                '全部', '待批改', '已批改完成', '已公布成绩'
            ],
            loading: true,
        };
    },
    computed: {
        totalPages() {
            return Math.ceil(this.exams.length / this.itemsPerPage);
        },
        paginatedExams() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.filteredExams.slice(start, end);
        },
        combinedExams() {
            return [...this.ongoingExams, ...this.comingExams];
        },
        allSubjects() {
            const subjects = [
                ...this.exams.map(exam => exam.subject),
            ];
            return Array.from(new Set(subjects)).sort();
        },
        subjectOptions() {
            return this.allSubjects;
        },
        filteredExams() {
            const filterName = (this.filterName || "").toLowerCase().trim();
            const filterSubject = this.filterSubject || "";

            let filtered = this.exams.filter(exam => {
                const examName = exam.name || "";
                const matchesName = examName.toLowerCase().includes(filterName);
                const matchesSubject = filterSubject ? exam.subject === filterSubject : true;
                return matchesName && matchesSubject;
            });

            if (this.filterStatus === '待批改') {
                filtered = filtered.filter(exam => {
                    return !exam.ready;
                });
            } else if (this.filterStatus === '已批改完成') {
                filtered = filtered.filter(exam => {
                    return exam.ready && !exam.disclosed;
                });
            } else if (this.filterStatus === '已公布成绩') {
                filtered = filtered.filter(exam => {
                    return exam.ready && exam.disclosed;
                });
            }

            return filtered;
        },
    },
    mounted() {
        const title = "模拟测试评分";
        this.setAppTitle(title);
        this.setPageTitle(title);
        this.getAll();
    },
    methods: {
        // 映射 Vuex 的 mutation
        ...mapMutations(["setAppTitle", "setPageTitle"]),
        ...mapActions('snackbar', ['showSnackbar']),
        async getAll() {
            const response = await axios.post('http://127.0.0.1:8000/api/exams/get_all_exams/', {
                user_id: this.$store.getters.getUserId
            });
            console.log(response.data);
            this.exams = response.data.exams;
            this.loading = false;
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
        resetPages() {
            this.currentPage = 1;
        },
        enterExam(exam) {
            // 导航到目标路由
            this.$router.push(`/admin/judge/${exam.id}`);
        },
        async confirm(exam) {
            this.toDiscloseExam = exam;
            this.confirmDialogOpen = true;
        },
        async discloseExam() {
            this.confirmDialogOpen = false;
            this.toDiscloseExam.disclosed = true;
            const response = await axios.post('http://127.0.0.1:8000/api/exams/publish_exam_results/', {
                user_id: this.$store.getters.getUserId,
                exam_id: this.toDiscloseExam.id
            });
            this.showSnackbar({
                message: `已公布“${this.toDiscloseExam.name}”的成绩`,
                color: 'success',
                timeout: 3000
            });
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

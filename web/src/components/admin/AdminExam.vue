<template>
    <div>
        <!-- 顶部横幅 -->
        <v-banner sticky icon="mdi-plus" lines="one">
            <template v-slot:text>
                <div class="text-subtitle-1">作为辅导师，你可创建新的模拟测试，或编辑已有的模拟测试。</div>
            </template>

            <template v-slot:actions>
                <v-btn color="primary" class="mr-5" @click="gotoNew">
                    <div class="text-subtitle-1">创建模拟测试</div>
                </v-btn>
            </template>
        </v-banner>

        <!-- 筛选条件区域 -->
        <v-card variant="text" class="pb-2 pl-2 pr-2" title="筛选模拟测试" subtitle="通过名称搜索或选择科目进行筛选" prepend-icon="mdi-filter">
            <v-row align="center" justify="start" no-gutters>
                <v-col cols="12" sm="6" md="4" class="pa-2">
                    <v-text-field v-model="filterName" label="考试名称" placeholder="输入考试名称" clearable
                        @input="resetPages"></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="4" class="pa-2">
                    <v-select v-model="filterSubject" :items="subjectOptions" label="科目" placeholder="选择科目" clearable
                        @change="resetPages"></v-select>
                </v-col>
            </v-row>
        </v-card>

        <!-- 考试列表区域 -->
        <div class="scroll-container">
            <v-expansion-panels>
                <!-- 进行中的测试 -->
                <v-expansion-panel>
                    <v-expansion-panel-title>
                        <template v-slot:default="{ expanded }">
                            <v-row no-gutters class="align-center w-100">
                                <v-col class="d-flex justify-start text-bold" cols="2">
                                    进行中的测试
                                </v-col>
                                <v-col class="text-grey" cols="9">
                                    <v-fade-transition leave-absolute>
                                        <span> 共 {{ filteredOngoingExams.length }} 个考试 </span>
                                    </v-fade-transition>
                                </v-col>
                            </v-row>
                        </template>
                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                        <v-row dense class="justify-start">
                            <v-col v-for="exam in paginatedExams(filteredOngoingExams, ongoingPage)" :key="exam.id"
                                cols="12" sm="6" md="3" class="pa-1">
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
                                        <v-btn color="primary" text @click="viewEditExam(exam.id)">查看/编辑测试</v-btn>
                                    </v-card-actions>
                                </v-card>
                            </v-col>
                        </v-row>
                        <v-pagination v-model="ongoingPage"
                            :length="Math.ceil(filteredOngoingExams.length / itemsPerPage)" :total-visible="7"
                            class="my-4" @input="scrollToTop"></v-pagination>
                    </v-expansion-panel-text>
                </v-expansion-panel>

                <!-- 即将进行的测试 -->
                <v-expansion-panel>
                    <v-expansion-panel-title>
                        <template v-slot:default="{ expanded }">
                            <v-row no-gutters class="align-center w-100">
                                <v-col class="d-flex justify-start text-bold" cols="2">
                                    即将进行的测试
                                </v-col>
                                <v-col class="text-grey" cols="9">
                                    <v-fade-transition leave-absolute>
                                        <span> 共 {{ filteredComingExams.length }} 个考试 </span>
                                    </v-fade-transition>
                                </v-col>
                            </v-row>
                        </template>
                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                        <v-row dense class="justify-start">
                            <v-col v-for="exam in paginatedExams(filteredComingExams, comingPage)" :key="exam.id"
                                cols="12" sm="6" md="3" class="pa-1">
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
                                        <v-btn color="primary" text @click="viewEditExam(exam.id)">查看/编辑测试</v-btn>
                                        <v-btn color="red" text @click="confirmDeleteExam(exam.id, exam.name)">删除测试</v-btn>
                                    </v-card-actions>
                                </v-card>
                            </v-col>
                        </v-row>
                        <v-pagination v-model="comingPage"
                            :length="Math.ceil(filteredComingExams.length / itemsPerPage)" :total-visible="7"
                            class="my-4" @input="scrollToTop"></v-pagination>
                    </v-expansion-panel-text>
                </v-expansion-panel>

                <!-- 已结束的测试 -->
                <v-expansion-panel>
                    <v-expansion-panel-title>
                        <template v-slot:default="{ expanded }">
                            <v-row no-gutters class="align-center w-100">
                                <v-col class="d-flex justify-start text-bold" cols="2">
                                    已结束的测试
                                </v-col>
                                <v-col class="text-grey" cols="9">
                                    <v-fade-transition leave-absolute>
                                        <span> 共 {{ filteredPastExams.length }} 个考试 </span>
                                    </v-fade-transition>
                                </v-col>
                            </v-row>
                        </template>
                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                        <v-row dense class="justify-start">
                            <v-col v-for="exam in paginatedExams(filteredPastExams, pastPage)" :key="exam.id" cols="12"
                                sm="6" md="3" class="pa-1">
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
                                        <v-btn color="primary" text @click="viewEditExam(exam.id)">查看/编辑测试</v-btn>
                                        <v-btn color="red" text @click="confirmDeleteExam(exam.id, exam.name)">删除测试</v-btn>
                                    </v-card-actions>
                                </v-card>
                            </v-col>
                        </v-row>
                        <v-pagination v-model="pastPage" :length="Math.ceil(filteredPastExams.length / itemsPerPage)"
                            :total-visible="7" class="my-4" @input="scrollToTop"></v-pagination>
                    </v-expansion-panel-text>
                </v-expansion-panel>
            </v-expansion-panels>
        </div>
    </div>
    <v-dialog v-model="confirmDialogOpen" max-width="400px">
        <v-card>
            <v-card-title>
                <v-icon color="primary">mdi-alert-circle-outline</v-icon>
                <span class="headline ml-2">操作不可逆</span>
            </v-card-title>
            <v-card-text>确定删除题库 {{ this.toDeleteExamName }}吗？</v-card-text>
            <v-card-actions>
                <v-btn color="red" variant="text" @click="deleteExam()">
                    确定
                </v-btn>
                <v-btn variant="plain" @click="confirmDialogOpen = false">
                    取消
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
    <v-snackbar v-model="snackbar.show" :timeout="2000" :color="snackbar.color" min-width="25%">
        <div style="font-size: 16px">{{ snackbar.message }}</div>
        <template #actions>
            <v-btn icon @click="snackbar.show = false">
                <v-icon>mdi-close</v-icon>
            </v-btn>
        </template>
    </v-snackbar>
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
                // ... 其他进行中的测试数据
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
                // ... 其他即将进行的测试数据
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
                // ... 其他已结束的测试数据
            ],
            itemsPerPage: 4, // 每页显示的测试数量
            ongoingPage: 1,
            comingPage: 1,
            pastPage: 1,
            // 筛选条件
            filterName: "",
            filterSubject: "",
            snackbar: {
                show: false,
                message: '',
                color: 'error'
            },
            confirmDialogOpen: false,
            toDeleteExamId: null
        };
    },
    mounted() {
        const title = "模拟测试管理";
        this.setAppTitle(title);
        this.setPageTitle(title);
    },
    computed: {
        // 获取所有唯一的科目选项
        allSubjects() {
            const subjects = [
                ...this.ongoingExams.map(exam => exam.subject),
                ...this.comingExams.map(exam => exam.subject),
                ...this.pastExams.map(exam => exam.subject),
            ];
            return Array.from(new Set(subjects)).sort();
        },
        subjectOptions() {
            return this.allSubjects;
        },
        // 过滤后的进行中的考试
        filteredOngoingExams() {
            const filterName = (this.filterName || "").toLowerCase().trim();
            const filterSubject = this.filterSubject || "";

            return this.ongoingExams.filter(exam => {
                const examName = exam.name || "";
                const matchesName = examName.toLowerCase().includes(filterName);
                const matchesSubject = filterSubject ? exam.subject === filterSubject : true;
                return matchesName && matchesSubject;
            });
        },
        // 过滤后的即将进行的考试
        filteredComingExams() {
            const filterName = (this.filterName || "").toLowerCase().trim();
            const filterSubject = this.filterSubject || "";

            return this.comingExams.filter(exam => {
                const examName = exam.name || "";
                const matchesName = examName.toLowerCase().includes(filterName);
                const matchesSubject = filterSubject ? exam.subject === filterSubject : true;
                return matchesName && matchesSubject;
            });
        },
        // 过滤后的已结束的考试
        filteredPastExams() {
            const filterName = (this.filterName || "").toLowerCase().trim();
            const filterSubject = this.filterSubject || "";

            return this.pastExams.filter(exam => {
                const examName = exam.name || "";
                const matchesName = examName.toLowerCase().includes(filterName);
                const matchesSubject = filterSubject ? exam.subject === filterSubject : true;
                return matchesName && matchesSubject;
            });
        },
    },
    methods: {
        ...mapMutations(["setAppTitle", "setPageTitle"]),
        formatDate(dateString) {
            const options = {
                year: "numeric",
                month: "2-digit",
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
        gotoNew() {
            this.$router.push("/admin/exam/new");
        },
        viewEditExam(id) {
            this.$router.push(`/admin/exam/${id}`);
        },
        confirmDeleteExam(id, name) {
            this.toDeleteExamId = id;
            this.toDeleteExamName = name;
            this.confirmDialogOpen = true;
        },
        deleteExam() {
            this.showSnackbar(`已删除测试 ${this.toDeleteExamId} ${this.toDeleteExamName}`, 'success');
            this.confirmDialogOpen = false;
        },
        showSnackbar(message, color = 'error') {
            this.snackbar = {
                show: true,
                message,
                color
            };
        },
        resetPages() {
            this.ongoingPage = 1;
            this.comingPage = 1;
            this.pastPage = 1;
        },
        scrollToTop() {
            // 滚动到顶部，提升用户体验
            const container = this.$el.querySelector(".scroll-container");
            if (container) {
                container.scrollTop = 0;
            }
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
    height: 60vh;
    max-height: 60vh;
    -ms-overflow-style: none;
    scrollbar-width: none;
}

.scroll-container::-webkit-scrollbar {
    display: none;
}

.info-row {
    display: flex;
    margin-bottom: 4px;
}

.info-row span:first-child {
    font-weight: bold;
    width: 80px;
}

.info-row span:last-child {
    flex: 1;
}

.v-responsive {
    max-width: 100%;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    font-size: 14px;
}

.v-expansion-panel {
    margin-bottom: 8px;
}

.v-expansion-panel-title {
    cursor: pointer;
}

.v-banner {
    margin-bottom: 16px;
}

.v-expansion-panel {
    margin-bottom: 0px;
}

/* 没有结果的提示 */
.no-results {
    padding: 32px;
    text-align: center;
    color: #757575;
}

/* 可选：调整按钮颜色和样式 */
.v-btn.blue-darken-4 {
    background-color: #1e3a8a;
    /* 深蓝色 */
    color: white;
}

.v-btn.blue-darken-4:hover {
    background-color: #1e40af;
}

.btns {
    margin-top: 16px;
    padding-left: 16px;
}

.info-card {
    max-height: 60%;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.card-text {
    padding-left: 16px;
    padding-top: 16px;
    text-align: left;
    overflow: hidden;
}

.info-card .v-btn {
    margin-top: 8px;
}

.info-item {
    display: flex;
    align-items: center;
    margin-top: 8px;
    gap: 8px;
    font-size: 16px;
    text-align: left;
}

.info-title {
    font-weight: bold;
}
</style>

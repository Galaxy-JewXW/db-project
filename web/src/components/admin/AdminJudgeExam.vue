<template>
    <div class="problem-set-detail" v-if="problemSetData">
        <v-scroll-y-transition mode="out-in">
            <!-- 测试进行中且未完成所有题目 -->
            <div v-if="finishedQuestions.length < totalQuestions" style="padding-bottom: 15px">
                <v-alert type="info" icon="mdi-clock-outline">
                    <v-alert-title>
                        批改进行中。
                    </v-alert-title>
                    已完成{{ totalQuestions }}题中{{ finishedQuestions.length }}题的批改。
                </v-alert>
            </div>

            <!-- 测试进行中且已完成所有题目 -->
            <div v-else-if="finishedQuestions.length === totalQuestions" style="padding-bottom: 15px">
                <v-alert type="success">
                    <v-alert-title>
                        批改已完成。
                    </v-alert-title>
                    本次测试的所有题目均已批改完成。
                </v-alert>
            </div>
        </v-scroll-y-transition>

        <!-- 题库名称 -->
        <h1 style="padding-top: 10px">{{ problemSetData.name }}</h1>

        <!-- 信息芯片 -->
        <div class="chips-row" style="padding-bottom: 5px; margin-bottom: 5px">
            <v-chip v-for="(chip, index) in chips" :key="index" :color="chip.color" class="ma-1 chip-item">
                <v-icon left class="chip-icon">{{ chip.icon }}</v-icon>
                {{ chip.label }}: {{ chip.value }}
            </v-chip>
        </div>

        <!-- 可滚动的题目列表区域 -->
        <div class="questions-container">
            <v-expansion-panels>
                <v-expansion-panel v-for="(group, index) in questions" :key="index">
                    <v-expansion-panel-title>
                        <template v-slot:default="{ expanded }">
                            <v-row no-gutters>
                                <v-col class="d-flex justify-start text-bold" cols="4">
                                    {{ group.type }}
                                </v-col>
                                <v-col class="text-grey" cols="8">
                                    <v-fade-transition leave-absolute>
                                        <span>
                                            本部分共 {{ group.ids.length }} 题，已完成
                                            {{
                                                finishedQuestions.filter((qid) =>
                                                    group.ids.includes(qid)
                                                ).length
                                            }}
                                            题
                                        </span>
                                    </v-fade-transition>
                                </v-col>
                            </v-row>
                        </template>
                    </v-expansion-panel-title>

                    <!-- 题目按钮及分页控件 -->
                    <v-expansion-panel-text>
                        <v-row no-gutters>
                            <div class="question-squares">
                                <v-btn v-for="questionId in getPaginatedIds(group)" :key="questionId" :class="[
                                    'question-square',
                                    { finished: finishedQuestions.includes(questionId) },
                                ]" :color="finishedQuestions.includes(questionId)
                                    ? 'green'
                                    : 'blue-darken-4'
                                    " rounded="0" @click="goToQuestionDetail(questionId)">
                                    <v-responsive class="text-truncate">{{ questionId }}</v-responsive>
                                </v-btn>
                            </div>
                        </v-row>
                        <!-- 分页控件 -->
                        <v-row justify="center" class="mt-2">
                            <v-pagination v-model="group.currentPage" :total-visible="7"
                                :length="Math.ceil(group.ids.length / pageSize)"
                                @input="handlePageChange(group, $event)"></v-pagination>
                        </v-row>
                    </v-expansion-panel-text>
                </v-expansion-panel>
            </v-expansion-panels>
        </div>
    </div>
</template>

<script>
import { mapMutations } from "vuex";
import axios from "axios";
export default {
    name: "ProblemSetDetail",
    props: {
        examId: {
            type: String,
            required: true,
        }
    },
    data() {
        return {
            currentId: null,
            problemSetData: null,
            questions: [],
            loading: false,
            error: null,
            dialog: false, // 控制dialog显示
            question: "", // 存储题面的Markdown文本
            loadingQuestion: false, // 控制加载状态
            finishedQuestions: [], // 完成的题目
            files: [],
            choices: -2,
            selectedOption: null, // 单项选择题
            selectedOptions: [], // 多项选择题
            text: "",
            pageSize: 10, // 每页显示的题目数量
            questionType: "", // 当前题目的类型
            currentQuestionId: null, // 当前题目ID
        };
    },
    computed: {
        totalQuestions() {
            return (
                this.questions?.reduce((total, group) => {
                    return total + group.ids.length;
                }, 0) || 0
            );
        },
        chips() {
            return [
                {
                    color: "primary",
                    icon: "mdi-book-open",
                    label: "所属科目",
                    value: this.problemSetData?.subject || "N/A",
                },
                {
                    color: "secondary",
                    icon: "mdi-clock-outline",
                    label: "时长",
                    value: `${this.problemSetData?.duration || 0} 分钟`,
                },
                {
                    color: "success",
                    icon: "mdi-calendar",
                    label: "测试开始时间",
                    value: this.formatDate2S(this.problemSetData?.starttime),
                },
                {
                    color: "warning",
                    icon: "mdi-format-list-numbered",
                    label: "题目数量",
                    value: `${this.totalQuestions} 题`,
                },
            ];
        },
    },
    mounted() {
        const id = parseInt(this.examId);
        this.currentId = id;
        this.fetchProblemSetData(id);
    },
    methods: {
        ...mapMutations(["setAppTitle", "setPageTitle", "setProblemType"]),

        async fetchProblemSetData(problemSetId) {
            console.log(`Fetching problem set data for ID: ${problemSetId}`);
            this.loading = true;
            this.error = null;

            try {
                // 模拟从后端获取模拟测试数据
                const response = await axios.post('http://127.0.0.1:8000/api/exams/get_exam_questions_teacher/', {
                    user_id: this.$store.getters.getUserId,
                    exam_id: problemSetId
                });
                const data = response.data;
                this.problemSetData = {
                    id: data.exam_id,
                    name: data.name,
                    subject: data.subject,
                    starttime: data.startTime,
                    duration: data.duration,
                };
                const title = "模拟测试详情 - " + this.problemSetData.name;
                this.finishedQuestions = data.finish;
                this.setAppTitle(title);
                this.setPageTitle(title);
                this.fetchQuestionsById(problemSetId); // 获取题目列表
                this.loading = false;
            } catch (e) {
                console.error("获取模拟测试数据失败", e);
                this.error = "获取模拟测试数据失败";
                this.loading = false;
            }
        },

        async fetchQuestionsById(problemSetId) {
            console.log(`Fetching questions for problem set ID: ${problemSetId}`);
            this.loading = true;
            this.error = null;

            try {
                const response = await axios.post('http://127.0.0.1:8000/api/exams/get_exam_questions_teacher/', {
                    user_id: this.$store.getters.getUserId,
                    exam_id: problemSetId
                });
                // 模拟从后端获取数据
                const questions = response.data.new_que;
                this.questions = questions; // 更新组件本地的题目列表数据
                this.loading = false;
            } catch (e) {
                console.error("获取题目数据失败", e);
                this.error = "获取题目数据失败";
                this.loading = false;
            }
        },

        formatDate2S(dateString) {
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

        goToQuestionDetail(questionId) {
            console.log(
                `Fetching question for question ID: ${questionId}`
            );
            this.$router.push(`/admin/judge/${this.currentId}/${questionId}`);
        },

        // 获取当前页的题目ID
        getPaginatedIds(group) {
            const start = (group.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return group.ids.slice(start, end);
        },

        // 处理分页变化
        handlePageChange(group, newPage) {
            group.currentPage = newPage;
        },
    },
};
</script>

<style scoped>
.problem-set-detail {
    padding: 16px;
}

.chips-row {
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 16px;
    align-items: center;
}

.chip-item {
    display: flex;
    align-items: center;
    margin-right: 8px;
}

.chip-item:last-child {
    margin-right: 0;
}

.chip-icon {
    margin-right: 4px;
}

.questions-container {
    max-height: calc(100vh - 300px);
    overflow-y: auto;
    padding: 16px 16px 32px;
    display: flex;
    flex-direction: column;
    scrollbar-width: none;
}

.questions-container::-webkit-scrollbar {
    display: none;
}

.question-squares {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 16px;
}

.question-square {
    width: 70px;
    height: 70px;
    font-size: 16px;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    border-radius: 0;
    overflow-wrap: break-word;
    word-wrap: break-word;
    cursor: pointer;
}

.question-square:hover {
    background-color: rgba(0, 0, 0, 0.1);
}

.v-responsive {
    max-width: 100%;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    font-size: 14px;
}

.v-expansion-panel {
    margin-bottom: 0px;
}

.markdown-content {
    padding: 16px;
    font-size: 16px;
}

.v-card {
    margin-top: 16px;
}

.v-card-title {
    font-size: 18px;
    font-weight: bold;
}

.v-card-text {
    font-size: 14px;
}

.fullscreen-card {
    width: 100vw;
    height: 100vh;
    max-width: 100vw;
    max-height: 100vh;
    margin: 0;
}
</style>
<template>
    <div class="grading-page">
        <v-container fluid>
            <v-row>
                <!-- 左侧栏：学生答案 -->
                <v-col cols="12" md="8">
                    <v-window v-model="currentWindow" show-arrows="hover">
                        <v-window-item v-for="(answer, index) in answers" :key="answer.student">
                            <v-card class="pa-4">
                                <!-- 答案导航指示器 -->
                                <v-card-title>
                                    学生ID: {{ answer.student }}
                                </v-card-title>
                                <v-card-subtitle>
                                    第{{ index + 1 }}个回答 / 共{{ answers.length }}个回答
                                </v-card-subtitle>
                                <v-card-text class="scroll-container1">
                                    <v-md-preview :text="answer.answer"></v-md-preview>
                                </v-card-text>
                            </v-card>
                        </v-window-item>
                    </v-window>
                </v-col>

                <!-- 右侧栏：评分和标准答案 -->
                <v-col cols="12" md="4">
                    <v-card>
                        <v-card-title>
                            评分 (总分: {{ totalScore }})
                        </v-card-title>
                        <v-card-text>
                            <v-form ref="scoreForm" @submit.prevent="saveScore">
                                <v-text-field v-model.number="selectedScore" label="分数" :rules="scoreRules"
                                    type="number" min="1" :max="maxScore" required variant="outlined"></v-text-field>
                                <v-btn color="primary" @click="saveScore">
                                    保存分数
                                </v-btn>
                                <v-btn variant="plain" @click="goBack">
                                    返回总览页面
                                </v-btn>
                            </v-form>
                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-title>
                            标准答案
                        </v-card-title>
                        <v-card-text class="scroll-container">
                            <v-md-preview :text="stdanswer"></v-md-preview>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>

        <!-- Snackbar 用于显示分数保存成功的消息 -->
        <v-snackbar v-model="snackbar" :timeout="500" top right color="green">
            分数已保存！
            <template v-slot:action="{ attrs }">
                <v-btn color="white" text v-bind="attrs" @click="snackbar = false">
                    关闭
                </v-btn>
            </template>
        </v-snackbar>
    </div>
</template>

<script>
import { mapMutations } from 'vuex'; // 引入 mapMutations

export default {
    name: 'GradingPage',
    props: {
        examId: {
            type: String,
            required: true,
        },
        exerciseId: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            currentWindow: 0, // 当前选择的窗口索引
            stdanswer: '',
            answers: [],
            selectedScore: 1, // 默认分数
            snackbar: false, // 控制 Snackbar 显示
            totalScore: 10, // 题目的总分
        };
    },
    computed: {
        maxScore() {
            return this.totalScore - 1;
        },
        scoreRules() {
            return [
                v => (v !== null && v !== undefined && v !== '') || '分数不能为空',
                v => Number.isInteger(v) || '分数必须是整数',
                v => (v > 0) || '分数必须大于 0',
                v => (v <= this.totalScore) || `分数不可大于总分 ${this.totalScore}`,
            ];
        },
    },
    watch: {
        // 监听窗口变化以更新 selectedScore
        currentWindow(newVal) {
            const selectedAnswer = this.answers[newVal];
            if (selectedAnswer) {
                // 确保分数符合规则
                this.selectedScore =
                    selectedAnswer.score >= 1 && selectedAnswer.score <= this.maxScore
                        ? selectedAnswer.score
                        : 1;
            }
        },
    },
    mounted() {
        // 更新页面标题
        const title = `测试 ${this.examId} - 批改题目${this.exerciseId}`;
        console.log(`所在考试：${this.examId} 批改题目：${this.exerciseId}`);
        this.setAppTitle(title);
        this.setPageTitle(title);
        this.fetchAnswers(this.examId, this.exerciseId);
    },
    methods: {
        ...mapMutations(['setAppTitle', 'setPageTitle']), // 映射 Vuex 的 mutations
        goBack() {
            this.$router.push(`/admin/judge/${this.examId}`);
        },
        fetchAnswers(examId, exerciseId) {
            // 模拟从 API 获取数据
            // 在这里应替换为实际的 API 调用以获取数据
            this.stdanswer = `$x * y$`;
            this.totalScore = 10; // 示例总分，实际数据请替换
            this.answers = [
                {
                    student: 22373001,
                    answer: 'x + y',
                    score: 5,
                },
                {
                    student: 22373002,
                    answer: 'x * y',
                    score: 7,
                },
                {
                    student: 22373003,
                    answer: `$y * x - 2$`,
                    score: 3,
                },
            ];
            // 初始化 selectedScore 为第一个学生的分数或默认值 1
            if (this.answers.length > 0) {
                const initialScore =
                    this.answers[0].score >= 1 && this.answers[0].score <= this.maxScore
                        ? this.answers[0].score
                        : 1;
                this.selectedScore = initialScore;
            }
        },
        saveScore() {
            const selectedAnswer = this.answers[this.currentWindow];
            if (selectedAnswer) {
                // 使用表单验证
                const isValid = this.$refs.scoreForm.validate();
                if (!isValid) {
                    return;
                }

                const score = Number(this.selectedScore);
                // 再次确保分数合法性
                if (
                    !Number.isInteger(score) ||
                    score < 1 ||
                    score >= this.totalScore
                ) {
                    // 验证失败，不保存
                    return;
                }

                // 更新本地状态中的分数
                selectedAnswer.score = score;

                // 这里可以提交 Vuex mutation 或调用 API 将分数保存到服务器
                console.log(
                    `已保存学生 ${selectedAnswer.student} 的分数: ${score}`
                );

                // 显示 Snackbar
                this.snackbar = true;
            }
        },
    },
};
</script>

<style scoped>
.grading-page {
    padding: 20px;
}

.scroll-container {
    flex-direction: column;
    flex: 1 1 auto;
    overflow-y: auto;
    padding: 16px;
    height: 60vh;
    max-height: 60vh;
    -ms-overflow-style: none;
    scrollbar-width: none;
}

.scroll-container1 {
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

.scroll-container::-webkit-scrollbar,
.scroll-container1::-webkit-scrollbar {
    display: none;
}
</style>
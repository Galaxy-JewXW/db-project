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

                <!-- 右侧栏：正误标记和标准答案 -->
                <v-col cols="12" md="4">
                    <v-card>
                        <v-card-title>
                            判定正误
                        </v-card-title>
                        <v-card-text>
                            <v-form ref="correctnessForm" @submit.prevent="saveCorrectness">
                                <v-switch v-model="isCorrectSelected" :label="isCorrectSelected ? '回答正确' : '回答错误'"
                                    hide-details="auto"></v-switch>
                                <v-btn color="primary" @click="saveCorrectness">
                                    保存结果
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
    </div>
</template>

<script>
import { mapMutations, mapActions } from 'vuex';

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
            isCorrectSelected: false,
        };
    },
    watch: {
        currentWindow(newVal) {
            const selectedAnswer = this.answers[newVal];
            if (selectedAnswer) {
                this.isCorrectSelected = selectedAnswer.isCorrect;
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
        ...mapMutations(['setAppTitle', 'setPageTitle']),
        ...mapActions('snackbar', ['showSnackbar']),
        goBack() {
            this.$router.push(`/admin/judge/${this.examId}`);
        },
        fetchAnswers(examId, exerciseId) {
            // 在这里应替换为实际的 API 调用以获取数据
            this.stdanswer = `$x * y$`;
            // 示例数据，使用 isCorrect 字段表示正误
            this.answers = [
                {
                    student: 22373001,
                    answer: 'x + y',
                    isCorrect: false,
                },
                {
                    student: 22373002,
                    answer: 'x * y',
                    isCorrect: true,
                },
                {
                    student: 22373003,
                    answer: `$y * x - 2$`,
                    isCorrect: false,
                },
            ];
            if (this.answers.length > 0) {
                this.isCorrectSelected = this.answers[0].isCorrect;
            }
        },
        saveCorrectness() {
            const selectedAnswer = this.answers[this.currentWindow];
            if (selectedAnswer) {
                selectedAnswer.isCorrect = this.isCorrectSelected;
                // 这里可调用 API 保存数据
                console.log(`已保存学生 ${selectedAnswer.student} 的判定结果: ${this.isCorrectSelected ? '正确' : '错误'}`);
                this.showSnackbar({
                    message: '结果已提交',
                    color: 'success',
                    timeout: 1500
                });
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
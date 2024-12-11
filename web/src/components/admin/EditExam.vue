<template>
    <v-banner sticky icon="mdi-plus" lines="one">
        <template v-slot:text>
            <div class="text-subtitle-1">作为辅导师，你可编辑此模拟测试。</div>
        </template>

        <template v-slot:actions>
            <v-btn color="primary" class="mr-5" @click="goBack">
                <div class="text-subtitle-1">返回</div>
            </v-btn>
        </template>
    </v-banner>

    <v-tabs v-model="tempTab" color="primary">
        <v-tab v-for="tabItem in tabs" :key="tabItem.value" :value="tabItem.value"
            :disabled="tabItem.value > maxAllowedTab + 1">
            {{ tabItem.label }}
        </v-tab>
    </v-tabs>

    <div class="pa-2">
        <v-tabs-window v-model="tab" class="scroll-container mt-2">
            <!-- 编辑基本信息 -->
            <v-tabs-window-item :value="1" eager>
                <v-form ref="formRef" @submit.prevent>
                    <v-row no-gutters>
                        <v-col cols="12">
                            <v-text-field v-model="form.name" label="名称" :rules="[value => !!value || '名称为必填项']"
                                required />
                        </v-col>
                        <!-- 科目输入 -->
                        <v-col cols="12">
                            <v-radio-group v-model="form.subject" label="学科" inline
                                :rules="[value => !!value || '请选择学科']" required>
                                <v-radio label="工科数学分析（上）" value="工科数学分析（上）" />
                                <v-radio label="工科数学分析（下）" value="工科数学分析（下）" />
                                <v-radio label="工科高等代数" value="工科高等代数" />
                                <v-radio label="离散数学（信息类）" value="离散数学（信息类）" />
                                <v-radio label="基础物理学A" value="基础物理学A" />
                            </v-radio-group>
                        </v-col>

                        <v-col cols="12">
                            <v-text-field v-model="form.startTime" label="开始时间" type="datetime-local"
                                :rules="[value => !!value || '开始时间为必填项']" required />
                        </v-col>

                        <!-- 时长输入 -->
                        <v-col cols="12">
                            <v-text-field v-model.number="form.duration" label="时长（分钟）" :rules="[
                                value => !!value || '时长为必填项',
                                value => Number.isInteger(value) || '时长必须是整数',
                                value => value > 0 || '时长必须大于0'
                            ]" required />
                        </v-col>
                    </v-row>
                </v-form>
            </v-tabs-window-item>

            <!-- 编辑题目 -->
            <v-tabs-window-item :value="2" eager>
                <v-row>
                    <v-col cols="6">
                        <div class="pa-3">
                            <v-card :title="form.subject + '的所有题目'" prepend-icon="mdi-plus"
                                subtitle="左键点击以查看题目，右键点击以添加题目到模拟测试。">
                                <v-divider></v-divider>
                                <v-expansion-panels>
                                    <v-expansion-panel v-for="(group, index) in questions" :key="index">
                                        <v-expansion-panel-title>
                                            <template v-slot:default="{ expanded }">
                                                <v-row no-gutters>
                                                    <v-col class="d-flex justify-start text-bold" cols="2">
                                                        {{ group.type }}
                                                    </v-col>
                                                    <v-col class="text-grey" cols="10">
                                                        <v-fade-transition leave-absolute>
                                                            <span>
                                                                共 {{ group.ids.length }} 题
                                                            </span>
                                                        </v-fade-transition>
                                                    </v-col>
                                                </v-row>
                                            </template>
                                        </v-expansion-panel-title>
                                        <v-expansion-panel-text>
                                            <v-row no-gutters>
                                                <div class="question-squares">
                                                    <v-btn v-for="questionId in getPaginatedIds(group)"
                                                        :key="questionId" class="question-square text-none"
                                                        color="blue-darken-4" rounded="0"
                                                        @click="viewQuestion(group.type, questionId)"
                                                        @contextmenu.prevent="addQuestion(group.type, questionId)">
                                                        <v-responsive class="text-truncate">
                                                            {{ questionId }}
                                                        </v-responsive>
                                                    </v-btn>
                                                </div>
                                            </v-row>
                                            <v-row justify="center" class="mt-2">
                                                <v-pagination v-model="group.currentPage"
                                                    :length="Math.ceil(group.ids.length / pageSize)" :total-visible="7"
                                                    @input="handlePageChange(group, $event)"></v-pagination>
                                            </v-row>
                                        </v-expansion-panel-text>
                                    </v-expansion-panel>
                                </v-expansion-panels>
                            </v-card>
                        </div>
                    </v-col>
                    <v-col cols="6">
                        <div class="pa-3">
                            <v-card :title="'模拟测试 ' + form.name + ' 已添加的题目'" prepend-icon="mdi-minus"
                                subtitle="左键点击以查看题目，右键点击以从模拟测试中移除题目。">
                                <v-divider></v-divider>
                                <v-expansion-panels>
                                    <v-expansion-panel v-for="(group, index) in form.questions" :key="index">
                                        <v-expansion-panel-title>
                                            <template v-slot:default="{ expanded }">
                                                <v-row no-gutters>
                                                    <v-col class="d-flex justify-start text-bold" cols="2">
                                                        {{ group.type }}
                                                    </v-col>
                                                    <v-col class="text-grey" cols="10">
                                                        <v-fade-transition leave-absolute>
                                                            <span>
                                                                共 {{ group.questions.length }} 题
                                                            </span>
                                                        </v-fade-transition>
                                                    </v-col>
                                                </v-row>
                                            </template>
                                        </v-expansion-panel-title>
                                        <v-expansion-panel-text>
                                            <v-row no-gutters>
                                                <div class="question-squares">
                                                    <v-btn v-for="question in getPaginatedQuestions(group)"
                                                        :key="question.id" class="question-square text-none"
                                                        color="blue-darken-4" rounded="0"
                                                        @click="viewQuestion(group.type, question.id)"
                                                        @contextmenu.prevent="removeQuestion(group.type, question.id)">
                                                        <v-responsive class="text-truncate">
                                                            {{ question.id }}
                                                        </v-responsive>
                                                    </v-btn>
                                                </div>
                                            </v-row>
                                            <v-row justify="center" class="mt-2">
                                                <v-pagination v-model="group.currentPage"
                                                    :length="Math.ceil(group.questions.length / pageSize)"
                                                    :total-visible="7"
                                                    @input="handlePageChange(group, $event)"></v-pagination>
                                            </v-row>
                                        </v-expansion-panel-text>
                                    </v-expansion-panel>
                                </v-expansion-panels>
                            </v-card>
                        </div>
                    </v-col>
                </v-row>
            </v-tabs-window-item>

            <!-- 编辑题目分值 -->
            <v-tabs-window-item :value="3" eager>
                <v-form ref="scoreFormRef" @submit.prevent>
                    <v-row>
                        <v-col cols="12">
                            <v-alert type="info" icon="mdi-information" class="mb-4">
                                请为每个已添加的题目设置分数。 当前总分：{{ calculateTotalScore().total }}
                            </v-alert>
                        </v-col>
                        <v-col v-for="(group, groupIndex) in form.questions" :key="groupIndex" cols="12">
                            <v-card class="mb-4 ml-2 mr-2">
                                <v-card-title class="text-h6">
                                    {{ group.type }} （总分：{{ calculateTotalScore()[group.type] || 0 }}）
                                </v-card-title>
                                <v-divider></v-divider>
                                <v-card-text>
                                    <v-data-table :headers="scoreHeaders" :items="group.questions" density="compact"
                                        disable-pagination disable-sort>
                                        <template v-slot:item.id="{ item }">
                                            {{ item.id }}
                                        </template>
                                        <template v-slot:item.score="{ item, index }">
                                            <v-text-field v-model.number="item.score" type="number" min="1" :rules="[
                                                v => v !== null && v !== undefined || '分数为必填项',
                                                v => Number.isInteger(v) || '分数必须是整数',
                                                v => v > 0 || '分数必须大于0'
                                            ]" @change="updateScore(group.type, item.id, item.score)"></v-text-field>
                                        </template>
                                        <template v-slot:item.actions="{ item }">
                                            <v-btn color="primary" variant="text" small
                                                @click="viewQuestion(group.type, item.id)">
                                                查看题目
                                            </v-btn>
                                        </template>
                                    </v-data-table>
                                </v-card-text>
                            </v-card>
                        </v-col>
                    </v-row>
                </v-form>
            </v-tabs-window-item>

            <!-- 预览模拟测试 -->
            <v-tabs-window-item :value="4" eager>
                <v-alert color="warning" class="mb-3" icon="mdi-circle-multiple-outline">
                    <v-alert-title>确认</v-alert-title>
                    请确认模拟测试信息编辑是否正确。若均填写正确，请点击下方提交按钮。直接离开本界面不会对原有测试进行更改。
                </v-alert>
                <v-btn color="primary" variant="outlined" @click="handleSubmit">提交</v-btn>
                <div class="pa-3">
                    <v-row>
                        <v-col cols="12" md="8">
                            <v-expansion-panels>
                                <v-expansion-panel v-for="(group, index) in form.questions" :key="index">
                                    <v-expansion-panel-title>
                                        <template v-slot:default="{ expanded }">
                                            <v-row no-gutters>
                                                <v-col class="d-flex justify-start text-bold" cols="2">
                                                    {{ group.type }}
                                                </v-col>
                                                <v-col class="text-grey" cols="10">
                                                    <v-fade-transition leave-absolute>
                                                        <span>
                                                            共 {{ group.questions.length }} 题
                                                        </span>
                                                    </v-fade-transition>
                                                </v-col>
                                            </v-row>
                                        </template>
                                    </v-expansion-panel-title>
                                    <v-expansion-panel-text>
                                        <v-row no-gutters>
                                            <div class="question-squares">
                                                <v-btn v-for="question in getPaginatedQuestions(group)"
                                                    :key="question.id" class="question-square text-none"
                                                    color="blue-darken-4" rounded="0"
                                                    @click="viewQuestion(group.type, question.id)"
                                                    @contextmenu.prevent="removeQuestion(group.type, question.id)">
                                                    <v-responsive class="text-truncate">
                                                        {{ question.id }}
                                                    </v-responsive>
                                                </v-btn>
                                            </div>
                                        </v-row>
                                        <v-row justify="center" class="mt-2">
                                            <v-pagination v-model="group.currentPage"
                                                :length="Math.ceil(group.questions.length / pageSize)"
                                                :total-visible="7"
                                                @input="handlePageChange(group, $event)"></v-pagination>
                                        </v-row>
                                    </v-expansion-panel-text>
                                </v-expansion-panel>
                            </v-expansion-panels>
                        </v-col>
                        <v-col cols="12" md="4">
                            <v-card class="info-card" outlined>
                                <v-card-title class="text-h6">基本信息</v-card-title>
                                <v-divider></v-divider>
                                <v-card-text class="card-text">
                                    <!-- 添加题目相关信息 -->
                                    <div class="info-item">
                                        <v-icon>mdi-database</v-icon>
                                        <span class="info-title">名称：</span>
                                        <span>{{ form.name }}</span>
                                    </div>
                                    <div class="info-item">
                                        <v-icon>mdi-school</v-icon>
                                        <span class="info-title">学科：</span>
                                        <span>{{ form.subject }}</span>
                                    </div>
                                    <div class="info-item">
                                        <v-icon>mdi-clock-time-eight-outline</v-icon>
                                        <span class="info-title">开始时间：</span>
                                        <span>{{ formatDate(form.startTime) }}</span>
                                    </div>
                                    <div class="info-item">
                                        <v-icon>mdi-timer-outline</v-icon>
                                        <span class="info-title">时长：</span>
                                        <span>{{ form.duration }} 分钟</span>
                                    </div>
                                </v-card-text>
                            </v-card>
                        </v-col>
                    </v-row>
                </div>
            </v-tabs-window-item>
        </v-tabs-window>
    </div>

    <v-dialog v-model="dialog" transition="dialog-bottom-transition" fullscreen>
        <v-card>
            <v-toolbar dark color="primary">
                <v-btn icon @click="dialog = false;">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
                <v-toolbar-title>预览题目 - {{ currentQuestion.id }}</v-toolbar-title>
            </v-toolbar>
            <div class="pa-4">
                <v-alert color="warning" class="mb-3" icon="mdi-chart-donut">
                    <v-alert-title>预览题目 - {{ currentQuestion.id }}</v-alert-title>
                    以下是原始题目信息。如需更改信息，请进入“题目管理-编辑题目”修改。
                </v-alert>
                <v-row justify="start">
                    <!-- 左侧内容区域，占 8 列（约 70%） -->
                    <v-col cols="12" md="8">
                        <div>
                            <v-md-preview :text="currentQuestion.content" v-if="currentQuestion"></v-md-preview>
                        </div>
                    </v-col>

                    <!-- 右侧卡片区域，占 4 列（约 30%） -->
                    <v-col cols="12" md="4">
                        <v-card class="info-card" outlined>
                            <v-card-title class="text-h6">基本信息</v-card-title>
                            <v-divider></v-divider>
                            <v-card-text class="card-text">
                                <!-- 添加题目相关信息 -->
                                <div class="info-item">
                                    <v-icon>mdi-school</v-icon>
                                    <span class="info-title">学科：</span>
                                    <span>{{ currentQuestion.subject }}</span>
                                </div>
                                <div class="info-item">
                                    <v-icon>mdi-comment-edit-outline</v-icon>
                                    <span class="info-title">题型：</span>
                                    <span>{{ currentQuestion.questionType }}</span>
                                </div>
                                <div class="info-item">
                                    <v-icon>mdi-source-branch</v-icon>
                                    <span class="info-title">来源：</span>
                                    <span>{{ currentQuestion.source }}</span>
                                </div>
                                <div class="info-item">
                                    <v-icon>mdi-tag</v-icon>
                                    <span class="info-title">标签：</span>
                                    <span>{{ currentQuestion.tags }}</span>
                                </div>
                                <div class="info-item">
                                    <v-icon>mdi-star-outline</v-icon>
                                    <span class="info-title">难度：</span>
                                    <span>{{ currentQuestion.difficulty }}</span>
                                </div>
                            </v-card-text>
                        </v-card>
                        <v-card class="mt-4">
                            <v-card-title class="text-h6">答案</v-card-title>
                            <v-divider></v-divider>
                            <v-md-preview :text="currentQuestion.answer" v-if="currentQuestion"></v-md-preview>
                        </v-card>
                    </v-col>
                </v-row>
            </div>
        </v-card>
    </v-dialog>
</template>

<script>
import { mapMutations, mapActions } from "vuex";
import axios from "axios";
export default {
    name: "AdminSet",
    props: {
        id: {
            type: String,
            required: true,
        }
    },
    data() {
        return {
            tab: 1,
            tempTab: 1,
            maxAllowedTab: 4,
            currentId: null,
            tabs: [
                { value: 1, label: "编辑基本信息" },
                { value: 2, label: "编辑题目" },
                { value: 3, label: "编辑题目分值" },
                { value: 4, label: "预览模拟测试" },
            ],
            form: {
                name: "",
                subject: "",
                startTime: "",
                duration: null,
                description: "",
                questions: [], // Array of groups with type, questions (id & score), currentPage
            },
            originalForm: {},
            questions: [],
            pageSize: 40,
            dialog: false,
            currentQuestion: {
                id: 1,
                questionType: "单项选择题",
                content: `
# Markdown 测试文档
`,
                subject: "工科数学分析（上）",
                source: "自出题",
                tags: "算法",
                difficulty: "中等",
                answer: "B",
            },
            scoreHeaders: [
                { title: "题目编号", value: "id" },
                { title: "设定分数", value: "score" },
                { title: "操作", value: "actions" },
            ],
        };
    },
    mounted() {
        // 更新标题
        const title = "编辑模拟测试 - " + this.id;
        this.currentId = parseInt(this.id);
        console.log('接收到的 ID:', this.currentId);
        this.setAppTitle(title);
        this.setPageTitle(title);
        this.fetchExam(this.currentId);
        this.getExercises(this.form.subject);
    },
    methods: {
        ...mapMutations(["setAppTitle", "setPageTitle"]),
        ...mapActions('snackbar', ['showSnackbar']),
        goBack() {
            this.$router.push("/admin/exam");
        },
        fetchExam(problemId) {
            // 模拟直接从后端获取数据
            const mockProblemData = {
                name: "史上最难数分",
                subject: "工科数学分析（上）",
                startTime: "2024-11-25 14:20:00",
                duration: 120,
                questions: [
                    {
                        currentPage: 1,
                        type: "单项选择题",
                        questions: [
                            { id: 12, score: 1 },
                            { id: 13, score: 1 },
                            { id: 14, score: 10 },
                        ]
                    },
                    {
                        currentPage: 1,
                        type: "多项选择题",
                        questions: [
                            { id: 121, score: 10 },
                            { id: 131, score: 10 },
                            { id: 141, score: 10 },
                        ]
                    },
                ],
            };
            this.form = { ...mockProblemData };
            console.log(this.form);
            this.originalForm = { ...mockProblemData };
        },
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
            return date
                .toLocaleString("zh-CN", options)
                .replace(/\//g, "-");
        },
        calculateTotalScore() {
            const scores = this.form.questions.reduce((result, group) => {
                const groupTotal = group.questions.reduce((sum, question) => {
                    return sum + (question.score || 0); // 默认分数为 0
                }, 0);
                result[group.type] = groupTotal;
                result.total += groupTotal;
                return result;
            }, { total: 0 });
            return scores;
        },
        getExercises(subject) {
            // Simulate fetching questions based on subject
            // This should be replaced with actual API calls
            const questions = [
                {
                    type: "单项选择题",
                    ids: [...Array(50).keys()].map((i) => i + 1), // 生成 50 道单项选择题
                    currentPage: 1,
                },
                {
                    type: "填空题",
                    ids: [101, 102, 103], // 填空题
                    currentPage: 1,
                },
                {
                    type: "判断题",
                    ids: [1101, 1102, 1103], // 判断题
                    currentPage: 1,
                },
                {
                    type: "解答题",
                    ids: [201, 202], // 解答题
                    currentPage: 1,
                },
            ];
            this.questions = [...questions];
        },
        async validateForm() {
            try {
                const isValid = await this.$refs.formRef.validate();
                if (!isValid.valid) {
                    this.showSnackbar({
                        message: '请填写所有必填字段，并确保字段合法！',
                        color: 'error',
                        timeout: 2000
                    });
                }
                return isValid;
            } catch (error) {
                console.error("表单验证出错：", error);
                this.showSnackbar({
                    message: '表单验证出错',
                    color: 'error',
                    timeout: 2000
                });
                return false;
            }
        },
        async validateScoreForm() {
            try {
                const isValid = await this.$refs.scoreFormRef.validate();
                if (!isValid) {
                    this.showSnackbar({
                        message: '请为所有题目设置有效分数！',
                        color: 'error',
                        timeout: 2000
                    });
                }
                return isValid;
            } catch (error) {
                console.error("分数表单验证出错：", error);
                this.showSnackbar({
                    message: '分数表单验证出错',
                    color: 'error',
                    timeout: 2000
                });
                return false;
            }
        },
        async beforeTabChange(newTab, oldTab) {
            if (newTab > oldTab) {
                // 只在前往后续页面时校验
                if (newTab === 2) {
                    const isValid = await this.validateForm();
                    if (!isValid.valid) {
                        this.showSnackbar({
                            message: '基本信息未填写或有误，请及时修改',
                            color: 'error',
                            timeout: 2000
                        });
                        this.tempTab = oldTab; // 还原到当前页
                        return;
                    }
                } else if (newTab === 3) {
                    const isValid = await this.validateForm();
                    if (!isValid.valid) {
                        this.showSnackbar({
                            message: '基本信息未填写或有误，请及时修改',
                            color: 'error',
                            timeout: 2000
                        });
                        this.tempTab = oldTab;
                        this.tab = oldTab;
                        return;
                    }
                    if (this.form.questions.length === 0) {
                        this.showSnackbar({
                            message: '模拟测试内容不能为空',
                            color: 'error',
                            timeout: 2000
                        });
                        this.tempTab = 2;
                        this.tab = 2;
                        return;
                    }
                } else if (newTab === 4) {
                    const isValid = await this.validateForm();
                    console.log(isValid);
                    if (!isValid.valid) {
                        this.showSnackbar({
                            message: '基本信息未填写或有误，请及时修改',
                            color: 'error',
                            timeout: 2000
                        });
                        this.tempTab = oldTab;
                        this.tab = oldTab;
                        return;
                    }
                    if (this.form.questions.length === 0) {
                        this.showSnackbar({
                            message: '模拟测试内容不能为空',
                            color: 'error',
                            timeout: 2000
                        });
                        this.tempTab = 2;
                        this.tab = 2;
                        return;
                    }
                    const scoreValid = await this.validateScoreForm();
                    console.log(scoreValid);
                    if (!scoreValid) {
                        this.showSnackbar({
                            message: '请为所有题目设置有效分数',
                            color: 'error',
                            timeout: 2000
                        });
                        this.tempTab = 3;
                        this.tab = 3;
                        return;
                    }
                }
                this.maxAllowedTab = Math.max(this.maxAllowedTab, newTab); // 解锁新页面
            }
            this.tab = newTab;
        },
        async handleSubmit() {
            // Validate all forms
            const isValidForm = await this.validateForm();
            const isValidScores = await this.validateScoreForm();

            if (!isValidForm.valid) {
                this.showSnackbar({
                    message: '基本信息未填写或有误，请及时修改',
                    color: 'error',
                    timeout: 2000
                });
                this.tempTab = 1;
                this.tab = 1;
                return;
            }

            if (this.form.questions.length === 0) {
                this.showSnackbar({
                    message: '模拟测试内容不能为空',
                    color: 'error',
                    timeout: 2000
                });
                this.tempTab = 2;
                this.tab = 2;
                return;
            }

            if (!isValidScores) {
                this.showSnackbar({
                    message: '请为所有题目设置有效分数',
                    color: 'error',
                    timeout: 2000
                });
                this.tempTab = 3;
                this.tab = 3;
                return;
            }

            try {
                // TODO: 在这里添加实际的表单提交逻辑
                console.log(this.form);
                this.showSnackbar({
                    message: '编辑考试成功',
                    color: 'success',
                    timeout: 2000
                });
                this.goBack();
            } catch (error) {
                console.error("表单提交出错：", error);
                this.showSnackbar({
                    message: '表单提交失败',
                    color: 'error',
                    timeout: 2000
                });
            }
        },
        async viewQuestion(type, id) {
            this.dialog = true;
            try {
                // 发送 POST 请求到后端获取数据
                const response = await axios.post('http://127.0.0.1:8000/api/questions/get_question_by_id/', {
                    user_id: this.$store.getters.getUserId,
                    question_id: id
                });
               
                // 检查后端返回的响应
                if (response.data.success) {
                    const question_data = response.data.question;
                    console.log(question_data.tags);
                    // 将后端返回的题目信息映射到前端的 `questions` 结构
                    this.currentQuestion.id = question_data.id;
                    this.currentQuestion.questionType = question_data.type; // 映射 type 到 questionType
                    this.currentQuestion.content = question_data.content;
                    this.currentQuestion.subject = question_data.subject;
                    this.currentQuestion.source = question_data.source;
                    this.currentQuestion.tags = question_data.tags.join(", "); // 假设 tags 是数组，需要转换为字符串
                    this.currentQuestion.difficulty = question_data.difficulty;
                    this.currentQuestion.answer = question_data.answer;
                } else {
                    throw new Error("获取题目数据失败");
                }
            } catch (e) {
                console.error("获取题目数据失败", e);
                this.error = "获取题目数据失败";
            }
            console.log(`访问了 ${type} 的题目 - ${id}`);
        },
        addQuestion(type, id) {
            // 查找是否已经存在该类型
            const typeIndex = this.form.questions.findIndex(
                (group) => group.type === type
            );
            if (typeIndex !== -1) {
                // 类型存在，检查id是否已经存在
                const questionExists = this.form.questions[
                    typeIndex
                ].questions.find((q) => q.id === id);
                if (!questionExists) {
                    this.form.questions[typeIndex].questions.push({
                        id: id,
                        score: 10, // Default score
                    });
                    this.showSnackbar({
                        message: `已添加题目 - ${id} 到 ${type}`,
                        color: 'success',
                        timeout: 2000
                    });
                } else {
                    this.showSnackbar({
                        message: `题目 - ${id} 已添加`,
                        color: 'warning',
                        timeout: 2000
                    });
                }
            } else {
                // 类型不存在，添加新的类型和id
                this.form.questions.push({
                    type: type,
                    questions: [
                        {
                            id: id,
                            score: 10, // Default score
                        },
                    ],
                    currentPage: 1,
                });
                this.showSnackbar({
                    message: `已添加题目 - ${id} 到 ${type}`,
                    color: 'success',
                    timeout: 2000
                });
            }
            this.sortQuestions();
        },
        removeQuestion(type, id) {
            // 查找该类型
            const typeIndex = this.form.questions.findIndex(
                (group) => group.type === type
            );
            if (typeIndex !== -1) {
                const questionIndex = this.form.questions[
                    typeIndex
                ].questions.findIndex((q) => q.id === id);
                if (questionIndex !== -1) {
                    this.form.questions[typeIndex].questions.splice(
                        questionIndex,
                        1
                    );
                    this.showSnackbar({
                        message: `已从 ${type} 移除题目 - ${id} `,
                        color: 'success',
                        timeout: 2000
                    });
                    // 如果该类型下没有题目了，移除整个类型
                    if (
                        this.form.questions[typeIndex].questions.length ===
                        0
                    ) {
                        this.form.questions.splice(typeIndex, 1);
                    } else {
                        // 调整 currentPage 以确保不超过总页数
                        const group = this.form.questions[typeIndex];
                        const totalPages = Math.ceil(
                            group.questions.length / this.pageSize
                        );
                        if (group.currentPage > totalPages) {
                            group.currentPage = totalPages;
                        }
                    }
                }
            }
            this.sortQuestions();
        },
        sortQuestions() {
            const typeOrder = [
                "单项选择题",
                "多项选择题",
                "判断题",
                "填空题",
                "解答题",
            ];

            this.form.questions.sort(
                (a, b) => typeOrder.indexOf(a.type) - typeOrder.indexOf(b.type)
            );

            this.form.questions.forEach((group) => {
                group.questions.sort((a, b) => a.id - b.id);
            });
        },
        getPaginatedIds(group) {
            const start = (group.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return group.ids.slice(start, end);
        },
        getPaginatedQuestions(group) {
            const start = (group.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return group.questions.slice(start, end);
        },
        handlePageChange(group, newPage) {
            group.currentPage = newPage;
        },
        updateScore(type, id, score) {
            // Find the question and update its score
            const group = this.form.questions.find(
                (g) => g.type === type
            );
            if (group) {
                const question = group.questions.find((q) => q.id === id);
                if (question) {
                    question.score = score;
                }
            }
        },
    },
    watch: {
        tempTab(newTab, oldTab) {
            this.beforeTabChange(newTab, oldTab);
        },
    },
};
</script>

<style scoped>
.scroll-container {
    flex-direction: column;
    flex: 1 1 auto;
    overflow-y: auto;
    height: 80vh;
    max-height: 80vh;
    -ms-overflow-style: none;
    scrollbar-width: none;
}

.scroll-container::-webkit-scrollbar {
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

.info-card {
    max-height: 80vh;
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

.v-data-table {
    overflow-x: auto;
}
</style>
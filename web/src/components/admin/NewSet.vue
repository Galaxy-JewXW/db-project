<template>
    <v-banner sticky icon="mdi-plus" lines="one">
        <template v-slot:text>
            <div class="text-subtitle-1">作为辅导师，你可创建新的题库。</div>
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
            <v-tabs-window-item :value="1">
                <!-- 设置基本信息 -->
                <v-form ref="formRef" @submit.prevent>
                    <v-row no-gutters>
                        <v-col cols="12">
                            <v-text-field v-model.number="form.name" label="名称" :rules="[value => !!value || '名称为必填项']"
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

                        <!-- 时长输入 -->
                        <v-col cols="12">
                            <v-text-field v-model.number="form.duration" label="时长（分钟）" :rules="[
                                value => !!value || '时长为必填项',
                                value => Number.isInteger(value) || '时长必须是整数',
                                value => value > 0 || '时长必须大于0'
                            ]" required />
                        </v-col>

                        <!-- 描述输入 -->
                        <v-col cols="12">
                            <v-textarea v-model="form.description" label="描述（不超过60字）" :rules="[
                                value => !!value || '描述为必填项',
                                value => value.length <= 60 || '描述不能超过60字'
                            ]" required rows="4" no-resize counter />
                        </v-col>
                    </v-row>
                </v-form>
            </v-tabs-window-item>
            <v-tabs-window-item :value="2">
                <v-row>
                    <v-col cols="6">
                        <div class="pa-3">
                            <v-card :title="form.subject + '的所有题目'" prepend-icon="mdi-plus"
                                subtitle="左键点击以查看题目，右键点击以添加题目到题库">
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
                                                            <span> 共 {{ group.ids.length }} 题 </span>
                                                        </v-fade-transition>
                                                    </v-col>
                                                </v-row>
                                            </template>
                                        </v-expansion-panel-title>
                                        <v-expansion-panel-text>
                                            <v-row no-gutters>
                                                <div class="question-squares">
                                                    <v-btn v-for="questionId in group.ids" :key="questionId"
                                                        class="question-square text-none" color="blue-darken-4"
                                                        rounded="0" @click="viewQuestion(group.type, questionId)"
                                                        @contextmenu.prevent="addQuestion(group.type, questionId)">
                                                        <v-responsive class="text-truncate">{{ questionId
                                                            }}</v-responsive>
                                                    </v-btn>
                                                </div>
                                            </v-row>
                                        </v-expansion-panel-text>
                                    </v-expansion-panel>
                                </v-expansion-panels>
                            </v-card>
                        </div>
                    </v-col>
                    <v-col cols="6">
                        <div class="pa-3">
                            <v-card :title="'题库 ' + form.name + ' 已添加的题目'" prepend-icon="mdi-minus"
                                subtitle="左键点击以从题库中移除题目">
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
                                                            <span> 共 {{ group.ids.length }} 题 </span>
                                                        </v-fade-transition>
                                                    </v-col>
                                                </v-row>
                                            </template>
                                        </v-expansion-panel-title>
                                        <v-expansion-panel-text>
                                            <v-row no-gutters>
                                                <div class="question-squares">
                                                    <v-btn v-for="questionId in group.ids" :key="questionId"
                                                        class="question-square text-none" color="blue-darken-4"
                                                        rounded="0" @click="removeQuestion(group.type, questionId)">
                                                        <v-responsive class="text-truncate">{{ questionId
                                                            }}</v-responsive>
                                                    </v-btn>
                                                </div>
                                            </v-row>
                                        </v-expansion-panel-text>
                                    </v-expansion-panel>
                                </v-expansion-panels>
                            </v-card>
                        </div>
                    </v-col>
                </v-row>
            </v-tabs-window-item>
            <v-tabs-window-item :value="3">
                <!-- 预览内容 -->
                <div>
                    <h3>题库预览</h3>
                    <v-list>
                        <v-list-item-group>
                            <v-list-item v-for="(group, index) in form.questions" :key="index">
                                <v-list-item-content>
                                    <v-list-item-title>{{ group.type }}</v-list-item-title>
                                    <v-list-item-subtitle>
                                        {{ group.ids.join(', ') }}
                                    </v-list-item-subtitle>
                                </v-list-item-content>
                            </v-list-item>
                        </v-list-item-group>
                    </v-list>
                </div>
            </v-tabs-window-item>
        </v-tabs-window>
    </div>

    <!-- Snackbar for notifications -->
    <v-snackbar v-model="snackbar.show" :timeout="1000" :color="snackbar.color" min-width="25%">
        <div style="font-size: 16px">{{ snackbar.message }}</div>
        <template #actions>
            <v-btn icon @click="snackbar.show = false">
                <v-icon>mdi-close</v-icon>
            </v-btn>
        </template>
    </v-snackbar>
</template>

<script>
import { mapMutations } from 'vuex';

export default {
    name: 'AdminSet',
    data() {
        return {
            tab: 1,
            tempTab: 1,
            maxAllowedTab: 1,
            tabs: [
                { value: 1, label: '设置基本信息' },
                { value: 2, label: '添加题目' },
                { value: 3, label: '预览题库' }
            ],
            form: {
                name: '',
                subject: '',
                duration: null,
                description: '',
                questions: []
            },
            questions: [],
            snackbar: {
                show: false,
                message: '',
                color: 'error'
            },
        };
    },
    mounted() {
        // 更新标题
        const title = '创建新题库';
        this.setAppTitle(title);
        this.setPageTitle(title);
        // 初始化题目列表
        this.getExercises(this.form.subject);
    },
    methods: {
        ...mapMutations(['setAppTitle', 'setPageTitle']),
        goBack() {
            this.$router.push('/admin/problemset');
        },
        showSnackbar(message, color = 'error') {
            this.snackbar = {
                show: true,
                message,
                color
            };
        },
        getExercises(subject) {
            const questions = [
                {
                    type: "单项选择题",
                    ids: [...Array(50).keys()].map((i) => i + 1), // 生成 50 道单项选择题
                },
                {
                    type: "填空题",
                    ids: [101, 102, 103], // 填空题
                },
                {
                    type: "判断题",
                    ids: [1101, 1102, 1103], // 填空题
                },
                {
                    type: "解答题",
                    ids: [201, 202], // 解答题
                },
            ];
            this.questions = [...questions];
        },
        async validateForm() {
            try {
                const isValid = await this.$refs.formRef.validate();
                if (!isValid.valid) {
                    this.showSnackbar('请填写所有必填字段，并确保字段合法！');
                }
                return isValid;
            } catch (error) {
                console.error('表单验证出错：', error);
                this.showSnackbar('表单验证出错');
                return false;
            }
        },
        async beforeTabChange(newTab, oldTab) {
            if (newTab > oldTab) {
                // 只在前往后续页面时校验
                const isValid = await this.validateForm();
                console.log(isValid);
                if (!isValid.valid) {
                    this.showSnackbar('基本信息未填写或有误，请及时修改');
                    this.tempTab = oldTab; // 还原到当前页
                    return;
                }
                this.maxAllowedTab = Math.max(this.maxAllowedTab, newTab); // 解锁新页面
            }
            if (newTab === 2) {
                console.log(this.form);
                this.getExercises(this.form.subject);
            }
            this.tab = newTab;
        },
        viewQuestion(type, id) {
            console.log(`访问了 ${type} 的题目 - ${id}`);
        },
        addQuestion(type, id) {
            // 查找是否已经存在该类型
            const typeIndex = this.form.questions.findIndex(group => group.type === type);
            if (typeIndex !== -1) {
                // 类型存在，检查id是否已经存在
                if (!this.form.questions[typeIndex].ids.includes(id)) {
                    this.form.questions[typeIndex].ids.push(id);
                    this.showSnackbar(`已添加题目 - ${id} 到 ${type}`, 'success');
                } else {
                    this.showSnackbar(`题目 - ${id} 已添加`, 'info');
                }
            } else {
                // 类型不存在，添加新的类型和id
                this.form.questions.push({
                    type: type,
                    ids: [id]
                });
                this.showSnackbar(`已添加题目 - ${id} 到 ${type}`, 'success');
            }
            this.sortQuestions();
        },
        removeQuestion(type, id) {
            // 查找该类型
            const typeIndex = this.form.questions.findIndex(group => group.type === type);
            if (typeIndex !== -1) {
                const idIndex = this.form.questions[typeIndex].ids.indexOf(id);
                if (idIndex !== -1) {
                    this.form.questions[typeIndex].ids.splice(idIndex, 1);
                    this.showSnackbar(`已从 ${type} 移除题目 - ${id} `);
                    // 如果该类型下没有题目了，移除整个类型
                    if (this.form.questions[typeIndex].ids.length === 0) {
                        this.form.questions.splice(typeIndex, 1);
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
                "解答题"
            ];

            this.form.questions.sort(
                (a, b) => typeOrder.indexOf(a.type) - typeOrder.indexOf(b.type)
            );

            this.form.questions.forEach((group) => {
                group.ids.sort((a, b) => a - b);
            });
        },
    },
    watch: {
        tempTab(newTab, oldTab) {
            this.beforeTabChange(newTab, oldTab);
        }
    }
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
</style>

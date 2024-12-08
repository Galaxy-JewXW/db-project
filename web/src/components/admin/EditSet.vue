<template>
    <v-banner sticky icon="mdi-plus" lines="one">
        <template v-slot:text>
            <div class="text-subtitle-1">作为辅导师，你可查看/编辑此题库。</div>
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
                                subtitle="左键点击以查看题目，右键点击以添加题目到题库。">
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
                                                    <v-btn v-for="questionId in getPaginatedIds(group)"
                                                        :key="questionId" class="question-square text-none"
                                                        color="blue-darken-4" rounded="0"
                                                        @click="viewQuestion(group.type, questionId)"
                                                        @contextmenu.prevent="addQuestion(group.type, questionId)">
                                                        <v-responsive class="text-truncate">{{ questionId
                                                            }}</v-responsive>
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
                            <v-card :title="'题库 ' + form.name + ' 已添加的题目'" prepend-icon="mdi-minus"
                                subtitle="左键点击以查看题目，右键点击以从题库中移除题目。">
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
                                                    <v-btn v-for="questionId in getPaginatedIds(group)"
                                                        :key="questionId" class="question-square text-none"
                                                        color="blue-darken-4" rounded="0"
                                                        @click="viewQuestion(group.type, questionId)"
                                                        @contextmenu.prevent="removeQuestion(group.type, questionId)">
                                                        <v-responsive class="text-truncate">{{ questionId
                                                            }}</v-responsive>
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
                </v-row>
            </v-tabs-window-item>
            <v-tabs-window-item :value="3">
                <v-alert color="warning" class="mb-3" icon="mdi-circle-multiple-outline">
                    <v-alert-title>确认</v-alert-title>
                    请确认题库信息编辑是否正确。若均填写正确，请点击下方提交按钮。直接离开本界面不会对原有题库进行更改。
                </v-alert>
                <v-btn color="primary" variant="outlined" @click="handleSubmit">提交</v-btn>
                <!-- 预览内容 -->
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
                                                        <span> 共 {{ group.ids.length }} 题 </span>
                                                    </v-fade-transition>
                                                </v-col>
                                            </v-row>
                                        </template>
                                    </v-expansion-panel-title>
                                    <v-expansion-panel-text>
                                        <v-row no-gutters>
                                            <div class="question-squares">
                                                <v-btn v-for="questionId in getPaginatedIds(group)" :key="questionId"
                                                    class="question-square text-none" color="blue-darken-4" rounded="0"
                                                    @click="viewQuestion(group.type, questionId)"
                                                    @contextmenu.prevent="removeQuestion(group.type, questionId)">
                                                    <v-responsive class="text-truncate">{{ questionId
                                                        }}</v-responsive>
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
                                        <span class="info-title">时长：</span>
                                        <span>{{ form.duration }} 分钟</span>
                                    </div>
                                    <div class="info-item">
                                        <v-icon>mdi-forum</v-icon>
                                        <span class="info-title">描述：</span>
                                        <span>{{ form.description }}</span>
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
import { mapMutations, mapActions } from 'vuex';

export default {
    name: 'AdminSet',
    props: {
        id: {
            type: String,
            required: true,
        }
    },
    data() {
        return {
            currentId: null,
            originalSet: {},
            tab: 1,
            tempTab: 1,
            maxAllowedTab: 3,
            tabs: [
                { value: 1, label: '编辑基本信息' },
                { value: 2, label: '编辑题目' },
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
            pageSize: 40,
            dialog: false,
            currentQuestion: {
                id: 1,
                questionType: "单项选择题",
                content: `
# Markdown 测试文档

## 1. 简介
这是一个用于测试的 Markdown 文档，用于验证各种 Markdown 特性以及 \`marked\` 库的渲染能力。以下内容包含各种元素，如标题、列表、表格、图片、链接、代码块以及 LaTeX 公式。

## 2. 列表

### 2.1 无序列表
- 第一项
- 第二项
  - 嵌套项 1
  - 嵌套项 2
- 第三项

### 2.2 有序列表
1. 第一点
2. 第二点
   1. 嵌套第一点
   2. 嵌套第二点
3. 第三点

## 3. 链接与图片
- [OpenAI 官网](https://www.openai.com)
- 图片示例：
  ![image-20240910103809548](https://drinkwater-1325041233.cos.ap-guangzhou.myqcloud.com/imgs/image-20240910103809548.png)

## 4. 代码块

### 4.1 行内代码
这是一个行内代码示例：\`console.log("Hello, World!");\`

### 4.2 多行代码块
\`\`\`javascript
function greet(name) {
  console.log(\`Hello, \${name}!\`);
}

greet('OpenAI');
\`\`\`

## 5. 表格
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Row 1    | Data 1   | Data A   |
| Row 2    | Data 2   | Data B   |
| Row 3    | Data 3   | Data C   |

## 6. 引用与分隔线
> 这是一个引用块，可以用于引用他人的话语或注释。

---
这是一个分隔线，用于分割内容。

## 7. LaTeX 公式

### 7.1 行内公式
这是一个行内公式示例：$E = mc^2$

### 7.2 多行公式
$$
\\int_{a}^{b} f(x) \\,dx = F(b) - F(a)
$$

这是一个多行公式，用于展示积分计算。

## 8. 粗体与斜体

- **这是一个粗体文本示例**
- *这是一个斜体文本示例*
- ***这是一个粗体加斜体文本示例***
    
## 9. 长文本段落测试
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum vehicula ex eu nulla scelerisque, ac consectetur lacus dapibus. Phasellus efficitur risus in ligula tempor, et lacinia risus convallis. Nunc sit amet erat nec elit suscipit auctor. Mauris convallis purus eu lectus tincidunt, in volutpat odio mollis. Integer a nisl mi. Duis ac magna sed orci facilisis aliquet. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse potenti. Praesent sit amet turpis non nisl interdum tempor a nec orci.
    
Donec ac odio sit amet nisi feugiat dignissim. Proin ac erat nec mauris pretium vulputate. Ut gravida lectus sit amet sapien tincidunt, non efficitur magna viverra. Fusce sed arcu eu odio euismod ullamcorper. Nulla facilisi. Aenean vitae orci dui. Phasellus sit amet maximus magna, vel ornare nisi. Donec euismod nulla eget libero dignissim, sit amet finibus lacus ultricies. Ut consequat mauris vitae sem volutpat, eget tempor orci auctor. Cras vestibulum diam vitae tellus vehicula, at consectetur sapien aliquet。
`,
                subject: "工科数学分析（上）",
                source: "自出题",
                tags: "算法",
                difficulty: "中等",
                answer: "B",
            }
        };
    },
    mounted() {
        // 更新标题

        this.currentId = parseInt(this.id);
        console.log('接收到的 ID:', this.currentId);
        // 初始化题目列表
        this.fetchProblemSet(this.currentId);
        const title = '查看/编辑题库 - ' + this.originalSet.name;
        this.setAppTitle(title);
        this.setPageTitle(title);
    },
    methods: {
        ...mapMutations(['setAppTitle', 'setPageTitle']),
        ...mapActions('snackbar', ['showSnackbar']),
        fetchProblemSet(id) {
            const mockData = {
                name: '上学期期中',
                subject: '工科高等代数',
                duration: 120,
                description: '哥们自己乱编的题目',
                questions: [
                    {
                        type: "单项选择题",
                        ids: [99, 101, 102, 104],
                        currentPage: 1,
                    },
                    {
                        type: "填空题",
                        ids: [8101, 8102, 8103], // 填空题
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
                ]
            };
            this.form = { ...mockData };
            this.originalSet = { ...mockData };
        },
        goBack() {
            this.$router.push('/admin/problemset');
        },
        getExercises(subject) {
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
                this.showSnackbar({
                    message: '表单验证出错',
                    color: 'error',
                    timeout: 2000
                });
                return false;
            }
        },
        async beforeTabChange(newTab, oldTab) {
            if (newTab > oldTab) {
                // 只在前往后续页面时校验
                const isValid = await this.validateForm();
                console.log(isValid);
                if (!isValid.valid) {
                    this.showSnackbar({
                        message: '基本信息未填写或有误，请及时修改',
                        color: 'error',
                        timeout: 2000
                    });
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
        async handleSubmit() {
            // 验证第一页的表单
            const isValid = await this.validateForm();
            if (!isValid.valid) {
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
                    message: '题目内容不能为空',
                    color: 'error',
                    timeout: 2000
                });
                this.tempTab = 2;
                this.tab = 2;
                return;
            }
            try {
                // TODO: 在这里添加实际的表单提交逻辑
                this.showSnackbar({
                    message: '编辑题库成功',
                    color: 'success',
                    timeout: 2000
                });
                console.log(this.form);
                this.goBack();
            } catch (error) {
                console.error('表单提交出错：', error);
                this.showSnackbar({
                    message: '表单提交出错',
                    color: 'error',
                    timeout: 2000
                });
            }
        },
        viewQuestion(type, id) {
            this.dialog = true;
            console.log(`访问了 ${type} 的题目 - ${id}`);
        },
        addQuestion(type, id) {
            // 查找是否已经存在该类型
            const typeIndex = this.form.questions.findIndex(group => group.type === type);
            if (typeIndex !== -1) {
                // 类型存在，检查id是否已经存在
                if (!this.form.questions[typeIndex].ids.includes(id)) {
                    this.form.questions[typeIndex].ids.push(id);
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
                    ids: [id],
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
            const typeIndex = this.form.questions.findIndex(group => group.type === type);
            if (typeIndex !== -1) {
                const idIndex = this.form.questions[typeIndex].ids.indexOf(id);
                if (idIndex !== -1) {
                    this.form.questions[typeIndex].ids.splice(idIndex, 1);
                    this.showSnackbar({
                        message: `已从 ${type} 移除题目 - ${id} `,
                        color: 'success',
                        timeout: 2000
                    });
                    // 如果该类型下没有题目了，移除整个类型
                    if (this.form.questions[typeIndex].ids.length === 0) {
                        this.form.questions.splice(typeIndex, 1);
                    } else {
                        // 调整 currentPage 以确保不超过总页数
                        const group = this.form.questions[typeIndex];
                        const totalPages = Math.ceil(group.ids.length / this.pageSize);
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
                "解答题"
            ];

            this.form.questions.sort(
                (a, b) => typeOrder.indexOf(a.type) - typeOrder.indexOf(b.type)
            );

            this.form.questions.forEach((group) => {
                group.ids.sort((a, b) => a - b);
            });
        },
        getPaginatedIds(group) {
            const start = (group.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return group.ids.slice(start, end);
        },
        handlePageChange(group, newPage) {
            group.currentPage = newPage;
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
</style>

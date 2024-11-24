<template>
    <v-banner sticky icon="mdi-vector-polyline-edit" lines="one">
        <template v-slot:text>
            <div class="text-subtitle-1">作为辅导师，你可查看/编辑/删除题目 - {{ this.id }}。</div>
        </template>

        <template v-slot:actions>
            <v-btn color="primary" class="mr-5" @click="goBack()">
                <div class="text-subtitle-1">返回</div>
            </v-btn>
            <v-btn color="error" class="mr-5" @click="confirmDelete">
                <div class="text-subtitle-1">删除该题目</div>
            </v-btn>
        </template>
    </v-banner>

    <v-tabs v-model="tab" color="primary">
        <v-tab v-for="tabItem in tabs" :key="tabItem.value" :value="tabItem.value"
            :disabled="isTabDisabled(tabItem.value)">
            {{ tabItem.label }}
        </v-tab>
    </v-tabs>

    <v-tabs-window v-model="tab" class="scroll-container mt-2">
        <v-tabs-window-item :value="1">
            <v-alert color="warning" class="mb-3" icon="mdi-chart-donut">
                <v-alert-title>预览原始题目</v-alert-title>
                以下是原始题目信息。如需更改，请点击“编辑基本信息”以开始。
            </v-alert>
            <v-row justify="start">
                <!-- 左侧内容区域，占 8 列（约 70%） -->
                <v-col cols="12" md="8">
                    <div>
                        <v-md-preview :text="originalExercise.content" v-if="originalExercise"></v-md-preview>
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
                                <span>{{ originalExercise.subject }}</span>
                            </div>
                            <div class="info-item">
                                <v-icon>mdi-comment-edit-outline</v-icon>
                                <span class="info-title">题型：</span>
                                <span>{{ originalExercise.questionType }}</span>
                            </div>
                            <div class="info-item">
                                <v-icon>mdi-source-branch</v-icon>
                                <span class="info-title">来源：</span>
                                <span>{{ originalExercise.source }}</span>
                            </div>
                            <div class="info-item">
                                <v-icon>mdi-tag</v-icon>
                                <span class="info-title">标签：</span>
                                <span>{{ originalExercise.tags }}</span>
                            </div>
                            <div class="info-item">
                                <v-icon>mdi-star-outline</v-icon>
                                <span class="info-title">难度：</span>
                                <span>{{ originalExercise.difficulty }}</span>
                            </div>
                        </v-card-text>
                    </v-card>
                    <v-card class="mt-4">
                        <v-card-title class="text-h6">答案</v-card-title>
                        <v-divider></v-divider>
                        <v-md-preview :text="originalExercise.answer" v-if="originalExercise"></v-md-preview>
                    </v-card>
                </v-col>
            </v-row>
        </v-tabs-window-item>

        <v-tabs-window-item :value="2">
            <!-- 设置基本信息 -->
            <v-form ref="formRef" @submit.prevent>
                <v-row no-gutters>
                    <!-- 学科选择 -->
                    <v-col cols="12">
                        <v-radio-group v-model="form.subject" label="学科" inline :rules="[value => !!value || '请选择学科']"
                            required>
                            <v-radio label="工科数学分析（上）" value="工科数学分析（上）" />
                            <v-radio label="工科数学分析（下）" value="工科数学分析（下）" />
                            <v-radio label="工科高等代数" value="工科高等代数" />
                            <v-radio label="离散数学（信息类）" value="离散数学（信息类）" />
                            <v-radio label="基础物理学A" value="基础物理学A" />
                        </v-radio-group>
                    </v-col>

                    <!-- 来源 -->
                    <v-col cols="12">
                        <v-text-field v-model="form.source" label="来源" outlined :rules="[value => !!value || '来源不能为空']"
                            required />
                    </v-col>

                    <!-- 标签 -->
                    <v-col cols="12">
                        <v-text-field v-model="form.tags" label="标签" outlined :rules="[value => !!value || '标签不能为空']"
                            required />
                    </v-col>

                    <!-- 难度选择 -->
                    <v-col cols="12">
                        <v-radio-group v-model="form.difficulty" label="难度" inline
                            :rules="[value => !!value || '请选择难度']" required>
                            <v-radio label="简单" value="简单" />
                            <v-radio label="中等" value="中等" />
                            <v-radio label="困难" value="困难" />
                        </v-radio-group>
                    </v-col>
                    <!-- 题型选择 -->
                    <v-col cols="12">
                        <v-radio-group v-model="form.questionType" label="题型" inline
                            :rules="[value => !!value || '请选择题型']" required>
                            <v-radio label="单项选择题" value="单项选择题" />
                            <v-radio label="多项选择题" value="多项选择题" />
                            <v-radio label="判断题" value="判断题" />
                            <v-radio label="填空题" value="填空题" />
                            <v-radio label="解答题" value="解答题" />
                        </v-radio-group>
                    </v-col>

                    <!-- 选项数量（仅在选择题时显示） -->
                    <v-col cols="12" v-if="isChoiceQuestion">
                        <v-text-field v-model.number="form.optionsCount" label="选项数量" type="number" outlined :rules="[
                            value => !!value || '选项数量不能为空',
                            value => Number.isInteger(Number(value)) || '选项数量必须是整数',
                            value => Number(value) >= 3 || '选项数量不能少于3个',
                            value => Number(value) <= 10 || '选项数量不能超过10个'
                        ]" required />
                    </v-col>
                </v-row>
            </v-form>
        </v-tabs-window-item>

        <v-tabs-window-item :value="3">
            <v-alert v-if="form.questionType === '单项选择题' || form.questionType === '多项选择题'" color="primary"
                icon="mdi-ab-testing">
                <v-alert-title>提示</v-alert-title>
                你选择的题型是"{{ form.questionType }}"，选项个数为{{ form.optionsCount }}。请在题面中加入对应数量的选项。
            </v-alert>
            <v-md-editor v-model="form.content" height="525px" width="20%"
                left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | link image code"
                right-toolbar="preview toc sync-scroll" :rules="[value => !!value || '题目内容不能为空']"
                required></v-md-editor>
        </v-tabs-window-item>

        <v-tabs-window-item :value="4">
            <v-alert
                v-if="form.questionType === '单项选择题' || form.questionType === '多项选择题' || form.questionType === '判断题'"
                color="primary" icon="mdi-ab-testing">
                <v-alert-title>提示</v-alert-title>
                你选择的题型是客观题型"{{ form.questionType }}"，选项个数为{{ form.optionsCount }}，请设置答案。
            </v-alert>
            <div v-if="form.questionType === '单项选择题'">
                <v-radio-group v-model="form.answer" :rules="[v => !!v || '请选择答案']" required>
                    <template v-for="n in form.optionsCount" :key="n">
                        <v-radio :label="String.fromCharCode(64 + n)" :value="String.fromCharCode(64 + n)"></v-radio>
                    </template>
                </v-radio-group>
            </div>

            <!-- 多项选择题 -->
            <div v-else-if="form.questionType === '多项选择题'">
                <v-row no-gutters>
                    <v-container>
                        <v-checkbox v-for="n in form.optionsCount" :key="n" v-model="selectedOptions"
                            :label="String.fromCharCode(64 + n)" :value="String.fromCharCode(64 + n)"
                            @change="updateMultipleAnswer" class="mb-2" />
                    </v-container>
                </v-row>
            </div>

            <!-- 判断题 -->
            <div v-else-if="form.questionType === '判断题'">
                <v-radio-group v-model="form.answer" :rules="[v => !!v || '请选择答案']" required>
                    <v-radio label="正确" value="正确"></v-radio>
                    <v-radio label="错误" value="错误"></v-radio>
                </v-radio-group>
            </div>
            <div v-else>
                <v-md-editor v-model="form.answer" height="525px" width="20%"
                    left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | link image code"
                    right-toolbar="preview toc sync-scroll" :rules="[value => !!value || '题目答案不能为空']"
                    required></v-md-editor>
            </div>
        </v-tabs-window-item>

        <v-tabs-window-item :value="5">
            <v-alert color="warning" class="mb-3" icon="mdi-circle-multiple-outline">
                <v-alert-title>确认</v-alert-title>
                请确认题目信息设置是否正确。若均填写正确，请点击下方提交按钮。
            </v-alert>
            <v-btn color="primary" variant="outlined" @click="handleSubmit">提交</v-btn>
            <v-row justify="start">
                <!-- 左侧内容区域，占 8 列（约 70%） -->
                <v-col cols="12" md="8">
                    <div>
                        <v-md-preview :text="form.content" v-if="form"></v-md-preview>
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
                                <span>{{ form.subject }}</span>
                            </div>
                            <div class="info-item">
                                <v-icon>mdi-comment-edit-outline</v-icon>
                                <span class="info-title">题型：</span>
                                <span>{{ form.questionType }}</span>
                            </div>
                            <div class="info-item">
                                <v-icon>mdi-source-branch</v-icon>
                                <span class="info-title">来源：</span>
                                <span>{{ form.source }}</span>
                            </div>
                            <div class="info-item">
                                <v-icon>mdi-tag</v-icon>
                                <span class="info-title">标签：</span>
                                <span>{{ form.tags }}</span>
                            </div>
                            <div class="info-item">
                                <v-icon>mdi-star-outline</v-icon>
                                <span class="info-title">难度：</span>
                                <span>{{ form.difficulty }}</span>
                            </div>
                        </v-card-text>
                    </v-card>
                    <v-card class="mt-4">
                        <v-card-title class="text-h6">答案</v-card-title>
                        <v-divider></v-divider>
                        <v-md-preview :text="form.answer" v-if="form"></v-md-preview>
                    </v-card>
                </v-col>
            </v-row>
        </v-tabs-window-item>
    </v-tabs-window>

    <v-dialog v-model="confirmDialogOpen" max-width="400px">
        <v-card>
            <v-card-title>
                <v-icon color="primary">mdi-alert-circle-outline</v-icon>
                <span class="headline ml-2">操作不可逆，确定删除题目吗？</span>
            </v-card-title>
            <v-card-actions>
                <v-btn color="red" variant="text" @click="deleteExercise">
                    确定
                </v-btn>
                <v-btn variant="plain" @click="confirmDialogOpen = false">
                    取消
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>

    <!-- Snackbar 提示 -->
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
import { mapMutations } from 'vuex';

export default {
    name: 'EditExercise',
    props: {
        id: {
            type: String,
            required: true,
        }
    },
    data() {
        return {
            currentId: null,
            tab: 1,
            tabs: [
                { value: 1, label: '原始题目' },
                { value: 2, label: '编辑基本信息' },
                { value: 3, label: '编辑题面' },
                { value: 4, label: '编辑答案' },
                { value: 5, label: '预览题目' },
            ],
            originalExercise: {},
            form: {
                subject: null,
                questionType: null,
                optionsCount: null,
                source: '',
                tags: '',
                content: '',
                answer: '',
                difficulty: null,
            },
            snackbar: {
                show: false,
                message: '',
                color: 'error'
            },
            selectedOptions: [],
            confirmDialogOpen: false,
        };
    },
    computed: {
        isChoiceQuestion() {
            return this.form.questionType === '单项选择题' || this.form.questionType === '多项选择题';
        }
    },
    mounted() {
        const title = '查看/编辑/删除题目 - ' + this.id;
        this.currentId = parseInt(this.id);
        console.log('接收到的 ID:', this.currentId);
        this.setAppTitle(title);
        this.setPageTitle(title);
        this.fetchExercise(this.currentId);
    },
    watch: {
        async tab(newTab, oldTab) {
            // 如果尝试切换到其他标签页（除了 "原始题目" 和 "编辑基本信息"），先验证表单
            if (![1, 2].includes(newTab)) {
                const isValid = await this.validateForm();
                if (!isValid) {
                    this.tab = oldTab; // 保持在当前标签页
                    return;
                }
            }
        },
        'form.questionType'(newValue) {
            // 当题型改变时，如果不是选择题，清空选项数量
            if (newValue !== '多项选择题' && newValue !== '单项选择题') {
                this.form.optionsCount = null;
            }
        },
        'form.questionType'() {
            this.selectedOptions = [];
            this.form.answer = this.originalExercise.answer;
        }
    },
    methods: {
        ...mapMutations(['setAppTitle', 'setPageTitle']),

        isTabDisabled(value) {
            if (this.tab === 1) {
                // 在 "原始题目" 时，只有 "编辑基本信息" 可以访问
                return value !== 1 && value !== 2;
            }
            return false; // 其他情况下，所有标签都可访问
        },

        currentTabIsOriginal() {
            return this.tab === 1;
        },

        fetchExercise(problemId) {
            // 模拟直接从后端获取数据
            const mockProblemData = {
                id: problemId,
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
                optionsCount: 4,
            };

            this.form = { ...mockProblemData };
            console.log(this.form);
            this.originalExercise = { ...mockProblemData };
        },

        goBack() {
            this.$router.push("/admin/exercise");
        },

        deleteExercise() {
            // TODO: 添加删除逻辑
            console.log('删除题目 ID:', this.currentId);
            this.showSnackbar('题目已删除', 'success');
            this.goBack();
        },

        showSnackbar(message, color = 'error') {
            this.snackbar = {
                show: true,
                message,
                color
            };
        },

        updateMultipleAnswer() {
            // 将选中的选项排序并转换为字符串
            this.form.answer = this.selectedOptions.sort().join(',')
        },

        confirmDelete() {
            this.confirmDialogOpen = true;
        },

        async validateForm() {
            try {
                const { valid } = await this.$refs.formRef.validate();
                if (!valid) {
                    this.showSnackbar('请填写所有必填字段！');
                }
                return valid;
            } catch (error) {
                console.error('表单验证出错：', error);
                this.showSnackbar('表单验证出错');
                return false;
            }
        },

        async handleSubmit() {
            // 验证表单
            const isValid = await this.validateForm();

            if (!isValid) {
                this.tab = 2;
                return;
            }

            // 验证题目内容是否为空
            if (!this.form.content) {
                this.showSnackbar('题目内容不能为空');
                this.tab = 3;
                return;
            }

            if (!this.form.answer) {
                this.showSnackbar('题目答案不能为空');
                this.tab = 4;
                return;
            }

            try {
                // TODO: 在这里添加实际的表单提交逻辑
                console.log(this.form);
                this.showSnackbar('题目已提交', 'success');
                this.goBack();
            } catch (error) {
                console.error('表单提交出错：', error);
                this.showSnackbar('表单提交失败');
            }
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

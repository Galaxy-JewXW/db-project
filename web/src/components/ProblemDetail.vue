<template>
  <v-container fluid>
    <v-row justify="start">
      <!-- 左侧内容区域，占 8 列（约 70%） -->
      <v-col cols="12" md="8">
        <div class="markdown-container">
          <v-md-preview
            :text="problem.content"
            class="markdown-content"
            v-if="problem"
          ></v-md-preview>
        </div>
      </v-col>

      <!-- 右侧卡片区域，占 4 列（约 30%） -->
      <v-col cols="12" md="4">
        <v-card class="info-card" outlined>
          <v-card-text class="card-text">
            <div class="problem-header" v-if="problem">
              <h1>题目 - {{ problem.id }}</h1>
              <v-chip class="ma-2 chip-item" color="primary" variant="outlined">
                {{ problem.type }}
              </v-chip>
            </div>

            <!-- 添加题目相关信息 -->
            <div class="info-item">
              <v-icon>mdi-school</v-icon>
              <span class="info-title">学科：</span>
              <span>{{ problem.subject }}</span>
            </div>
            <div class="info-item">
              <v-icon>mdi-calendar</v-icon>
              <span class="info-title">添加时间：</span>
              <span>{{ problem.addedAt }}</span>
            </div>
            <div class="info-item">
              <v-icon>mdi-source-branch</v-icon>
              <span class="info-title">来源：</span>
              <span>{{ problem.source }}</span>
            </div>
            <div class="info-item">
              <v-icon>mdi-tag</v-icon>
              <span class="info-title">标签：</span>
              <span>{{ problem.tags.join(', ') }}</span>
            </div>
            <div class="info-item">
              <v-icon>mdi-star-outline</v-icon>
              <span class="info-title">难度：</span>
              <span>{{ problem.difficulty }}</span>
            </div>

            <!-- 按钮区域，放置在同一行 -->
            <v-row class="ma-2">
              <v-col cols="6">
                <v-btn
                  prepend-icon="mdi-lightbulb"
                  color="primary"
                  @click="viewAnswer"
                  block
                >
                  查看答案
                </v-btn>
              </v-col>
              <v-col cols="6">
                <v-btn
                  prepend-icon="mdi-comment-text"
                  color="secondary"
                  @click="viewDiscussion"
                  block
                >
                  相关讨论
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 答案对话框 -->
    <v-dialog
      v-model="dialog"
      transition="dialog-bottom-transition"
      fullscreen
    >
      <v-card>
        <v-toolbar dark color="primary">
          <v-btn icon @click="closeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>答案</v-toolbar-title>
        </v-toolbar>

        <!-- 根据用户选择显示内容 -->
        <div v-if="!answerResult">
          <!-- 做对了、做错了按钮 -->
          <v-card flat elevation="0" class="ma-4" style="max-width: 100%;">
            <v-card-title class="headline text-h5 font-weight-bold">你做对了吗？</v-card-title>
            <v-card-text class="d-flex justify-start">
              <v-btn color="success" class="ma-2" outlined @click="handleAnswer(true)">
                <v-icon left>mdi-check</v-icon> 做对了
              </v-btn>
              <v-btn color="error" class="ma-2" outlined @click="handleAnswer(false)">
                <v-icon left>mdi-close</v-icon> 做错了
              </v-btn>
            </v-card-text>
          </v-card>
        </div>
        <div v-else>
          <!-- 显示对应的提示信息 -->
          <v-alert
            :type="answerResult === 'correct' ? 'success' : 'error'"
            class="ma-4"
            title="回答情况已记录"
            style="max-width: 100%;"
          >
            {{ alertMessage }}
          </v-alert>
        </div>

        <!-- Markdown 内容显示区域 -->
        <v-card-text>
          <div class="markdown-content" v-if="answer">
            <v-md-preview :text="answer" />
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { mapMutations } from "vuex";

export default {
  name: "ProblemDetail",
  data() {
    return {
      problem: null, // 存储题目信息
      dialog: false, // 控制答案弹框显示与隐藏
      answer: null, // 存储答案内容
      answerResult: null, // 存储用户的答案结果
      alertMessage: "", // 存储提示信息
    };
  },
  created() {
    const problemId = this.$route.params.id;
    this.fetchProblemData(problemId);
  },
  methods: {
    ...mapMutations(["setAppTitle", "setPageTitle"]),

    // 获取题目信息
    fetchProblemData(problemId) {
      // 模拟直接从后端获取数据
      const mockProblemData = {
        id: problemId,
        type: "单项选择题",
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
        subject: "计算机科学",
        addedAt: "2024-10-12",
        source: "自出题",
        tags: ["算法", "数据结构"],
        difficulty: "中等",
      };

      this.problem = mockProblemData;

      // 使用 Vuex 更新 appTitle 和 pageTitle
      const title = `题目详情 - ${problemId}`;
      this.setAppTitle(title);
      this.setPageTitle(title);
    },

    // 查看答案
    viewAnswer() {
      // 模拟从后端获取答案内容
      const mockAnswerData = `
# 答案

这是题目的答案部分，包含详细的解答步骤和说明。
`;

      this.answer = mockAnswerData;
      this.dialog = true;
    },

    viewDiscussion() {
      console.log("相关讨论");
    },

    // 处理用户点击“做对了”或“做错了”
    handleAnswer(isCorrect) {
      if (isCorrect) {
        this.answerResult = 'correct';
        this.alertMessage = '恭喜你，回答正确！';
      } else {
        this.answerResult = 'incorrect';
        this.alertMessage = '别灰心，下次再接再厉！';
      }
    },

    // 关闭对话框并重置状态
    closeDialog() {
      this.dialog = false;
      this.answerResult = null;
    },
  },
};
</script>

<style scoped>
h1 {
  margin-bottom: 8px;
  text-align: left;
}

.problem-header {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: flex-start;
}

.chip-item {
  display: flex;
  align-items: center;
  margin: 0;
}

.markdown-container {
  max-height: calc(100vh - 150px);
  overflow-y: auto;
  margin-left: -29px;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.markdown-container::-webkit-scrollbar {
  display: none;
}

.markdown-content {
  margin-top: 16px;
  text-align: left;
  overflow-wrap: break-word;
  word-wrap: break-word;
}

.info-card {
  height: 60%;
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

.v-dialog {
  z-index: 200;
}

/* 隐藏 v-card 的边框 */
.v-card {
  border: none;
}
</style>

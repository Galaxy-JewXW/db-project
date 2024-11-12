<template>
  <v-container fluid class="problem-container">
    <v-row>
      <!-- 主内容区域 -->
      <v-col cols="12" md="9" class="main-content">
        <div class="problem-header" v-if="problem">
          <h1>题目 - {{ problem.id }}</h1>
          <v-chip class="ma-2 chip-item" color="primary" variant="outlined">
            {{ problem.type }}
          </v-chip>
        </div>
        <div class="markdown-container">
          <v-md-preview :text="problem.content" class="markdown-content" v-if="problem"></v-md-preview>
        </div>
      </v-col>

      <!-- 侧边栏区域 -->
      <v-col cols="12" md="3" class="sidebar no-scrollbar">
        <v-card>
          <v-card-title>其他板块</v-card-title>
          <v-card-text>
            <!-- 在这里添加你需要的内容 -->
            <p>这是侧边栏的占位内容。</p>
            <v-list>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>板块 1</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>板块 2</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>板块 3</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapMutations } from 'vuex';

export default {
  name: "ProblemDetail",
  data() {
    return {
      problem: null, // 存储题目信息
    };
  },
  created() {
    const problemId = this.$route.params.id;
    this.fetchProblemData(problemId);
  },
  methods: {
    ...mapMutations(["setAppTitle", "setPageTitle"]),
    fetchProblemData(problemId) {
      // 模拟直接从后端获取数据
      const mockProblemData = {
        id: problemId,
        type: "选择题", // 示例类型
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
      };

      this.problem = mockProblemData;

      // 使用 Vuex 更新 appTitle 和 pageTitle
      const title = `题目详情 - ${problemId}`;
      this.setAppTitle(title);
      this.setPageTitle(title);
    },
  },
};
</script>

<style scoped>
.problem-container {
  display: flex;
  height: 100vh;
  padding: 16px;
  box-sizing: border-box;
}

.main-content {
  display: flex;
  flex-direction: column;
  height: 100%;
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
  flex: 1;
  overflow-y: auto;
  margin-top: 16px;
  scrollbar-width: none;
  /* Firefox */
  -ms-overflow-style: none;
  /* IE and Edge */
}

.markdown-container::-webkit-scrollbar {
  display: none;
  /* Chrome, Safari, and Opera */
}

.markdown-content {
  text-align: left;
  overflow-wrap: break-word;
  word-wrap: break-word;
}

.sidebar {
  display: flex;
  flex-direction: column;
  height: 80%;
  padding-left: 16px;
  box-sizing: border-box;
}

.v-card {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.v-card-title {
  font-weight: bold;
}

.v-card-text {
  flex: 1;
  overflow-y: auto;
}

.no-scrollbar {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

.no-scrollbar::-webkit-scrollbar {
  width: 0;
  height: 0;
}
</style>

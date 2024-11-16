<template>
  <div class="scroll-container">
    <v-card class="mx-auto" max-width="85%">
      <v-card-item
        prepend-avatar="https://randomuser.me/api/portraits/women/85.jpg"
      >
        <v-card-item-title class="text-h6 font-weight-regular">
          <v-row align="center" no-gutters>
            <v-col cols="auto">
              {{ discussion.publisher }}
            </v-col>
          </v-row>
        </v-card-item-title>
        <v-card-item-subtitle>
          <v-row align="center" no-gutters>
            <v-col cols="auto" class="text-body-1 text-disabled">
              {{ formatDate(discussion.publishTime) }}
            </v-col>
          </v-row>
        </v-card-item-subtitle>
      </v-card-item>
      <v-card-text>
        <v-divider style="padding-top: 10px; padding-bottom: 0px"></v-divider>
        <!-- 显示内容 -->
        <div style="margin-left: -29px">
          <v-md-preview :text="discussion.content"></v-md-preview>
        </div>
      </v-card-text>
    </v-card>
  </div>
  <v-btn class="floating-btn" fab color="primary" @click="returnForum()">
    <v-icon size="32">mdi-arrow-collapse-left</v-icon>
  </v-btn>
</template>

<script>
import { mapMutations } from "vuex"; // 引入 mapMutations

export default {
  name: "ForumContent",
  data() {
    return {
      // 定义 discussion 数据
      discussion: {
        id: 2,
        title: "离散数学在计算机科学中的应用",
        publisher: "李四",
        publishTime: "2024-09-25T15:30:00",
        lastUpdated: "2024-11-15T15:30:00",
        tag: "离散数学（信息类）",
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
      },
    };
  },
  mounted() {
    // 更新标题
    const title = `讨论 - ${this.discussion.title}`; // 动态设置标题
    this.setAppTitle(title); // 设置应用的标题
    this.setPageTitle(title); // 设置页面的标题
  },
  methods: {
    ...mapMutations(["setAppTitle", "setPageTitle"]),
    formatDate(dateStr) {
      const options = {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      };
      return new Date(dateStr).toLocaleString(undefined, options);
    },
    returnForum() {
      this.$router.push(`/forum`);
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
  height: 98vh;
  max-height: 98vh;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scroll-container::-webkit-scrollbar {
  display: none;
}

.floating-btn {
  position: fixed;
  right: 4%;
  bottom: 10%;
  z-index: 9999;
  border-radius: 75%;
  width: 64px;
  height: 64px;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
}

.v-icon {
  color: white;
}
</style>

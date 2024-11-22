<template>
  <div>
    <v-card class="mx-auto my-5" max-width="70%">
      <v-card-title>
        <span class="text-h5 font-weight-bold">个人信息</span>
      </v-card-title>

      <v-divider></v-divider>

      <!-- 卡片内容 -->
      <v-card-text>
        <v-row>
          <!-- 左侧：头像和上传按钮 -->
          <v-col cols="12" md="4" class="text-center">
            <v-avatar size="120">
              <img :src="userAvatar" alt="用户头像" />
            </v-avatar>
            <v-divider class="my-6"></v-divider>
            <v-btn color="primary" prepend-icon="mdi-lead-pencil" @click="uploadAvatar">上传新头像</v-btn>
          </v-col>

          <!-- 右侧：个人信息 -->
          <!-- 昵称 -->
          <v-col cols="12" md="8">
            <v-row class="mb-3 text-subtitle-1" align="center">
              <v-col cols="1">
                <v-icon>mdi-account-box</v-icon>
              </v-col>
              <v-col cols="3">
                <strong>昵称</strong>
              </v-col>
              <v-col cols="8" class="text-subtitle-1">
                <!-- 调大字体 -->
                {{ userName }}
              </v-col>
            </v-row>

            <!-- 学工号 -->
            <v-row class="mb-3 text-subtitle-1" align="center">
              <v-col cols="1">
                <v-icon>mdi-card-account-details</v-icon>
              </v-col>
              <v-col cols="3">
                <strong>学工号</strong>
              </v-col>
              <v-col cols="8" class="text-subtitle-1">
                <!-- 调大字体 -->
                {{ userNumber }}
              </v-col>
            </v-row>

            <!-- 学院/书院 -->
            <v-row class="mb-3 text-subtitle-1" align="center">
              <v-col cols="1">
                <v-icon>mdi-school</v-icon>
              </v-col>
              <v-col cols="3">
                <strong>学院/书院</strong>
              </v-col>
              <v-col cols="8" class="text-subtitle-1">
                <!-- 调大字体 -->
                {{ userCollege }}
              </v-col>
            </v-row>

            <!-- 入学年份 -->
            <v-row class="mb-3 text-subtitle-1" align="center">
              <v-col cols="1">
                <v-icon>mdi-calendar</v-icon>
              </v-col>
              <v-col cols="3">
                <strong>入学年份</strong>
              </v-col>
              <v-col cols="8" class="text-subtitle-1">
                <!-- 调大字体 -->
                {{ userEntryYear }}
              </v-col>
            </v-row>

            <!-- 邮箱 -->
            <v-row class="mb-3 text-subtitle-1" align="center">
              <v-col cols="1">
                <v-icon>mdi-email</v-icon>
              </v-col>
              <v-col cols="3">
                <strong>邮箱</strong>
              </v-col>
              <v-col cols="8" class="text-subtitle-1">
                <!-- 调大字体 -->
                {{ userEmail }}
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>

      <!-- 卡片操作 -->
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="dialog = true">修改个人信息</v-btn>
      </v-card-actions>
    </v-card>

    <!-- 修改个人信息的 v-dialog -->
    <v-dialog v-model="dialog" max-width="600px" persistent>
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon class="mr-2">mdi-account-edit</v-icon>
          <span class="headline">修改个人信息</span>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-row dense>
              <!-- 昵称 -->
              <v-col cols="12">
                <v-text-field
                  label="昵称"
                  v-model="formData.username"
                  :rules="nameRules"
                  variant="outlined"
                  validate-on-blur
                ></v-text-field>
              </v-col>

              <!-- 学工号 -->
              <v-col cols="12">
                <v-text-field
                  label="学工号"
                  v-model="this.studentNumber"
                  variant="outlined"
                  hint="学工号不可修改"
                  persistent-hint
                  disabled
                ></v-text-field>
              </v-col>

              <!-- 学院/书院 -->
              <v-col cols="12">
                <v-autocomplete
                  clearable
                  label="学院/书院"
                  v-model="formData.college"
                  :items="colleges"
                  :rules="collegeRules"
                  variant="outlined"
                  validate-on-blur
                ></v-autocomplete>
              </v-col>

              <!-- 入学年份 -->
              <v-col cols="12">
                <v-select
                  :items="entryYears"
                  label="入学年份"
                  v-model="formData.enrollmentYear"
                  :rules="entryYearRules"
                  variant="outlined"
                  validate-on-blur
                ></v-select>
              </v-col>

              <!-- 邮箱 -->
              <v-col cols="12">
                <v-text-field
                  label="邮箱"
                  v-model="formData.email"
                  :rules="emailRules"
                  variant="outlined"
                  validate-on-blur
                  hint="请输入有效的邮箱地址"
                  persistent-hint
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text="取消" @click="dialog = false"></v-btn>
          <v-btn text="清除" @click="handleClear"></v-btn>
          <v-btn
            color="primary"
            text="保存"
            :disabled="!valid"
            @click="submitForm"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapMutations, mapState } from "vuex"; // 引入 mapMutations

export default {
  name: "ProfileContent",
  data() {
    return {
      // 用户信息
      avatar: "https://randomuser.me/api/portraits/women/85.jpg",
      username: "时间的彷徨",
      studentNumber: 22373300,
      college: "1",
      enrollmentYear: "2021",
      email: "pigkiller@gmail.com",

      // 对话框控制
      dialog: false,
      valid: false,

      // 表单数据
      formData: {
        username: "时间的彷徨",
        college: "1",
        enrollmentYear: "2021",
        email: "pigkiller@gmail.com",
      },

      // 入学年份选项
      entryYears: [],

      // 学院/书院列表
      colleges: [
        "材料科学与工程学院",
        "电子信息工程学院",
        "自动化科学与电气工程学院",
        "能源与动力工程学院",
        "航空科学与工程学院",
        "计算机学院",
        "机械工程及自动化学院",
        "经济管理学院",
        "数学科学学院",
        "生物与医学工程学院",
        "人文社会科学学院（公共管理学院）",
        "外国语学院",
        "交通科学与工程学院",
        "可靠性与系统工程学院",
        "宇航学院",
        "飞行学院",
        "仪器科学与光电工程学院",
        "北京学院",
        "物理学院",
        "法学院",
        "软件学院",
        "未来空天技术学院/高等理工学院（沈元学院）",
        "中法工程师学院",
        "国际学院",
        "新媒体艺术与设计学院",
        "化学学院",
        "马克思主义学院",
        "人文与社会科学高等研究院",
        "空间与环境学院",
        "无人系统研究院",
        "航空发动机研究院",
        "国际通用工程学院/国际交叉科学研究院",
        "传源书院",
        "士谔书院",
        "冯如书院",
        "士嘉书院",
        "守锷书院",
        "致真书院",
        "知行书院",
        "医学科学与工程学院/医工交叉创新研究院",
        "网络空间安全学院",
        "集成电路科学与工程学院",
        "人工智能研究院",
        "前沿科学技术创新研究院",
      ],

      // 验证规则
      nameRules: [(v) => !!v || "昵称是必填项。"],
      collegeRules: [(v) => !!v || "学院/书院是必填项。"],
      emailRules: [
        (v) => !!v || "邮箱是必填项。",
        (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || "请输入有效的邮箱地址。",
      ],
      entryYearRules: [(v) => !!v || "入学年份是必填项。"],
    };
  },
  mounted() {
    // 初始化入学年份
    this.entryYears = this.getEntryYears();

    // 更新标题
    const title = "个人中心";
    this.setAppTitle(title);
    this.setPageTitle(title);
  },
  computed: {
    ...mapState(["user", "userId"]),
    userAvatar() {
      return this.user && this.user.urls
        ? this.user.urls
        : "https://randomuser.me/api/portraits/lego/1.jpg";
    },
    userName() {
      const name = this.user && this.user.name ? this.user.name : "error";
      this.formData.username = name;
      return name;
    },
    userNumber() {
      const number = this.user && this.userId ? this.userId : -1;
      this.studentNumber = number;
      return number;
    },
    userCollege() {
      const college = this.user && this.user.college ? this.user.college : "error";
      this.formData.college = college;
      return college;
    },
    userEntryYear() {
      const entryYear = this.user && this.user.entry_year ? this.user.entry_year : "error";
      this.formData.enrollmentYear = entryYear;
      return entryYear;
    },
    userEmail() {
      const email = this.user && this.user.email ? this.user.email : "error";
      this.formData.email = email;
      return email;
    }
  },
  methods: {
    ...mapMutations(["setAppTitle", "setPageTitle"]), // 映射 Vuex 的 mutations

    // 生成从当前年份向前 10 年的入学年份列表
    getEntryYears() {
      const currentYear = new Date().getFullYear();
      const years = [];
      for (let i = 0; i < 10; i++) {
        years.push(currentYear - i);
      }
      return years;
    },

    // 提交表单数据
    submitForm() {
      if (this.$refs.form.validate()) {
        // 更新用户信息
        this.username = this.formData.username;
        this.college = this.formData.college;
        this.enrollmentYear = this.formData.enrollmentYear;
        this.email = this.formData.email;

        // 关闭对话框
        this.dialog = false;

        // 清除表单
        this.handleClear();

        // 可以在这里调用 API 或者 Vuex action 来保存修改到后端
        console.log("个人信息已更新:", {
          username: this.username,
          college: this.college,
          enrollmentYear: this.enrollmentYear,
          email: this.email,
        });
      } else {
        console.log("表单验证失败");
      }
    },

    // 清空表单内容
    handleClear() {
      this.formData = {
        username: this.username,
        college: this.college,
        enrollmentYear: this.enrollmentYear,
        email: this.email,
      };
      this.$refs.form.resetValidation();
    },

    // 上传头像
    uploadAvatar() {
      // 实现上传头像的逻辑
      const fileInput = document.createElement("input");
      fileInput.type = "file";
      fileInput.accept = "image/*";
      fileInput.onchange = (e) => {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (event) => {
            this.avatar = event.target.result;
            console.log("新头像已上传");
          };
          reader.readAsDataURL(file);
        }
      };
      fileInput.click();
    },
  },
};
</script>

<style scoped>
.v-form {
  width: 100%;
}

.mb-2 {
  margin-bottom: 16px;
}

.w-100 {
  width: 100%;
}

.card-spacing {
  margin-top: 16px;
  margin-bottom: 24px;
}

.custom-title {
  font-size: 32px;
  font-weight: 500;
  margin-bottom: 12px;
}

.custom-subtitle {
  font-size: 16px;
  font-weight: 400;
  color: #757575;
  margin-bottom: 24px;
}

.card-spacing {
  padding-left: 0;
}

.no-border {
  border: none;
}

.field-spacing {
  margin-bottom: -16px;
}

.no-scrollbar {
  scrollbar-width: none;
}

.no-scrollbar::-webkit-scrollbar {
  width: 0;
  height: 0;
}
</style>

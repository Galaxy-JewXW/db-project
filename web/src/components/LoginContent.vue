<template>
  <div>
    <div class="card-spacing no-border">
      <!-- 自定义标题和副标题，使用 h2 和 h3 标签 -->
      <h2 class="custom-title">欢迎回来。</h2>
      <h3 class="custom-subtitle">要继续使用本系统，请使用您的账号登录。</h3>
    </div>

    <!-- 登录表单 -->
    <v-form ref="loginForm" v-model="isLoginValid" @submit.prevent="submitLogin" @keyup.enter="submitLogin">
      <v-row>
        <!-- 学工号输入字段 -->
        <v-col cols="12" class="field-spacing">
          <v-text-field v-model="studentNumber.value" :rules="studentNumberRules" label="学工号" type="text"
            prepend-inner-icon="mdi-account" variant="outlined" validate-on-blur persistent-hint></v-text-field>
        </v-col>

        <!-- 密码输入字段 -->
        <v-col cols="12" class="field-spacing">
          <v-text-field v-model="password.value" :rules="passwordRules" label="密码" type="password"
            prepend-inner-icon="mdi-lock" variant="outlined" validate-on-blur persistent-hint></v-text-field>
        </v-col>

        <!-- 按钮区域 -->
        <v-col cols="12">
          <!-- 登录按钮 -->
          <v-btn class="w-100 mb-2" :disabled="!isLoginValid" color="primary" @click="submitLogin">
            登录
          </v-btn>

          <!-- 注册按钮 -->
          <v-btn class="w-100" variant="outlined" @click="dialog = true" color="info">
            没有账号？注册
          </v-btn>
        </v-col>
      </v-row>
    </v-form>

    <!-- 注册对话框 -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card prepend-icon="mdi-account-plus" title="快加入我们！" subtitle="要继续注册，请填写以下个人信息。" class="no-scrollbar">
        <v-card-text>
          <v-form ref="registerForm" v-model="isRegisterValid">
            <v-row dense>
              <!-- 姓名/昵称 -->
              <v-col cols="12">
                <v-text-field label="昵称" v-model="name" :rules="nameRules" variant="outlined"
                  validate-on-blur></v-text-field>
              </v-col>

              <!-- 学工号 -->
              <v-col cols="12">
                <v-text-field label="学工号" v-model="studentNumberReg" :rules="studentNumberRegRules" variant="outlined"
                  validate-on-blur hint="学工号在注册完成后无法更改，敬请留意。" persistent-hint></v-text-field>
              </v-col>

              <!-- 学院/书院 -->
              <v-col cols="12">
                <v-autocomplete clearable label="学院/书院" v-model="college" :items="colleges" :rules="collegeRules"
                  variant="outlined" validate-on-blur></v-autocomplete>
              </v-col>

              <!-- 邮箱 -->
              <v-col cols="12">
                <v-text-field label="邮箱" v-model="email" :rules="emailRules" variant="outlined" validate-on-blur
                  hint="请输入有效的邮箱地址" persistent-hint></v-text-field>
              </v-col>

              <!-- 入学年份 -->
              <v-col cols="12">
                <v-select :items="entryYears" label="入学年份" v-model="entryYear" :rules="entryYearRules"
                  variant="outlined" validate-on-blur></v-select>
              </v-col>

              <!-- 密码 -->
              <v-col cols="12">
                <v-text-field label="密码" v-model="passwordReg" :rules="passwordRegRules" type="password"
                  variant="outlined" validate-on-blur hint="密码长度至少为6位" persistent-hint></v-text-field>
              </v-col>

              <!-- 确认密码 -->
              <v-col cols="12">
                <v-text-field label="确认密码" v-model="confirmPassword" :rules="confirmPasswordRules" type="password"
                  variant="outlined" validate-on-blur></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text="已有账号？登录" variant="plain" @click="dialog = false"></v-btn>
          <v-btn text="清除" variant="plain" @click="handleClear"></v-btn>
          <v-btn color="primary" text="注册" variant="tonal" :disabled="!isRegisterValid" @click="handleRegister"></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapMutations, mapActions } from "vuex"; // 引入 mapMutations
import axios from "axios";
export default {
  name: "LoginContent",
  data() {
    return {
      // 登录表单
      isLoginValid: false,
      studentNumber: {
        value: "",
      },
      password: {
        value: "",
      },
      // 注册对话框
      dialog: false,
      isRegisterValid: false,
      name: "",
      studentNumberReg: "",
      college: "",
      email: "",
      entryYear: "",
      passwordReg: "",
      confirmPassword: "",
      role: "",
      // 入学年份选项
      entryYears: [],
      avatar: "",
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
      studentNumberRules: [
        (v) => !!v || "学工号是必填项。",
      ],
      passwordRules: [
        (v) => !!v || "密码是必填项。",
        (v) => (v && v.length >= 6) || "密码长度至少为6位。",
      ],
      studentNumberRegRules: [
        (v) => !!v || "学工号是必填项。",
      ],
      collegeRules: [(v) => !!v || "学院/书院是必填项。"],
      emailRules: [
        (v) => !!v || "邮箱是必填项。",
        (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || "请输入有效的邮箱地址。",
      ],
      entryYearRules: [(v) => !!v || "入学年份是必填项。"],
      passwordRegRules: [
        (v) => !!v || "密码是必填项。",
        (v) => (v && v.length >= 6) || "密码长度至少为6位。",
      ],
      confirmPasswordRules: [
        (v) => !!v || "确认密码是必填项。",
        (v) => v === this.passwordReg || "两次输入的密码不一致。",
      ],

    };
  },
  mounted() {
    // 初始化入学年份
    this.entryYears = this.getEntryYears();

    // 初始推算入学年份
    this.calculateEntryYear(this.studentNumberReg);

    // 更新标题
    const title = "登录";
    this.setAppTitle(title);
    this.setPageTitle(title);
    this.showSnackbar({
      message: '你必须先登录，才能访问本系统内容',
      color: 'warning',
      timeout: 2000
    });
  },
  watch: {
    studentNumberReg(val) {
      this.calculateEntryYear(val);
      // 重新验证表单以反映变化
      this.$refs.registerForm.validate();
    },
    passwordReg(val) {
      // 当密码变化时，重新验证确认密码
      this.$refs.registerForm.validate();
    },
    confirmPassword(val) {
      // 当确认密码变化时，重新验证确认密码
      this.$refs.registerForm.validate();
    },
  },
  methods: {
    ...mapMutations(["setAppTitle", "setPageTitle", "setUserId", "setUserInfo"]), // 映射 Vuex 的 mutations
    ...mapActions('snackbar', ['showSnackbar']),
    // 生成从当前年份向前 10 年的入学年份列表
    getEntryYears() {
      const currentYear = new Date().getFullYear();
      const years = [];
      for (let i = 0; i < 10; i++) {
        years.push(currentYear - i);
      }
      return years;
    },
    // 提交登录表单
    submitLogin() {
      if (!this.isLoginValid) {
        this.showSnackbar({
          message: "账户名或密码错误",
          color: 'error',
          timeout: 2000
        });
        return;
      }
      if (this.$refs.loginForm.validate()) {
        const loginData = {
          studentNumber: this.studentNumber.value,
          password: this.password.value,
        };
        axios
          .post("http://127.0.0.1:8000/api/myapp2/login/", loginData)
          .then((response) => {
            const token = this.studentNumber.value;
            const user = response.data;
            this.showSnackbar({
              message: `欢迎你，${user.name}！`,
              color: 'success',
              timeout: 2000
            });
            console.log(user);
            this.setUserId(token);
            this.setUserInfo(user);
            axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
            this.$router.push("/home");
          })
          .catch((error) => {
            this.showSnackbar({
              message: error.response.data.message,
              color: 'error',
              timeout: 2000
            });
          });
      } else {
        this.showSnackbar({
          message: '表单验证失败',
          color: 'error',
          timeout: 2000
        });
      }
    },
    handleResetLogin() {
      this.studentNumber.value = "";
      this.password.value = "";
      this.$refs.loginForm.resetValidation();
    },
    // 提交注册表单
    handleRegister() {
      if (this.$refs.registerForm.validate()) {
        const registerData = {
          name: this.name,
          studentNumber: this.studentNumberReg,
          college: this.college,
          email: this.email,
          entryYear: this.entryYear,
          password: this.passwordReg,
          confirmPassword: this.confirmPassword,
        }
        console.log("注册表单已提交:", registerData);
        axios
          .post("http://127.0.0.1:8000/api/myapp2/register/", registerData)
          .then((response) => {
            this.showSnackbar({
              message: '注册成功',
              color: 'success',
              timeout: 2000
            });
            this.dialog = false;
            this.studentNumber.value = this.studentNumberReg;
            this.password.value = this.confirmPassword;
          })
          .catch((error) => {
            this.showSnackbar({
              message: error.response.data.message,
              color: 'error',
              timeout: 2000
            });
          });
      } else {
        this.showSnackbar({
          message: '注册验证失败',
          color: 'error',
          timeout: 2000
        });
      }
    },
    // 清空注册表单内容
    handleClear() {
      this.name = "";
      this.studentNumberReg = "";
      this.college = "";
      this.email = "";
      this.entryYear = "";
      this.passwordReg = "";
      this.confirmPassword = "";
      this.$refs.registerForm.resetValidation();
    },
    // 根据学工号推算入学年份
    calculateEntryYear(studentNumber) {
      if (/^\d{8}$/.test(studentNumber)) {
        const yearPrefix = studentNumber.substring(0, 2);
        const currentYear = new Date().getFullYear();
        let fullYear = parseInt(`20${yearPrefix}`, 10);

        // 处理可能的年份范围（例如，避免推算出未来的年份）
        if (fullYear > currentYear) {
          fullYear -= 100; // 假设年份为1900年代
        }

        // 检查推算出的年份是否在入学年份选项中
        if (this.entryYears.includes(fullYear)) {
          this.entryYear = fullYear;
        } else {
          this.entryYear = "";
        }
      } else {
        this.entryYear = "";
      }
    },
  },
};
</script>

<style scoped>
/* 确保表单占满父容器的宽度 */
.v-form {
  width: 100%;
}

/* 调整按钮的下边距，确保按钮之间有间距 */
.mb-2 {
  margin-bottom: 16px;
}

/* 确保按钮占满宽度 */
.w-100 {
  width: 100%;
}

/* 增加标题和表单之间的间隔 */
.card-spacing {
  margin-top: 16px;
  margin-bottom: 24px;
}

/* 自定义 h2 和 h3 的样式 */
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

/* 左对齐标题和输入框 */
.card-spacing {
  padding-left: 0;
}

/* 移除 v-card 的边框（如果使用 v-card 时需要） */
.no-border {
  border: none;
}

/* 调整输入框之间的间距 */
.field-spacing {
  margin-bottom: -16px;
}

.no-scrollbar {
  scrollbar-width: none;
  /* Firefox */
  -ms-overflow-style: none;
  /* IE and Edge */
}

.no-scrollbar::-webkit-scrollbar {
  width: 0;
  height: 0;
}
</style>

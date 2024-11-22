<template>
    <v-card class="mx-auto my-12" max-width="60%" outlined>
      <v-card-title class="headline font-weight-bold text-h4">
        <v-icon color="error" large class="mr-3">mdi-alert-circle-outline</v-icon>
        未授权
      </v-card-title>
      <v-card-text class="text-h6">
        <p>你没有权限访问此页面。</p>
        <p>如果你认为这是系统错误，请联系我们。</p>
      </v-card-text>
      <v-card-actions class="justify-center">
        <v-btn color="error" class="w-100 text-subtitle-1" @click="goHome">
          返回首页
        </v-btn>
      </v-card-actions>
    </v-card>
  </template>
  
  <script>
  import { mapMutations } from "vuex";
  
  export default {
    mounted() {
      const title = "无权限";
      this.setAppTitle(title);
      this.setPageTitle(title);
    },
    methods: {
      ...mapMutations(["setAppTitle", "setPageTitle"]),
      goHome() {
        this.$router.push("/");
      },
    },
  };
  </script>
  
  <style scoped>
  .text-subtitle-1 {
    font-size: 20px;
  }
  </style>
  
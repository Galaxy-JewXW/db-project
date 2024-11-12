// router/index.js
import { createRouter, createWebHistory } from "vue-router";
import { routes as autoRoutes } from "vue-router/auto-routes";
import NotFound from "@/components/NotFound.vue"; // 导入 404 页面组件

// 手动添加的自定义路由
const customRoutes = [
  {
    path: "/problemset/:id",
    name: "ProblemSetDetail",
    component: () => import("@/components/ProblemSetDetail.vue"),
    props: true,
    meta: {
      appTitle: "题库详情",
      pageTitle: "题库详情",
    },
  },
  {
    path: "/exercise/:id",
    name: "ProblemDetail",
    component: () => import("@/components/ProblemDetail.vue"),
    props: true,
    meta: {
      appTitle: "题目详情",
      pageTitle: "题目详情",
    },
  },
  // 可以在这里添加更多自定义路由
];

// 为自动生成的路由添加 meta 字段
const routesWithMeta = autoRoutes.map((route) => {
  let appTitle = "加载中"; // 默认应用栏标题
  let pageTitle = "加载中"; // 默认浏览器标签页标题

  // 根据路由路径或名称设置具体标题
  switch (route.path) {
    case "/home":
      appTitle = "公告栏";
      pageTitle = "首页";
      break;
    case "/problemset":
      appTitle = "题库";
      pageTitle = "题库";
      break;
    case "/discussions":
      appTitle = "讨论区";
      pageTitle = "讨论区";
      break;
    case "/login":
      appTitle = "登录";
      pageTitle = "登录";
      break;
    case "/profile":
      appTitle = "个人中心";
      pageTitle = "个人中心";
      break;
    // 可以根据需要添加更多路由的标题配置
    default:
      appTitle = route.name || "即将就绪";
      pageTitle = route.name || "即将就绪";
  }

  return {
    ...route,
    meta: {
      appTitle,
      pageTitle,
    },
  };
});

// 添加重定向路由，从 '/' 重定向到 '/home'
const routes = [
  { path: "/", redirect: "/home" },
  // 先添加自定义路由，以确保匹配优先级
  ...customRoutes,
  // 然后添加自动生成的路由
  ...routesWithMeta,
  // 添加通配符路由，匹配所有未定义的路径
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: {
      appTitle: '出错了！',
      pageTitle: '出错了！',
    },
  },
];

// 创建路由实例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.("Failed to fetch dynamically imported module")) {
    if (!localStorage.getItem("vuetify:dynamic-reload")) {
      console.log("Reloading page to fix dynamic import error");
      localStorage.setItem("vuetify:dynamic-reload", "true");
      location.assign(to.fullPath);
    } else {
      console.error("Dynamic import error, reloading page did not fix it", err);
    }
  } else {
    console.error(err);
  }
});

router.isReady().then(() => {
  localStorage.removeItem("vuetify:dynamic-reload");
});

export default router;

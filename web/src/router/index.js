// router/index.js
import { createRouter, createWebHistory } from "vue-router";
import { routes as autoRoutes } from "vue-router/auto-routes";
import NotFound from "@/components/NotFound.vue"; // 导入 404 页面组件
import store from "@/store";
import Unauthorized from "@/components/Unauthorized.vue";

const adminRoutes = [
  {
    path: "/admin/home",
    component: () => import("@/components/admin/AdminBoard.vue"),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    }
  },
  {
    path: "/admin/new-notification",
    component: () => import("@/components/admin/NewAnnouncement.vue"),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    }
  },
  {
    path: "/admin/exercise/:id",
    component: () => import("@/components/admin/EditExercise.vue"),
    props: true,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    }
  },
  {
    path: "/admin/exercise/new",
    component: () => import("@/components/admin/NewExercise.vue"),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    }
  },
  {
    path: "/admin/exercise",
    component: () => import("@/components/admin/AdminExercise.vue"),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    }
  },
  {
    path: "/admin/problemset/new",
    component: () => import("@/components/admin/NewSet.vue"),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    }
  },
  {
    path: "/admin/problemset",
    component: () => import("@/components/admin/AdminSet.vue"),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    }
  }
]

// 手动添加的自定义路由
const customRoutes = [
  {
    path: "/logout",
    name: "登出",
    beforeEnter: (to, from, next) => {
      store.commit("cleanUserId");
      next("/login");
    },
    meta: { requiresAuth: true },
  },
  {
    path: "/problemset/:id",
    name: "ProblemSetDetail",
    component: () => import("@/components/user/ProblemSetDetail.vue"),
    props: true,
    meta: {
      appTitle: "题库详情",
      pageTitle: "题库详情",
      requiresAuth: true,
    },
  },
  {
    path: "/exercise/:id",
    name: "ProblemDetail",
    component: () => import("@/components/user/ProblemDetail.vue"),
    props: true,
    meta: {
      appTitle: "题目详情",
      pageTitle: "题目详情",
      requiresAuth: true,
    },
  },
  {
    path: "/exam/:id",
    name: "ExamDetail",
    component: () => import("@/components/user/ExamDetail.vue"),
    props: true,
    meta: {
      appTitle: "测试详情",
      pageTitle: "测试详情",
      requiresAuth: true,
    },
  },
  {
    path: "/discussion/new",
    name: "NewPost",
    component: () => import("@/components/user/NewPost.vue"),
    props: true,
    meta: {
      appTitle: "发布新讨论",
      pageTitle: "发布新讨论",
      requiresAuth: true,
    },
  },
  {
    path: "/admin/profile",
    name: "Profile",
    component: () => import("@/components/ProfileContent.vue"),
    props: true,
    meta: {
      appTitle: "个人中心",
      pageTitle: "个人中心",
      requiresAuth: true,
    },
  },
  {
    path: "/discussion/:id",
    name: "DiscussionContent",
    component: () => import("@/components/user/DiscussionContent.vue"),
    props: true,
    meta: {
      appTitle: "讨论详情",
      pageTitle: "讨论详情",
      requiresAuth: true,
    },
  },
  {
    path: "/unauthorized",
    name: "Unauthorized",
    component: Unauthorized,
    meta: {
      appTitle: "未授权",
      pageTitle: "未授权",
    },
  },
];

// 为自动生成的路由添加 meta 字段
const routesWithMeta = autoRoutes.map((route) => {
  let appTitle = "加载中"; // 默认应用栏标题
  let pageTitle = "加载中"; // 默认浏览器标签页标题
  let requiresAuth = true;

  // 根据路由路径或名称设置具体标题
  switch (route.path) {
    case "/home":
    case "/admin/home":
      appTitle = "公告栏";
      pageTitle = "首页";
      break;
    case "/problemset":
      appTitle = "题库";
      pageTitle = "题库";
      break;
    case "/exam":
      appTitle = "模拟测试";
      pageTitle = "模拟测试";
      break;
    case "/forum":
      appTitle = "讨论区";
      pageTitle = "讨论区";
      break;
    case "/login":
      appTitle = "登录";
      pageTitle = "登录";
      break;
    case "/profile":
    case "/admin/profile":
      appTitle = "个人中心";
      pageTitle = "个人中心";
      break;
    // 可以根据需要添加更多路由的标题配置
    default:
      appTitle = route.name || "即将就绪";
      pageTitle = route.name || "即将就绪";
  }

  // 如果路由是登录页，设置 requiresGuest 为 true
  if (route.path === "/login") {
    return {
      ...route,
      meta: {
        appTitle,
        pageTitle,
        requiresGuest: true, // 仅限未认证用户
      },
    };
  }

  // 其他路由默认需要认证
  return {
    ...route,
    meta: {
      appTitle,
      pageTitle,
      requiresAuth, // 根据前面的逻辑设置
    },
  };
});

// 添加重定向路由，从 '/' 重定向到 '/home'
const routes = [
  { path: "/", redirect: "/home" },
  { path: "/admin/", redirect: "/admin/home"},
  // 先添加自定义路由，以确保匹配优先级
  ...customRoutes,
  ...adminRoutes,
  // 然后添加自动生成的路由
  ...routesWithMeta,
  // 添加通配符路由，匹配所有未定义的路径
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: NotFound,
    meta: {
      appTitle: "出错了！",
      pageTitle: "出错了！",
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

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated;
  const userRole = store.getters.userRole ? store.getters.userRole : -1; // 获取用户角色

  if (to.meta.requiresAuth && !isAuthenticated) {
    // 如果目标路由需要认证但用户未认证，重定向到登录页
    next({ path: '/login', query: { redirect: to.fullPath } });
  } else if (to.meta.requiresGuest && isAuthenticated) {
    // 如果目标路由仅限未认证用户且用户已认证，重定向到首页
    next({ path: '/home' });
  } else if (to.meta.requiresAdmin && userRole <= 0) {
    // 如果目标路由需要管理员权限但用户角色不足，重定向到未授权页面
    next({ path: '/unauthorized' });
  } else {
    // 否则，允许导航
    next();
  }
});

router.isReady().then(() => {
  localStorage.removeItem("vuetify:dynamic-reload");
});

export default router;

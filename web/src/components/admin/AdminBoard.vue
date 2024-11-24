<template>
    <v-banner sticky icon="mdi-plus" lines="one">
        <template v-slot:text>
            <div class="text-subtitle-1">作为辅导师，你可发布新的公告。</div>
        </template>

        <template v-slot:actions>
            <v-btn color="primary" class="mr-5" @click="postNewNoti()">
                <div class="text-subtitle-1">发布新公告</div>
            </v-btn>
        </template>
    </v-banner>
    <v-container class="scroll-container">
        <v-row>
            <v-col v-for="notice in notices" :key="notice.id" cols="12">
                <v-card>
                    <v-card-title>
                        <div>
                            <div class="notice-title">{{ notice.title }}</div>
                            <div class="notice-subtitle">{{ notice.publisher }}&nbsp;&nbsp;{{
                                formatDate(notice.releaseTime) }}
                            </div>
                        </div>
                    </v-card-title>
                    <v-divider></v-divider>
                    <div style="margin-left: -15px;">
                        <v-md-preview :text="notice.content"></v-md-preview>
                    </div>
                    <v-divider></v-divider>
                    <v-row no-gutters>
                        <v-col cols="auto">
                            <v-btn rounded="0" variant="text" :color="'#1867c0'" @click="editNotice(notice)">
                                <v-icon left>mdi-pencil</v-icon>
                                编辑此公告
                            </v-btn>
                        </v-col>
                        <v-col cols="auto">
                            <v-btn rounded="0" variant="text" color="#ee3f4d" @click="confirmDelete(notice)">
                                <v-icon left>mdi-close</v-icon>
                                删除此公告
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
    <v-dialog v-model="editDialogOpen" transition="dialog-bottom-transition" fullscreen>
        <v-card>
            <v-toolbar dark color="primary">
                <v-btn icon dark @click="editDialogOpen = false">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
                <v-toolbar-title>编辑公告</v-toolbar-title>
            </v-toolbar>
            <div class="scroll-container">
                <v-form ref="form" v-model="valid" lazy-validation>
                    <v-row>
                        <v-col>
                            <v-text-field v-model="currentNotice.title" label="标题" :rules="[rules.required]"
                                variant="outlined" />
                        </v-col>
                    </v-row>
                </v-form>

                <!-- 表单和编辑器之间的分割线 -->
                <v-divider></v-divider>

                <!-- Markdown 编辑器 -->
                <v-md-editor v-model="currentNotice.content" height="325px"
                    left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | link image code"
                    right-toolbar="preview toc sync-scroll"></v-md-editor>

                <!-- 按钮行 -->
                <v-row class="btns">
                    <v-btn color="primary" @click="confirmNotice">发布</v-btn>
                    <v-btn variant="plain" @click="clearNotice">清除</v-btn>
                </v-row>
            </div>
        </v-card>
    </v-dialog>
    <v-dialog v-model="submitDialogOpen" max-width="400px">
        <v-card>
            <v-card-title>
                <v-icon color="primary">mdi-alert-circle-outline</v-icon>
                <span class="headline ml-2">确定提交你的更改吗？</span>
            </v-card-title>
            <v-card-actions>
                <v-btn color="primary" variant="text" @click="submitNotice">
                    确定
                </v-btn>
                <v-btn variant="plain" @click="submitDialogOpen = false">
                    取消
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
    <v-dialog v-model="deleteDialogOpen" max-width="400px">
        <v-card>
            <v-card-title>
                <v-icon color="primary">mdi-alert-circle-outline</v-icon>
                <span class="headline ml-2">确定删除该公告吗？</span>
            </v-card-title>
            <v-card-actions>
                <v-btn color="primary" variant="text" @click="deleteNotice">
                    确定
                </v-btn>
                <v-btn variant="plain" @click="deleteDialogOpen = false">
                    取消
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
    <v-snackbar v-model="snackbarOpen" :timeout="snackbarTimeout" :color="snackbarColor" min-width="25%"
        style="z-index: 10000;">
        <div style="font-size: 16px">{{ snackbarMessage }}</div>
        <template #actions>
            <v-btn icon @click="snackbarOpen = false">
                <v-icon>mdi-close</v-icon>
            </v-btn>
        </template>
    </v-snackbar>
</template>

<script>
import { mapMutations } from 'vuex';

export default {
    name: 'AdminBoard',
    data() {
        return {
            notices: [
                {
                    id: 1,
                    title: "关于2024年春季学期开学的通知",
                    publisher: "教务处",
                    releaseTime: "2023-10-15T19:00:09",
                    content:
                        "# 草四你 \n  各位同学，2024年春季学期将于2月20日正式开学，请提前做好返校准备。",
                },
                {
                    id: 2,
                    title: "国庆节放假安排",
                    publisher: "校办",
                    releaseTime: "2023-09-28T19:00:09",
                    content: "根据国家规定，国庆节放假时间为10月1日至10月7日，共7天。",
                },
                {
                    id: 3,
                    title: "校园网络维护通知",
                    publisher: "网络中心",
                    releaseTime: "2023-10-10T19:00:09",
                    content: "因设备升级，10月12日0:00-6:00校园网络将暂停服务。",
                },
            ],
            rules: {
                required: (value) => !!value || "该字段为必填项",
            },
            valid: false,
            editDialogOpen: false,
            currentNotice: {
                id: null,
                title: '',
                publisher: '',
                releaseTime: '',
                content: '',
            },
            originalNotice: {},
            toDeleteNotice: null,
            submitDialogOpen: false,
            deleteDialogOpen: false,
            snackbarOpen: false,
            snackbarMessage: '',
            snackbarTimeout: 1000,
            snackbarColor: 'error', // 错误颜色
        };
    },
    mounted() {
        // 更新标题
        const title = '主页';
        this.setAppTitle(title);
        this.setPageTitle(title);

        // 按发布时间对 notices 进行排序，越新的排在最前面
        this.notices.sort((a, b) => new Date(b.releaseTime) - new Date(a.releaseTime));
    },
    methods: {
        ...mapMutations(['setAppTitle', 'setPageTitle']),

        // 格式化日期
        formatDate(dateString) {
            const options = {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false, // 使用24小时制
            };
            const date = new Date(dateString);
            return date.toLocaleString("zh-CN", options).replace(/\//g, "-");
        },
        editNotice(notice) {
            this.currentNotice = { ...notice };
            this.originalNotice = { ...notice };
            this.editDialogOpen = true;
        },
        postNewNoti() {
            this.$router.push("/admin/new-notification");
        },
        hasChanges() {
            return (
                this.currentNotice.title !== this.originalNotice.title ||
                this.currentNotice.content !== this.originalNotice.content
            );
        },
        confirmDelete(notice) {
            this.toDeleteNotice = notice;
            this.deleteDialogOpen = true;
        },
        deleteNotice() {
            this.deleteDialogOpen = false;
            this.snackbarMessage = `已删除公告${this.toDeleteNotice.id} "${this.toDeleteNotice.title}" `;
            this.snackbarColor = 'success';
            this.snackbarOpen = true;
            this.toDeleteNotice = null;
        },
        confirmNotice() {
            if (!this.currentNotice.title || !this.currentNotice.content) {
                this.snackbarMessage = '标题或内容不能为空';
                this.snackbarColor = 'error';
                this.snackbarOpen = true;
                return;
            }
            if (this.hasChanges()) {
                this.submitDialogOpen = true;
            } else {
                this.snackbarMessage = '修改成功';
                this.snackbarColor = 'success';
                this.snackbarOpen = true;
                this.editDialogOpen = false;
                this.submitDialogOpen = false;
            }
        },
        submitNotice() {
            // 执行提交逻辑
            console.log(this.currentNotice);
            this.snackbarMessage = '修改成功';
            this.snackbarColor = 'success';
            this.snackbarOpen = true;
            this.editDialogOpen = false;
            this.submitDialogOpen = false;
        },

        // 清除公告内容
        clearNotice() {
            this.currentNotice.title = '';
            this.currentNotice.content = '';
        }
    },
};
</script>

<style scoped>
.scroll-container {
    flex-direction: column;
    flex: 1 1 auto;
    overflow-y: auto;
    padding: 16px;
    padding-bottom: 80px;
    height: 90vh;
    max-height: 90vh;
    -ms-overflow-style: none;
    scrollbar-width: none;
}

.scroll-container::-webkit-scrollbar {
    display: none;
}

/* 公告列表样式 */
.notice-title {
    font-size: 1.35rem;
    /* 增大字体 */
    margin-bottom: 4px;
}

.notice-subtitle {
    font-size: 1.0rem;
    /* 增大字体 */
    color: rgba(0, 0, 0, 0.6);
}

.notice-publisher {
    font-size: 1.1rem;
    /* 增大字体 */
}

.notice-time {
    font-size: 1rem;
    /* 保持时间字体大小不变 */
    color: rgba(0, 0, 0, 0.6);
}

.notice-item {
    padding: 4px 0;
}

.notice-item:hover {
    background-color: #f5f5f5;
    cursor: pointer;
}

.btns {
    margin-top: 16px;
    padding-left: 16px;
}
</style>

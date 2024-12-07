<template>
    <div class="scroll-container">
        <!-- 主讨论卡片和评论卡片作为一个整体 -->
        <v-card class="mx-auto main-card" max-width="85%">
            <!-- 主讨论部分 -->
            <v-card-item :prepend-avatar="mainDiscussion.avatar">
                <v-card-item-title class="text-h6 font-weight-regular">
                    <v-row align="center" no-gutters>
                        <v-col cols="auto">
                            {{ mainDiscussion.publisher }}
                        </v-col>
                    </v-row>
                </v-card-item-title>
                <v-card-item-subtitle>
                    <v-row align="center" no-gutters>
                        <v-col cols="auto" class="text-body-1 text-disabled">
                            {{ formatDate(mainDiscussion.publishTime) }}
                        </v-col>
                    </v-row>
                </v-card-item-subtitle>
                <template v-slot:append>
                    <v-icon v-if="mainDiscussion.isLiked" color="#ee3f4d">mdi-thumb-up</v-icon>
                    <v-icon v-if="isSubscribed" color="#fbc02d">mdi-bell</v-icon>
                    <v-icon v-if="isMarked" color="#fbc02d">mdi-star</v-icon>
                </template>
            </v-card-item>
            <v-card-text>
                <v-divider style="padding-top: 10px; padding-bottom: 0px"></v-divider>
                <!-- 显示主讨论内容 -->
                <div style="margin-left: -29px">
                    <v-md-preview :text="mainDiscussion.content"></v-md-preview>
                </div>
            </v-card-text>

            <!-- 订阅和点赞按钮区域 -->
            <v-divider></v-divider>
            <v-row no-gutters>
                <v-col cols="auto">
                    <v-btn rounded="0" @click="toggleLike('main')" class="like-btn"
                        :variant="mainDiscussion.isLiked ? 'tonal' : 'text'" color="#ee3f4d">
                        <v-icon>{{ mainDiscussion.isLiked ? "mdi-thumb-up" : "mdi-thumb-up-outline" }}</v-icon>
                        {{ mainDiscussion.isLiked ? "取消点赞" : "点赞" }}
                    </v-btn>
                </v-col>
                <v-col cols="auto">
                    <v-btn rounded="0" @click="toggleSubscription" class="subscribe-btn"
                        :variant="isSubscribed ? 'tonal' : 'text'" :color="'#fbc02d'">
                        <v-icon>{{ isSubscribed ? "mdi-bell-off" : "mdi-bell-outline" }}</v-icon>
                        {{ isSubscribed ? "取消订阅" : "订阅" }}
                    </v-btn>
                </v-col>
                <v-col cols="auto">
                    <v-btn rounded="0" @click="toggleMark" class="subscribe-btn" :variant="isMarked ? 'tonal' : 'text'"
                        :color="'#fbc02d'">
                        <v-icon>{{ isMarked ? "mdi-star-minus-outline" : "mdi-star-plus-outline" }}</v-icon>
                        {{ isMarked ? "取消加精" : "加精" }}
                    </v-btn>
                </v-col>
                <v-col cols="auto">
                    <v-btn rounded="0" variant="text" :color="'#574266'" @click="commentDiscussion(mainDiscussion.id)">
                        <v-icon left>mdi-comment-outline</v-icon>
                        评论
                    </v-btn>
                </v-col>
                <v-col v-if="mainDiscussion.publisherId == currentUserId" cols="auto">
                    <v-btn rounded="0" variant="text" :color="'#1867c0'"
                        @click="editDiscussion(mainDiscussion.id, mainDiscussion.content)">
                        <v-icon left>mdi-pencil</v-icon>
                        编辑
                    </v-btn>
                </v-col>
                <v-col cols="auto">
                    <v-btn rounded="0" variant="text" color="red">
                        <v-icon left>mdi-trash-can-outline</v-icon>
                        删除讨论贴
                    </v-btn>
                </v-col>
            </v-row>

        </v-card>

        <div v-for="discussion in followDiscussion" :key="discussion.id">
            <v-card class="mx-auto follow-card" max-width="85%" style="margin-bottom: 20px;">
                <v-card-item :prepend-avatar="discussion.avatar">
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
                    <template v-slot:append>
                        <v-icon v-if="discussion.isLiked" color="#ee3f4d">mdi-thumb-up</v-icon>
                    </template>
                </v-card-item>
                <v-card-text>
                    <v-divider style="padding-top: 10px; padding-bottom: 0px"></v-divider>
                    <!-- 显示跟随讨论内容 -->
                    <div style="margin-left: -29px">
                        <v-md-preview :text="discussion.content"></v-md-preview>
                    </div>
                </v-card-text>
                <v-divider></v-divider>
                <v-row no-gutters>
                    <v-col cols="auto">
                        <v-btn rounded="0" @click="toggleLike(discussion.id)" class="like-btn"
                            :variant="discussion.isLiked ? 'tonal' : 'text'" :color="'#ee3f4d'">
                            <v-icon>{{ discussion.isLiked ? "mdi-thumb-up" : "mdi-thumb-up-outline" }}</v-icon>
                            {{ discussion.isLiked ? "取消点赞" : "点赞" }}
                        </v-btn>
                    </v-col>
                    <v-col cols="auto">
                        <v-btn rounded="0" variant="text" :color="'#574266'" @click="commentDiscussion(discussion.id)">
                            <v-icon left>mdi-comment-outline</v-icon>
                            评论
                        </v-btn>
                    </v-col>
                    <v-col v-if="discussion.publisherId == currentUserId" cols="auto">
                        <v-btn rounded="0" variant="text" :color="'#1867c0'"
                            @click="editDiscussion(discussion.id, discussion.content)">
                            <v-icon left>mdi-pencil</v-icon>
                            编辑
                        </v-btn>
                    </v-col>
                    <v-col cols="auto">
                        <v-btn rounded="0" variant="text" color="red">
                            <v-icon left>mdi-trash-can-outline</v-icon>
                            删除回复
                        </v-btn>
                    </v-col>
                </v-row>
            </v-card>
        </div>
    </div>

    <v-btn class="floating-btn" fab color="primary" @click="returnForum()">
        <v-icon size="32">mdi-arrow-collapse-left</v-icon>
    </v-btn>

    <v-dialog v-model="editDialog" height="45%" width="60%">
        <v-card title="编辑">
            <v-md-editor v-model="text" height="325px" width="20%"
                left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | link image code"
                right-toolbar="preview toc sync-scroll"></v-md-editor>
            <v-spacer></v-spacer>
            <v-card-action>
                <v-btn color="primary" variant="text" @click="emitEdit">提交</v-btn>
            </v-card-action>
        </v-card>
    </v-dialog>

    <v-dialog v-model="commentDialog" height="45%" width="60%">
        <v-card title="评论">
            <v-md-editor v-model="text" height="325px" width="20%"
                left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | link image code"
                right-toolbar="preview toc sync-scroll"></v-md-editor>
            <v-spacer></v-spacer>
            <v-card-action>
                <v-btn color="primary" variant="text" @click="emitEdit">提交</v-btn>
            </v-card-action>
        </v-card>
    </v-dialog>
</template>

<script>
import axios from 'axios';
import { mapMutations } from "vuex";
import { mapState } from "vuex/dist/vuex.cjs.js";
import store from "@/store";

export default {
    name: "ForumContent",
    props: {
        id: {
            type: String,
            required: true,
        }
    },
    data() {
        return {
            currentUserId: null,
            editDialog: false,
            commentDialog: false,
            emitId: null,
            text: '',
            mainDiscussion: {
                id: 2,
                title: "离散数学在计算机科学中的应用",
                publisher: "李四",
                publisherId: 22373498,
                avatar: "https://randomuser.me/api/portraits/women/40.jpg",
                publishTime: "2024-09-25T15:30:00",
                lastUpdated: "2024-11-15T15:30:00",
                tag: "离散数学（信息类）",
                content: `
    # Markdown 测试文档
    ...
    `,
                isLiked: false,
            },
            isSubscribed: false,
            isMarked: false,
            followDiscussion: [
                {
                    id: 3,
                    publisher: "李四2",
                    publisherId: 22373300,
                    avatar: "https://randomuser.me/api/portraits/women/10.jpg",
                    publishTime: "2024-09-25T15:30:00",
                    lastUpdated: "2024-11-15T15:30:00",
                    content: "内容1",
                    isLiked: false,
                },
                {
                    id: 30,
                    publisher: "李四3",
                    publisherId: 22373498,
                    avatar: "https://randomuser.me/api/portraits/women/98.jpg",
                    publishTime: "2024-09-25T15:30:00",
                    lastUpdated: "2024-11-15T15:30:00",
                    content: "内容2",
                    isLiked: false,
                },
            ],
        };
    },
    mounted() {
        const title = `讨论 - ${this.mainDiscussion.title}`;
        this.setAppTitle(title);
        this.setPageTitle(title);
        this.currentUserId = store.getters.getUserId;
        this.sendDataToBackend();
    },
    methods: {
        ...mapMutations(["setAppTitle", "setPageTitle"]),
        ...mapState(["userId"]),
        async sendDataToBackend() {
            try {
                // 获取 user_id 和 dis_id
                const userId = this.$store.getters.getUserId; // 假设你使用 Vuex 获取 user_id
                const disId = this.$route.params.id;         // 从路由获取 dis_id

                // 打包请求数据
                const requestData = {
                    user_id: userId,
                    dis_id: disId
                };

                // 发送 POST 请求到后端 API，并指定请求头为 application/json
                const response = await axios.post('http://127.0.0.1:8000/api/discussions/get_discussion/', requestData, {
                    headers: {
                        'Content-Type': 'application/json',  // 指定请求体的格式为 JSON
                    }
                });
                if (response.data.success) {
                    this.mainDiscussion = response.data.discussion;
                    this.followDiscussion = response.data.replies;
                    // 处理后端响应
                    const title = `讨论 - ${this.mainDiscussion.title}`;
                    this.setAppTitle(title);
                    this.setPageTitle(title);
                    console.log('请求成功:', response.data);
                } else {
                    console.log('请求失败');
                }
            } catch (error) {
                // 请求失败时处理错误
                console.error('请求失败:', error);
            }
        },
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
        returnForum() {
            this.$router.push(`/admin/forum`);
        },
        async toggleSubscription() {
            this.isSubscribed = !this.isSubscribed;
            try {
                const userId = this.$store.getters.getUserId; // 假设你使用 Vuex 获取 user_id
                const disId = this.$route.params.id; // 使用传入的 discussionId 作为 dis_id

                const requestData = {
                    user_id: userId,
                    dis_id: disId
                };
                let url = 'http://127.0.0.1:8000/api/discussions/subscribe_discussion/';
                // 发送 POST 请求到后端 API，并指定请求头为 application/json
                const response = await axios.post(url, requestData, {
                    headers: {
                        'Content-Type': 'application/json',  // 指定请求体的格式为 JSON
                    }
                });
                console.log('请求成功:', response.data);

            } catch (error) {
                console.error('请求失败:', error);
            }
        },
        toggleMark() {
            this.isMarked = !this.isMarked;
        },
        async toggleLike(discussionId) {
            // 更新讨论的 isLiked 状态
            if (discussionId === "main") {
                this.mainDiscussion.isLiked = !this.mainDiscussion.isLiked;
            } else {
                // 检查是否是跟随讨论的ID
                const discussion = this.followDiscussion.find(
                    (d) => d.id === discussionId
                );
                if (discussion) {
                    discussion.isLiked = !discussion.isLiked;
                } else {
                    // 如果ID未找到，抛出警告
                    console.warn(`未找到对应的讨论或评论，ID: ${discussionId}`);
                    return;  // 退出方法，防止继续执行后面的请求
                }
            }

            try {
                // 获取 user_id 和 dis_id
                const userId = this.$store.getters.getUserId; // 假设你使用 Vuex 获取 user_id
                const disId = this.$route.params.id; // 使用传入的 discussionId 作为 dis_id

                // 打包请求数据
                const requestData = {
                    user_id: userId,
                    dis_id: discussionId == "main" ? disId : discussionId
                };
                let url = '';
                // 根据discussionId决定URL
                if (discussionId === "main") {
                    url = 'http://127.0.0.1:8000/api/discussions/like_discussion/';
                } else {
                    url = 'http://127.0.0.1:8000/api/discussions/like_reply/';
                }
                // 发送 POST 请求到后端 API，并指定请求头为 application/json
                const response = await axios.post(url, requestData, {
                    headers: {
                        'Content-Type': 'application/json',  // 指定请求体的格式为 JSON
                    }
                });

                // 处理后端响应
                console.log('请求成功:', response.data);

            } catch (error) {
                // 请求失败时处理错误
                console.error('请求失败:', error);
            }
        },
        editDiscussion(id, content) {
            this.editDialog = true;
            this.text = content;
            this.emitId = id;
        },
        commentDiscussion(id) {
            this.commentDialog = true;
            this.text = '';
            this.emitId = id;
        },
        emitEdit() {
            console.log(this.emitId);
            console.log(this.text);
            this.commentDialog = false;
            this.editDialog = false;
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

.main-card {
    margin-bottom: 30px;
}

.follow-card {
    margin-bottom: 30px;
}

.subscribe-btn,
.like-btn {
    width: auto;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    margin-top: 0px;
}
</style>
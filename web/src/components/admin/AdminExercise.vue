<template>
<!-- 顶部横幅 -->
<v-banner sticky icon="mdi-plus" lines="one">
    <template v-slot:text>
        <div class="text-subtitle-1">作为辅导师，你可创建新的题目，或查看/编辑/删除已有的题目。</div>
    </template>

    <template v-slot:actions>
        <v-btn color="primary" class="mr-5" @click="createExercise()">
            <div class="text-subtitle-1">创建新题目</div>
        </v-btn>
    </template>
</v-banner>
<v-container v-if="loading">
    <v-skeleton-loader class="mx-auto main-card" max-width="100%" type="list-item-avatar-three-line, list-item-avatar-three-line, list-item-avatar-three-line"></v-skeleton-loader>
</v-container>
<v-container v-else fluid>
    <!-- 筛选条件区域 -->
    <v-card class="pl-2 pr-2 pb- 2" variant="text" title="筛选题目" subtitle="输入题目ID或学科以查找题目，点击题目可进行查看/编辑/删除操作。" prepend-icon="mdi-filter">
        <v-row align="center" justify="start" no-gutters>
            <v-col cols="12" sm="6" md="4" class="pa-2">
                <v-text-field v-model="filterId" label="题目 ID" placeholder="输入题目 ID" clearable></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4" class="pa-2">
                <v-select v-model="filterSubject" :items="subjectOptions" label="学科" placeholder="选择学科" clearable></v-select>
            </v-col>
        </v-row>
    </v-card>

    <!-- 题目列表区域 -->
    <div class="exercises-container">
        <template v-if="filteredExercises && filteredExercises.length > 0">
            <v-expansion-panels>
                <v-expansion-panel v-for="(group, index) in filteredExercises" :key="group.subject">
                    <v-expansion-panel-title>
                        <template v-slot:default="{ expanded }">
                            <v-row no-gutters class="align-center w-100">
                                <v-col class="d-flex justify-start text-bold" cols="2">
                                    {{ group.subject }}
                                </v-col>
                                <v-col class="text-grey" cols="9">
                                    <v-fade-transition leave-absolute>
                                        <span> 共 {{ group.ids.length }} 题 </span>
                                    </v-fade-transition>
                                </v-col>
                            </v-row>
                        </template>
                    </v-expansion-panel-title>

                    <v-expansion-panel-text>
                        <v-row no-gutters>
                            <div class="question-squares">
                                <v-btn v-for="id in getPaginatedIds(group)" :key="id" class="question-square text-none" color="blue-darken-4" rounded="0" @click="editExercise(id)">
                                    <v-responsive class="text-truncate">{{ id }}</v-responsive>
                                </v-btn>
                            </div>
                        </v-row>
                        <v-row justify="center" class="mt-2">
                            <v-pagination v-model="group.currentPage" :total-visible="7" :length="Math.ceil(group.ids.length / pageSize)" @input="handlePageChange(group, $event)"></v-pagination>
                        </v-row>
                    </v-expansion-panel-text>
                </v-expansion-panel>
            </v-expansion-panels>
        </template>

        <!-- 没有符合条件的题目 -->
        <div v-else class="no-results">
            <p>没有符合条件的题目。</p>
        </div>
    </div>
</v-container>
</template>

<script>
import {
    mapMutations
} from 'vuex';
import axios from 'axios';
export default {
    name: 'AdminExercise',
    data() {
        return {
            exercises: [],
            filterId: '',
            filterSubject: '',
            pageSize: 40, // 每页显示的题目数量
            loading: true,
        };
    },
    computed: {
        // 获取所有唯一的学科选项
        subjectOptions() {
            return this.exercises.map(ex => ex.subject).sort();
        },
        // 根据筛选条件过滤后的题目
        filteredExercises() {
            let filtered = this.exercises;

            if (this.filterSubject) {
                filtered = filtered.filter(ex => ex.subject === this.filterSubject);
            }

            if (this.filterId) {
                filtered = filtered.map(ex => ({
                    ...ex,
                    ids: ex.ids.filter(id => id.toString() === this.filterId.trim())
                })).filter(ex => ex.ids.length > 0);
            }

            return filtered;
        },
    },
    created() {
        // 更新标题
        this.loading = true;
        const title = '题目管理';
        this.setAppTitle(title);
        this.setPageTitle(title);
        this.getAll();
    },
    methods: {
        ...mapMutations(['setAppTitle', 'setPageTitle']),
        async getAll() {
            console.log("there");
            try {
                // 发送 POST 请求到后端获取数据
                const response = await axios.post('http://127.0.0.1:8000/api/questions/get_all_questions/', {
                    user_id: this.$store.getters.getUserId,
                });

                // 检查后端返回的响应
                if (response.data.success) {
                    const data = response.data;

                    // 将后端返回的题目信息映射到前端的 `questions` 结构
                    const questions = data.qsdata.map((question) => {
                        return {
                            subject: question.subject, // 保留题型
                            ids: question.ids.map((id) => (id)),
                            currentPage: question.currentPage, // 保留当前页信息
                        };
                    });
                    // 更新组件的题目数据
                    this.exercises = questions;
                    this.loading = false;
                } else {
                    throw new Error("获取题目数据失败");
                }
            } catch (e) {
                console.error("获取题目数据失败", e);
                this.error = "获取题目数据失败";
                this.loading = false;
            }
        },
        createExercise() {
            this.$router.push("/admin/exercise/new");
        },
        editExercise(id) {
            this.$router.push(`/admin/exercise/${id}`);
        },
        getPaginatedIds(group) {
            const start = (group.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return group.ids.slice(start, end);
        },
        handlePageChange(group, newPage) {
            group.currentPage = newPage;
        },
    },
};
</script>

<style scoped>
.exercises-container {
    max-height: calc(100vh - 350px);
    overflow-y: auto;
    padding: 16px 16px 32px;
    display: flex;
    flex-direction: column;
    scrollbar-width: none;
}

.question-squares {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 16px;
}

.question-square {
    width: 70px;
    height: 70px;
    font-size: 16px;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    border-radius: 0;
    overflow-wrap: break-word;
    word-wrap: break-word;
    cursor: pointer;
}

.question-square:hover {
    background-color: rgba(0, 0, 0, 0.1);
}

.v-responsive {
    max-width: 100%;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    font-size: 14px;
}

.v-expansion-panel {
    margin-bottom: 8px;
}

.v-expansion-panel-title {
    cursor: pointer;
}

.v-banner {
    margin-bottom: 16px;
}

.v-expansion-panel {
    margin-bottom: 0px;
}

/* 没有结果的提示 */
.no-results {
    padding: 32px;
    text-align: center;
    color: #757575;
}

/* 可选：调整按钮颜色和样式 */
.v-btn.blue-darken-4 {
    background-color: #1e3a8a;
    /* 深蓝色 */
    color: white;
}

.v-btn.blue-darken-4:hover {
    background-color: #1e40af;
}

.btns {
    margin-top: 16px;
    padding-left: 16px;
}

.info-card {
    max-height: 60%;
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
</style>

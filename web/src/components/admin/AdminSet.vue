<template>
    <v-banner sticky icon="mdi-plus" lines="one">
        <template v-slot:text>
            <div class="text-subtitle-1">
                作为辅导师，你可创建新的题库，或查看/编辑/删除已有的题库。
            </div>
        </template>

        <template v-slot:actions>
            <v-btn color="primary" class="mr-5" @click="enterNewSet">
                <div class="text-subtitle-1">创建题库</div>
            </v-btn>
        </template>
    </v-banner>
    <v-container v-if="loading">
        <v-skeleton-loader class="mx-auto main-card" max-width="100%"
            type="list-item-avatar-three-line, list-item-avatar-three-line, list-item-avatar-three-line"></v-skeleton-loader>
    </v-container>
    <v-container v-else fluid class="problemset-container">
        <!-- Filter Section -->
        <div class="filter-container">
            <v-card variant="text" class="pb-2 pl-2 pr-2" title="筛选题库" subtitle="通过名称搜索、选择科目或选择时间范围进行筛选"
                prepend-icon="mdi-filter">
                <v-row no-gutters>
                    <v-col cols="12" sm="3">
                        <v-row align="center" justify="start">
                            <v-col cols="12" sm="12" md="12" class="pa-2">
                                <v-text-field v-model="filterName" label="题库名称" placeholder="输入题库名称" clearable
                                    class="pa-0" full-width></v-text-field>
                            </v-col>
                        </v-row>
                    </v-col>
                    <v-col cols="12" sm="9">
                        <v-row class="pl-12">
                            <!-- Subject Filter -->
                            <v-col cols="12" class="filter-section pa-0">
                                <div class="filter-group">
                                    <span class="filter-label">按科目筛选:</span>
                                    <v-chip v-for="subject in subjects" :key="subject" class="ma-2" color="primary"
                                        variant="outlined" :class="{ 'selected-chip': selectedSubject === subject }"
                                        @click="toggleSubject(subject)">
                                        {{ subject }}
                                        <v-icon v-if="selectedSubject === subject" class="ml-2" small>
                                            mdi-check
                                        </v-icon>
                                    </v-chip>
                                </div>
                            </v-col>

                            <!-- Time Filter -->
                            <v-col cols="12" class="filter-section pa-0">
                                <div class="filter-group">
                                    <span class="filter-label">按时间筛选:</span>
                                    <v-chip v-for="range in timeRanges" :key="range.value" class="ma-2" color="primary"
                                        variant="outlined" :class="{
                                            'selected-chip': selectedTimeRange === range.value,
                                        }" @click="toggleTimeRange(range.value)">
                                        {{ range.text }}
                                        <v-icon v-if="selectedTimeRange === range.value" class="ml-2" small>
                                            mdi-check
                                        </v-icon>
                                    </v-chip>
                                </div>
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>
            </v-card>
        </div>

        <!-- Total Count -->
        <div class="total-count pl-2">
            共 {{ filteredProblemSets.length }} 个满足条件的题库
        </div>

        <!-- Scroll Container -->
        <div class="scroll-container">
            <template v-if="filteredProblemSets.length > 0">
                <!-- Problem Set Cards -->
                <v-row dense class="justify-start">
                    <v-col v-for="problemSet in filteredProblemSets" :key="problemSet.id" cols="12" sm="6" md="3"
                        class="pa-1">
                        <v-card class="w-100" hover>
                            <v-card-text>
                                <p class="text-h5 font-weight-bold">{{ problemSet.name }}</p>

                                <div class="mt-2">
                                    <div class="info-row">
                                        <span>创建日期：</span>
                                        <span>{{ formatDate(problemSet.createdAt) }}</span>
                                    </div>
                                    <div class="info-row">
                                        <span>创建者：</span>
                                        <span>{{ problemSet.createdBy }}</span>
                                    </div>
                                    <div class="info-row">
                                        <span>所属科目：</span>
                                        <span>{{ problemSet.subject }}</span>
                                    </div>
                                    <div class="info-row">
                                        <span>预计用时：</span>
                                        <span>{{ problemSet.estimatedTime }} 分钟</span>
                                    </div>
                                </div>
                            </v-card-text>

                            <v-card-actions>
                                <v-btn color="primary" @click="enterEditSet(problemSet.id)">
                                    查看/编辑题库
                                </v-btn>
                                <v-btn color="red" @click="confirmDelete(problemSet.id, problemSet.name)">
                                    删除题库
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-col>
                </v-row>
            </template>

            <!-- No Results Message -->
            <div v-else class="no-results">没有满足条件的题库</div>
        </div>
    </v-container>
    <v-dialog v-model="confirmDialogOpen" max-width="400px">
        <v-card>
            <v-card-title>
                <v-icon color="primary">mdi-alert-circle-outline</v-icon>
                <span class="headline ml-2">操作不可逆</span>
            </v-card-title>
            <v-card-text>确定删除题库 {{ this.toDeleteName }} 吗？</v-card-text>
            <v-card-actions>
                <v-btn color="red" variant="text" @click="deleteSet"> 确定 </v-btn>
                <v-btn variant="plain" @click="confirmDialogOpen = false"> 取消 </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import {
    mapMutations
} from "vuex";
import axios from "axios";
export default {
    name: "ProblemSet",
    data() {
        return {
            problemSets: [],
            subjects: [
                "工科数学分析（上）",
                "工科数学分析（下）",
                "工科高等代数",
                "离散数学（信息类）",
                "基础物理学A",
            ],
            timeRanges: [{
                text: "最近7天",
                value: "7d",
            },
            {
                text: "最近1个月",
                value: "1m",
            },
            {
                text: "最近半年",
                value: "6m",
            },
            {
                text: "最近一年",
                value: "1y",
            },
            ],
            selectedSubject: null,
            selectedTimeRange: null,
            selectedProblemSet: {},
            confirmDialogOpen: false,
            toDeleteId: null,
            toDeleteName: "",
            filterName: "",
            loading: true,
        };
    },
    created() {
        this.loading = true;
        const title = "题库管理";
        this.setAppTitle(title);
        this.setPageTitle(title);
        this.getAll();
    },
    computed: {
        filteredProblemSets() {
            let filtered = this.problemSets;

            // 按科目筛选
            if (this.selectedSubject) {
                filtered = filtered.filter((ps) => ps.subject === this.selectedSubject);
            }

            // 按时间筛选
            if (this.selectedTimeRange) {
                const now = new Date();
                let fromDate;

                switch (this.selectedTimeRange) {
                    case "7d":
                        fromDate = new Date();
                        fromDate.setDate(now.getDate() - 7);
                        break;
                    case "1m":
                        fromDate = new Date();
                        fromDate.setMonth(now.getMonth() - 1);
                        break;
                    case "6m":
                        fromDate = new Date();
                        fromDate.setMonth(now.getMonth() - 6);
                        break;
                    case "1y":
                        fromDate = new Date();
                        fromDate.setFullYear(now.getFullYear() - 1);
                        break;
                    default:
                        fromDate = null;
                }

                if (fromDate) {
                    filtered = filtered.filter(
                        (ps) => new Date(ps.createdAt) >= fromDate
                    );
                }
            }

            // 按名称筛选
            const filterName = (this.filterName || "").toLowerCase().trim();
            filtered = filtered.filter((ps) => {
                const psName = ps.name || "";
                const matchesName = psName.toLowerCase().includes(filterName);
                return matchesName;
            });

            return filtered;
        },
    },
    methods: {
        // 映射 Vuex 的 mutation
        ...mapMutations(['setAppTitle', 'setPageTitle']),
        async getAll() {
            try {
                const userId = this.$store.getters.getUserId;

                const requestData = {
                    user_id: userId,
                };

                const response = await axios.post('http://127.0.0.1:8000/api/questions/get_all_question_banks/', requestData, {
                    headers: {
                        'Content-Type': 'application/json',  // 指定请求体的格式为 JSON
                    }
                });
                if (response.data.success) {
                    this.problemSets = response.data.question_banks;
                    console.log('请求成功:', response.data);
                    this.loading = false;
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
        toggleSubject(subject) {
            if (this.selectedSubject === subject) {
                this.selectedSubject = null;
            } else {
                this.selectedSubject = subject;
            }
        },
        toggleTimeRange(range) {
            if (this.selectedTimeRange === range) {
                this.selectedTimeRange = null;
            } else {
                this.selectedTimeRange = range;
            }
        },
        enterNewSet() {
            this.$router.push(`/admin/problemset/new`);
        },
        enterEditSet(id) {
            this.$router.push(`/admin/problemset/${id}`);
        },
        confirmDelete(id, name) {
            this.toDeleteId = id;
            this.toDeleteName = name;
            this.confirmDialogOpen = true;
        },
        deleteSet(id) {
            this.confirmDialogOpen = false;
        }
    },
};
</script>

<style scoped>
/* Set box-sizing globally */
* {
    box-sizing: border-box;
}

.problemset-container {
    display: flex;
    flex-direction: column;
    height: 92vh;
    overflow: hidden;
}

.filter-container {
    flex-shrink: 0;
}

/* Reduce vertical height of the filter card */
.filter-card {
    margin-bottom: 4px;
}

.filter-card .v-card-text {
    padding-top: 4px !important;
    padding-bottom: 4px !important;
}

/* Adjust the padding inside the filter sections */
.filter-section {
    margin-bottom: 0.1rem;
}

/* Scroll Container */
.scroll-container {
    flex: 1 1 auto;
    overflow-y: auto;
    padding: 16px;
    padding-bottom: 80px;

    /* 隐藏滚动条 */
    -ms-overflow-style: none;
    scrollbar-width: none;
}

.scroll-container::-webkit-scrollbar {
    display: none;
}

/* Other styles */
.filter-group {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 2px;
}

.filter-label {
    margin-right: 0.5rem;
    font-weight: bold;
}

.v-chip {
    margin: 1px;
    border: 1px solid #1867c0;
    cursor: pointer;
    color: #1867c0;
}

.selected-chip {
    background-color: #1867c0 !important;
    color: white !important;
}

.selected-chip .v-icon {
    color: white !important;
}

.mt-2 {
    margin-top: 0.5rem;
}

.pa-1 {
    padding: 0.25rem !important;
}

.info-row {
    margin-bottom: 0.1rem;
}

.no-results {
    font-size: 1.2rem;
    color: #777;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
}

.total-count {
    font-weight: bold;
}

@media (min-width: 960px) {
    .v-row {
        margin-left: -8px;
        margin-right: -8px;
    }

    .v-col.pa-1 {
        padding-left: 8px !important;
        padding-right: 8px !important;
    }
}
</style>
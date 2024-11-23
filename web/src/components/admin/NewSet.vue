<template>
    <v-banner sticky icon="mdi-plus" lines="one">
        <template v-slot:text>
            <div class="text-subtitle-1">作为辅导师，你可创建新的题库。</div>
        </template>

        <template v-slot:actions>
            <v-btn color="primary" class="mr-5" @click="goBack">
                <div class="text-subtitle-1">返回</div>
            </v-btn>
        </template>
    </v-banner>

    <v-tabs v-model="tempTab" color="primary">
        <v-tab v-for="tabItem in tabs" :key="tabItem.value" :value="tabItem.value"
            :disabled="tabItem.value > maxAllowedTab + 1">
            {{ tabItem.label }}
        </v-tab>
    </v-tabs>

    <div class="pa-2">
        <v-tabs-window v-model="tab" class="scroll-container mt-2">
            <v-tabs-window-item :value="1">
                <!-- 设置基本信息 -->
                <v-form ref="formRef" @submit.prevent>
                    <v-row no-gutters>
                        <v-col cols="12">
                            <v-text-field v-model.number="form.name" label="名称" :rules="[value => !!value || '名称为必填项']"
                                required />
                        </v-col>
                        <!-- 科目输入 -->
                        <v-col cols="12">
                            <v-radio-group v-model="form.subject" label="学科" inline
                                :rules="[value => !!value || '请选择学科']" required>
                                <v-radio label="工科数学分析（上）" value="工科数学分析（上）" />
                                <v-radio label="工科数学分析（下）" value="工科数学分析（下）" />
                                <v-radio label="工科高等代数" value="工科高等代数" />
                                <v-radio label="离散数学（信息类）" value="离散数学（信息类）" />
                                <v-radio label="基础物理学A" value="基础物理学A" />
                            </v-radio-group>
                        </v-col>

                        <!-- 时长输入 -->
                        <v-col cols="12">
                            <v-text-field v-model.number="form.duration" label="时长（分钟）" type="number" :rules="[
                                value => !!value || '时长为必填项',
                                value => Number.isInteger(value) || '时长必须是整数',
                                value => value > 0 || '时长必须大于0'
                            ]" required />
                        </v-col>

                        <!-- 描述输入 -->
                        <v-col cols="12">
                            <v-textarea v-model="form.description" label="描述（不超过60字）" :rules="[
                                value => !!value || '描述为必填项',
                                value => value.length <= 60 || '描述不能超过60字'
                            ]" required rows="4" />
                        </v-col>
                    </v-row>
                </v-form>
            </v-tabs-window-item>
            <v-tabs-window-item :value="2">
                <!-- 添加题目内容 -->
                222
            </v-tabs-window-item>
            <v-tabs-window-item :value="3">
                <!-- 预览内容 -->
                333
            </v-tabs-window-item>
        </v-tabs-window>
    </div>

    <!-- Snackbar for notifications -->
    <v-snackbar v-model="snackbar.show" :timeout="1000" :color="snackbar.color" min-width="25%">
        <div style="font-size: 16px">{{ snackbar.message }}</div>
        <template #actions>
            <v-btn icon @click="snackbar.show = false">
                <v-icon>mdi-close</v-icon>
            </v-btn>
        </template>
    </v-snackbar>
</template>

<script>
import { mapMutations } from 'vuex';

export default {
    name: 'AdminSet',
    data() {
        return {
            tab: 1,
            tempTab: 1,
            maxAllowedTab: 1,
            tabs: [
                { value: 1, label: '设置基本信息' },
                { value: 2, label: '添加题目' },
                { value: 3, label: '预览题库' }
            ],
            form: {
                name: '',
                subject: '',
                duration: null,
                description: '',
                questions: []
            },
            snackbar: {
                show: false,
                message: '',
                color: 'error'
            }
        };
    },
    mounted() {
        // 更新标题
        const title = '创建新题库';
        this.setAppTitle(title);
        this.setPageTitle(title);
    },
    methods: {
        ...mapMutations(['setAppTitle', 'setPageTitle']),
        goBack() {
            this.$router.push('/admin/problemset');
        },
        showSnackbar(message, color = 'error') {
            this.snackbar = {
                show: true,
                message,
                color
            };
        },
        async validateForm() {
            try {
                const isValid = await this.$refs.formRef.validate();
                if (!isValid) {
                    this.showSnackbar('请填写所有必填字段，并确保字段合法！');
                }
                return isValid;
            } catch (error) {
                console.error('表单验证出错：', error);
                this.showSnackbar('表单验证出错');
                return false;
            }
        },
        async beforeTabChange(newTab, oldTab) {
            if (newTab > oldTab) {
                // 只在前往后续页面时校验
                const isValid = await this.validateForm();
                console.log(isValid);
                if (!isValid.valid) {
                    this.showSnackbar('基本信息未填写或有误，请及时修改');
                    this.tempTab = oldTab; // 还原到当前页
                    return;
                }
                this.maxAllowedTab = Math.max(this.maxAllowedTab, newTab); // 解锁新页面
            }
            this.tab = newTab; // 更新实际页面索引
        }
    },
    watch: {
        tempTab(newTab, oldTab) {
            this.beforeTabChange(newTab, oldTab);
        }
    }
};
</script>

<style scoped>
.scroll-container {
    flex-direction: column;
    flex: 1 1 auto;
    overflow-y: auto;
    height: 80vh;
    max-height: 80vh;
    -ms-overflow-style: none;
    scrollbar-width: none;
}

.scroll-container::-webkit-scrollbar {
    display: none;
}
</style>
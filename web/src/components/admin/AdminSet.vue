<template>
    <v-banner sticky icon="mdi-plus" lines="one">
        <template v-slot:text>
            <div class="text-subtitle-1">作为辅导师，你可创建新的题库。</div>
        </template>

        <template v-slot:actions>
            <v-btn color="primary" class="mr-5" @click="createExercise()">
                <div class="text-subtitle-1">创建新题库</div>
            </v-btn>
        </template>
    </v-banner>
</template>

<script>
import { mapMutations } from 'vuex'; // 引入 mapMutations

export default {
    name: 'AdminSet',
    mounted() {
        // 更新标题
        const title = '题库管理';
        this.setAppTitle(title);
        this.setPageTitle(title);
    },
    methods: {
        ...mapMutations(['setAppTitle', 'setPageTitle']),
        createExercise() {
            this.$router.push("/admin/exercise/new");
        },
    },
};
</script>

<style scoped>
/* 你的样式 */
</style>
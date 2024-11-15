<template>
    <div>
        <h1>讨论页面，这个应该是具体的讨论页面</h1>
    </div>
</template>

<script>
import { mapMutations } from 'vuex'; // 引入 mapMutations

export default {
    name: 'ForumContent',
    mounted() {
        // 更新标题
        const title = '讨论';
        this.setAppTitle(title);
        this.setPageTitle(title);
    },
    methods: {
        ...mapMutations(['setAppTitle', 'setPageTitle']), // 映射 Vuex 的 mutations
    },
};
</script>

<style scoped>
/* 你的样式 */
</style>

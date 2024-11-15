<template>
    <div>
        <h1>讨论区页面</h1>
        <!-- 在这里添加更多讨论区的内容 -->
    </div>
</template>

<script>
import { mapMutations } from 'vuex'; // 引入 mapMutations

export default {
    name: 'ForumContent',
    mounted() {
        // 更新标题
        const title = '讨论区';
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

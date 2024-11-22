<template>
    <div>
        <h1>辅导师页面</h1>
    </div>
</template>

<script>
import { mapMutations } from 'vuex';

export default {
    name: 'AdminBoard',
    mounted() {
        // 更新标题
        const title = '辅导师首页';
        this.setAppTitle(title);
        this.setPageTitle(title);
    },
    methods: {
        ...mapMutations(['setAppTitle', 'setPageTitle']),
    },
};
</script>
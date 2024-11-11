<!-- src/pages/Home.vue -->
<template>
    <div>
        <Board /> 
    </div>
</template>

<script>
import Board from '../components/Board.vue';

export default {
    name: 'Home',
    components: {
        Board
    }
}
</script>

<style scoped>
/* 你的样式 */
</style>
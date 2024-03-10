<template>
    <div class="head" @click="go">
        <p>动物识别专家系统</p>
    </div>
</template>

<script>
    export default {
        name: "headers",
        methods: {
            go() {
                this.$router.push('/')
            }
        }
    }
</script>

<style scoped>

    .head {
        background: skyblue;
        height: 50px;
        /*与height保持一致使得文字居中*/
        line-height: 50px;
        text-align: center;
        font-family: 方正手迹-鲸鱼岛;
        color: black;
        font-size: 25px;
    }
    .head:hover{
        cursor:pointer
    }
</style>

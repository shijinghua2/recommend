<template>
  <div class="loading">
    数据加载中...
    <!-- <img src="../assets/loading_green.gif" alt="loading"> -->
  </div>
</template>

<script>
export default {
  name: 'loading',
  data () {
    return {}
  }
}
</script>

<style lang="scss" scoped>
.loading {
  margin: 2rem;
  margin-top:7rem;
  text-align: center;
  line-height: 5rem;
  height:5rem;
  font-size:2rem;
  font-weight: 700;
  color:#9c9c9c;
  img {
    width: 4.8rem;
  }
}
</style>

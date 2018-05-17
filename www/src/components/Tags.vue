<template>
  <div class="tags">
    <ul>
      <li v-for="(item,index) in items" :key="index">
        <router-link :to="'tag/' + item.id+'/'+encodeURIComponent(item.name)" append>
          {{item.name ? item.name : item}}
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'tags',
  props: {
    items: {
      type: Array,
      required: true
    }
  },
  data () {
    return {}
  }
}
</script>

<style lang="scss" scoped>
.tags {
  li {
    display: inline-block;
    margin: 1rem 1rem 0 0;
    font-size: 1.5rem;
  }

  a {
    display: block;
    padding: 0 1.2rem;
    line-height: 2.8rem;
    font-size: 1.5rem;
    border-radius: 2.8rem;
    text-align: center;
    color: #494949;
    background: #f5f5f5;
  }
}
</style>

<template>
  <div class="movie-view has-header">
    <!-- <sub-nav mold="quickNav"></sub-nav> -->
    <user-bar></user-bar>
    <scroller title="评分最高" type="hasCover" :items="top"></scroller>
    <scroller title="您的最爱" type="hasCover" v-if="uid" :items="topuser"></scroller>
    <scroller title="为您推荐" :loadingstr="'正在定制您的专属书籍'" type="onlyString" v-if="uid" :items="recommendtop"></scroller>
    <!-- <scroller title="热门图书榜" type="hasCover" :items="novel"></scroller>     -->
    
    <div class="types">
    <h2>分类浏览</h2>
    <div class="content">
      <ul class="type-list">
        <div class="genres">
            <tags :items="toptag"></tags>
        </div>
        <!-- <li v-for="(item,index) in itemms" :key="index">
          <a href="#">
            {{item.title}}<span></span>
          </a>
        </li> -->
      </ul>
    </div>
  </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

import Scroller from '../components/Scroller'
import UserBar from '../components/UserBar'
import SubNav from '../components/SubNav'
import Tags from '../components/Tags'

export default {
  name: 'book-view',
  components: { Scroller,UserBar, SubNav, Tags},
  data () {
    return {
      itemms:[1]
    }
  },
  computed: {
    // Getting Vuex State from store/modules/book
    ...mapState({
      novel: state => state.book.novel,
      travel: state => state.book.travel,
      top: state=>state.book.top,
      recommendtop: state=>state.book.recommendtop,
      topuser: state=>state.book.topuser,
      uid: state => state.user.uid,
      toptag:state=>state.book.toptag

    })
  },
  methods: {
    // Dispatching getBook
    getBook: function () {

      this.$store.dispatch('getBook')
      this.$store.dispatch('getTopTags',{count:10})      
      // 如果有用户登陆了
      if(this.uid){
        // 获取为用户推荐的书籍
        this.$store.dispatch('getRecommend',{
          uid:this.uid,
          count:8
        })
        // 获取用户评分过的书籍
        this.$store.dispatch('getUserRatings',{
          uid:this.uid,
          count:10
        })        
      }
      
    }
  },
  created: function created () {
    // Getting books data on created
    this.getBook()
  }
}
</script>

<style scoped>
.promItem {
  overflow: hidden;
  margin: 1.6rem 1.8rem 0.8rem 1.6rem;
}

.corver {
  float: left;
  width: 10rem;
  margin-right: 1.5rem;
}

.content {
  margin-right: 1rem;
}

.name {
  font-size: 2rem;
  color: #494949;
  margin: 1rem;
  max-width: 100%;
  line-height: 2.2rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  word-wrap: normal;
}

.price {
  float: right;
  color: #E76648;
  font-size: 1.6rem;
  line-height: 2.2rem;
}

.info {
  font-size: 1.3rem;
  font-weight: 300;
  line-height: 1.5;
  color: #9B9B9B;
}
.types {
  margin-top: 1rem;

  h2 {
    height: 2.6rem;
    line-height: 2.6rem;
    padding: 0 1.6rem;
    display: inline-block;
  }
}

.type-list {
  margin: 1.6rem 0 0 1.6rem;
  overflow: hidden;

  li {
    float: left;
    box-sizing: border-box;
    width: 50%;
    padding-right: 1.8rem;
    height: 4.2rem;
    line-height: 4.2rem;
    font-size: 1.6rem;
    border-top: solid 0.1rem #eee;
    border-right: solid 0.1rem #eee;

    a {
      color: #42bd56;
    }
  }

  li:nth-child(2n) {
    padding-left: 1.8rem;
  }

  span {
    color: #ccc;
    float: right;
    font-weight: bold;
    display: inline-block;
    border-right: solid 0.1rem #ccc;
    border-bottom: solid 0.1rem #ccc;
    width: 0.8rem;
    height: 0.8rem;
    transform: rotate(-45deg);
    margin-top: 1rem;
  }
}
</style>

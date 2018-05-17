<template>
  
  <div>
    <loading v-if="!loaded"/>
  
  <div v-else class="scroller">    
    <div class="header">
      <h2>{{title}}</h2>
    </div>
    <div class="content">
      <slot name="promItem"></slot>
      <ul class="hasCover" >
        <li v-for="(item,index) in items" :key="index" v-if="item.images.large">
          <div class="book">
            <img v-if="item.images" :src="item.images.large" alt="">            
          </div>
          <div class="rate">
            <span class="title">{{item.title}}</span>
            <a href="#" class="ratebtn" @click="getrating(item.id,status[item.id])">
              <template v-if="status[item.id]==-1">
                <i class="icon-loading"  /> 获取中
              </template>
              <template v-if="!status[item.id]">
                获取评分
              </template>
              <template v-if="status[item.id] && status[item.id] !=-1">
                {{status[item.id]}}
              </template>
              
            </a>
          </div>
        </li>
      </ul>
      <ul class="onlyString" v-if="false">
        <li v-for="(item,index) in items" :key="index" style="border-color: #FFAC2D;">
          <a :href="item.href" v-if="!item.line" :style="{color: item.color}">{{item.title}}</a>
        </li>
      </ul>
    </div>
  </div>
  </div>
</template>

<script>
import request from "superagent";
import common from "../store/modules/common";
import loading from "./Loading";
import { mapState } from "vuex";

export default {
  name: "scroller",
  data() {
    return {
      items: [],
      title: decodeURIComponent(this.$route.params.name),
      status: {},
      loaded: false
    };
  },
  components: { loading },
  computed: {
    // Getting Vuex State from store/modules/book
    ...mapState({
      uid: state => state.user.uid
    })
  },
  watch: {
    status: {
      handler: (n, o) => {},
      deep: true
    }
  },
  methods: {
    getrating(isbn, flag) {
      if (flag !== undefined) {
        return;
      }
      if (!this.uid) {
        this.$route.push({ name: "LoginView" });
      }
      this.$set(this.status, isbn, -1);

      request
        .get(common.apiUrl(`ratings/${this.uid}/${isbn}`))

        .end((err, res) => {
          if (err) return;
          let body = JSON.parse(res.text);
          this.$set(this.status, isbn, body[0].Rating.toFixed(1));
        });
    }
  },
  created() {
    request
      .get(common.apiUrl(`top_tag_books/${this.$route.params.id}/${8}`))
      .end((err, res) => {
        if (err) return;
        this.loaded = true;
        if (!res.body) {
          res.body = JSON.parse(res.text);
        }
        this.items = res.body.map(x => {
          return {
            id: x.isbn,
            images: {
              large: x.imgl,
              medium: x.imgm,
              small: x.imgs
            },
            title: x.title,
            isbn10: x.isbn,
            rating: {
              average: x.avgr,
              min: 0,
              max: 10,
              numraters: 2
            }
          };
        });
      });
  }
};
</script>

<style lang="scss" scoped>
.scroller {
  padding-top: 1rem;
}

.header {
  height: 2.6rem;
  line-height: 2.6rem;
  padding: 0 1.6rem;

  a {
    float: right;
    font-size: 1.44rem;
    &:last-child {
      color: #42bd56;
    }
  }

  h2 {
    display: inline-block;
  }
}

.content {
  box-sizing: content-box;

  ul {
    padding: 0.8rem 0;
  }
}

.hasCover {
  overflow-x: auto;
  white-space: nowrap;

  .title {
    display: block;
    line-height: 1.4;
    font-size: 1.6rem;
    color: #111;
    overflow: hidden;
    white-space: normal;
  }

  li {
    // display: inline-block;
    display: flex;
    padding: 1rem;
    .book {
      width: 10rem;
    }
    .rate {
      position: relative;
      flex: 1;
      padding-left: 2rem;
      width: 0;
      .ratebtn {
        position: absolute;
        right: 0.5rem;
        bottom: 0.5rem;
        font-size: 1.5rem;
        padding: 0.7rem 1.5rem;
        font-size: 1.7rem;
        text-align: center;
        color: #fff;
        background: #17aa52;
        border: 0.1rem solid #17aa52;
        border-radius: 0.3rem;
      }
    }
  }

  li:first-child {
    padding-left: 0.8rem;
  }

  img {
    height: 15rem;
  }
}

.icon-loading {
  display: inline-block;
  width: 1.8rem;
  height: 1.8rem !important;
  background: url(../assets/loading.gif) 0 0/100% 100% no-repeat;
}

.onlyString {
  overflow-x: auto;
  white-space: nowrap;

  li {
    //display: inline-block;
    display: block;
    margin: 0 0 0.8rem 1.6rem;
    font-size: 1.6rem;
    border: solid 0.1rem;
    border-radius: 0.4rem;
    vertical-align: middle;
  }

  a {
    height: 5rem;
    line-height: 5rem;
    padding: 0 2.4rem;
    letter-spacing: 0.16rem;
    overflow: auto;
    display: block;
    text-align: center;
  }

  li:empty {
    width: 100%;
    display: block;
    height: 0.1rem;
    border: 0;
    margin: 0;
  }
}
</style>

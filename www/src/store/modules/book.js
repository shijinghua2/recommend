import request from 'superagent'
import jsonp from 'superagent-jsonp'
import common from './common'

const state = {
  novel: [],          // 小说 豆瓣
  travel: [],         // 旅行 豆瓣
  top: [],            // 评分最高 sqlite
  recommendtop:[]     // 推荐算法 spark
}


const mutations = {
  getBook(state, payload) {
    switch (payload.tag) {
      case 'novel':
        state.novel = payload.res
        break
      case 'travel':
        state.travel = payload.res
        break
      case 'top':
        state.top = payload.res
        break
      case 'recommendtop':
        state.recommendtop=payload.res
        break
      default:
        state.novel = payload.res
    }
  }
}

const actions = {

  getRecommend({
    commit
  },payload) {
      request
        .get(common.apiUrl(`ratings/top/${payload.uid}/${payload.count}`))
        .end((err, res) => {
          if (err) return
          if (!res.body) {
            res.body = JSON.parse(res.text)
          }
          commit({
            type: 'getBook',
            tag: 'recommendtop',
            res: res.body.map(x => {
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
              }
            })
          })
        })


  },


  /**
   * Getting books
   * q: 虚构类, 非虚构类, 旅行
   * count: 8
   */
  getBook({
    commit
  }) {
    request
      .get('https://api.douban.com/v2/book/search?q=虚构类&count=8')
      .use(jsonp)
      .end((err, res) => {
        if (!err) {
          commit({
            type: 'getBook',
            tag: 'novel',
            res: res.body.books
          })
        }
      })
    request
      .get('https://api.douban.com/v2/book/search?q=旅行&count=8')
      .use(jsonp)
      .end((err, res) => {
        if (!err) {
          commit({
            type: 'getBook',
            tag: 'travel',
            res: res.body.books
          })
        }
      })

    request
      .get(common.apiUrl('top_books/20'))
      .end((err, res) => {
        if (err) return
        if (!res.body) {
          res.body = JSON.parse(res.text)
        }
        commit({
          type: 'getBook',
          tag: 'top',
          res: res.body.map(x => {
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
            }
          })
        })
      })


  }
}

export default {
  state,
  mutations,
  actions
}

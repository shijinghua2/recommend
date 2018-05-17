import request from 'superagent'
import jsonp from 'superagent-jsonp'
import common from './common'

const state = {
  novel: [], // 小说 豆瓣
  travel: [], // 旅行 豆瓣
  top: [], // 评分最高 sqlite
  recommendtop: [], // 推荐算法 spark
  topuser: [], // 用户评分过的书籍
  toptag:[]
  
}

const mutations = {
  getBook(state, payload) {
    switch (payload.tag) {
      case 'top':
        state.top = payload.res
        break
      case 'recommendtop':
        state.recommendtop = payload.res
        break
      case 'topuser':
        state.topuser = payload.res
        break
      case 'toptag':
        state.toptag = payload.res
        break
    }
  }
}

const actions = {

  getRecommend({
    commit
  }, payload) {
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
              title: x.Title,
              isbn10: x.isbn,
              rating: {
                average: x.Rating,
                min: 0,
                max: 10,
                numraters: x.Count
              },
              href: 'javascript:void(0)',
              color: '#333'
            }
          })
        })
      })
  },

  getUserRatings({
    commit
  }, payload) {
    request
      .get(common.apiUrl(`top_user_books/${payload.uid}/${payload.count}`))

      .end((err, res) => {
        if (err) return
        if (!res.body) {
          res.body = JSON.parse(res.text)
        }
        commit({
          type: 'getBook',
          tag: 'topuser',
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

    request
      .get(common.apiUrl(`top_tags/10`))
      .end((err, res) => {
        if (err) return
        if (!res.body) {
          res.body = JSON.parse(res.text)
        }
        commit({
          type: 'getBook',
          tag: 'toptag',
          res: res.body.map(x => {
            return {
              id: x.id,
              name: x.name,
              avgr: x.avgr
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

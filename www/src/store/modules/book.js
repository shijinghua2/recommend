import request from 'superagent'
import jsonp from 'superagent-jsonp'

const state = {
  novel: [],
  travel: []
}

const mutations = {
  getBook (state, payload) {
    switch (payload.tag) {
      case 'novel':
        state.novel = payload.res
        break
      case 'travel':
        state.travel = payload.res
        break
      default:
        state.novel = payload.res
    }
  }
}

const actions = {
  /**
   * Getting books
   * q: 虚构类, 非虚构类, 旅行
   * count: 8
   */
  getBook ({ commit }) {
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
  }
}

export default {
  state,
  mutations,
  actions
}

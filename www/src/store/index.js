import Vue from 'vue'
import Vuex from 'vuex'

import book from './modules/book'
import subject from './modules/subject'
import group from './modules/group'
import search from './modules/search'
import user from './modules/user'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    book,
    subject,
    group,
    search,
    user
  }
})

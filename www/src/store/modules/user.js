import request from 'superagent'

const api='http://127.0.0.1:5432'
let apiUrl=function(url){
  return `${api}/${url}`
}
const state = {
  uid:'',
  location:'',
  age:''
}

const getters = {
  // Filtering currentUser
  currentUser: state => {
    return {
      uid: state.uid,
      guid: state.guid,
      location: state.location,
      age: state.age
    }
  }
}

const mutations = {
  updateData (state, payload) {
    switch (payload.name) {
      case 'uid':
        state.uid = payload.value
        break
      case 'guid':
        state.guid = payload.value
        break
      case 'location':
        state.location = payload.name
        break
      default:
        console.log('Error:Dont directly mutate Vuex store')
    }
  },
  getLocalUser (state) {
    state.uid = localStorage.getItem('uid')
    state.location = localStorage.getItem('location')
    state.age = localStorage.getItem('age')
    state.guid = localStorage.getItem('guid')
  },
  setUser (state, payload) {
    state.uid = payload.uid
    state.location = payload.location
    state.age = payload.age

    state.guid = payload.guid
  },
  logout (state) {
    localStorage.removeItem('uid')
    localStorage.removeItem('loation')
    localStorage.removeItem('age')
    localStorage.removeItem('guid')

    state.uid = ''
    state.location = ''
    state.guid = ''
    state.age=''
  }
}

const actions = {
  /**
   * Login
   * new Promise((resolve, reject) => {})
   * Authorization: 'Bearer ' + token
   * email: payload.email
   * pass: payload.pass
   * name: payload.name
   */
  login ({ commit }, payload) {
    return new Promise((resolve, reject) => {
      request
        .post(apiUrl ('login/' + payload.uid))

        .then(res => {
          commit({
            type: 'setUser',
            uid: res.body.uid,
            guid: res.body.guid,
            location: res.body.location,
            age: res.body.age
          })
          resolve(res)
        }, err => {
          reject(err)
        })
    })
  }
}

export default {
  state,
  getters,
  mutations,
  actions
}

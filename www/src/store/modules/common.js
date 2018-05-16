let common={}

let api = 'http://127.0.0.1:5432'

api='http://47.106.32.55:5432'
common.apiUrl = function (url) {
  return `${api}/${url}`
}

export default common

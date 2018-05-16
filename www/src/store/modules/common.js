let common={}

const api = 'http://127.0.0.1:5432'

common.apiUrl = function (url) {
  return `${api}/${url}`
}

export default common

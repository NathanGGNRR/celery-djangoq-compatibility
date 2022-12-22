import axios from 'axios'

const BASE_URL = 'http://localhost:8000/example/file/'

export default {
  generateNewOnes: (asyncRule, multiple, quantity) => axios.post(`${BASE_URL}generate/`, { asyncRule, multiple, quantity }),
  retrieve: () => axios.get(BASE_URL),
  deleteAll: () => axios.delete(`${BASE_URL}generate/`),
  retrieveCeleryInfo: () => axios.get(`${BASE_URL}retrieve/`)
}

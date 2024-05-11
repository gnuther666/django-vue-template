import axios from 'axios'

export const ServerUrl = import.meta.env.VITE_BACKEND_PATH
console.log('后端地址', ServerUrl)
const http = axios.create({
  baseURL: ServerUrl, // 开发环境
  timeout: 10000, // 请求超时时间
})
// 添加请求拦截器
http.interceptors.request.use(
  (config) => {
    // 在发送请求之前做些什么
    config.headers['Authorization'] = 'Bearer ' + localStorage.getItem('access_token')
    return config
  },
  (error) => {
    // 对请求错误做些什么
    return Promise.reject(error)
  }
)

// 添加响应拦截器
http.interceptors.response.use(
  (response) => {
    // 对响应数据做些什么
    return response.data
  },
  (error) => {
    // 对响应错误做些什么
    if (error.response && error.response.status === 401) {
      // 登录失效，跳转到登录页面
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default http
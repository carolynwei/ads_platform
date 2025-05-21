import axios from 'axios'
import router from '@/router' // 用于路由跳转，比如登录页

// 创建 axios 实例，配置基础路径和超时时间
const service = axios.create({
  baseURL: 'http://localhost:8000/api', // 根据后端接口地址调整
  timeout: 5000,
  // 如果你的后端用的是 Cookie 认证，需要加这个
  // withCredentials: true,
})

// 请求拦截器：发送请求之前执行
service.interceptors.request.use(
  config => {
    // 从 localStorage 取 access_token
    const token = localStorage.getItem('access_token')
    if (token) {
      // 在请求头加入 token，格式是 Bearer + 空格 + token
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    // 请求错误，直接返回拒绝 Promise
    return Promise.reject(error)
  }
)

// 响应拦截器：接收响应后执行
service.interceptors.response.use(
  response => {
    // 成功响应，直接返回响应数据（即 response.data）
    return response.data
  },
  error => {
    // 请求失败会走这里
    if (error.response) {
      const status = error.response.status

      // 根据状态码做不同处理
      switch (status) {
        case 401:
          // 401未授权，通常是token过期或未登录
          alert('登录已过期，请重新登录')
          // 清除本地存储的token
          localStorage.removeItem('access_token')
          // 跳转登录页
          router.push('/login')
          break
        case 403:
          alert('没有权限访问该资源')
          break
        case 404:
          alert('请求资源不存在')
          break
        case 500:
          alert('服务器内部错误，请稍后重试')
          break
        default:
          alert(`请求失败，错误码：${status}`)
      }
    } else {
      // 网络错误或者服务器无响应
      alert('网络错误，请检查你的网络连接')
    }
    // 返回 Promise 拒绝，让调用处能 catch 到错误
    return Promise.reject(error)
  }
)

export default service

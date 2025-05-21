// src/api/user.js
import service from './index'

// 用户注册
export function register(data) {
  return service.post('/users/register/', data)
}

// 用户登录，获取 JWT token
export function login(data) {
  return service.post('/users/login/', data).then(res => {
    const { access, refresh } = res
    if (access && refresh) {
      localStorage.setItem('token', access)
      localStorage.setItem('refresh', refresh)
    }
    return res
  })
}

// 刷新 token
export function refreshToken(refreshToken) {
  return service.post('/users/token/refresh/', { refresh: refreshToken }).then(res => {
    const { access } = res
    if (access) {
      localStorage.setItem('token', access)
    }
    return res
  })
}

// 获取当前登录用户信息（带 token）
export function getMe() {
  const token = localStorage.getItem('token')
  return service.get('/users/me/', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
}

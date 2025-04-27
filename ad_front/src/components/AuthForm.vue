<template>
    <div class="modal-overlay" @click.self="closeModal">
      <div class="modal-container">
        <!-- 登录表单 -->
        <div v-if="mode === 'login'" class="auth-form">
          <h2>登录</h2>
          <form @submit.prevent="handleLogin">
            <div class="form-group">
              <label for="login-username">用户名</label>
              <input 
                id="login-username" 
                v-model="loginForm.username" 
                type="text" 
                required 
                placeholder="请输入用户名"
              >
            </div>
            <div class="form-group">
              <label for="login-password">密码</label>
              <input 
                id="login-password" 
                v-model="loginForm.password" 
                type="password" 
                required 
                placeholder="请输入密码"
              >
            </div>
            <button type="submit" class="submit-button">登录</button>
          </form>
          <p class="switch-mode">
            还没有账号？<a href="#" @click.prevent="switchMode('register')">立即注册</a>
          </p>
        </div>
          <!-- 注册表单 -->
        <div v-if="mode === 'register'" class="auth-form compact">
          <h2>注册</h2>
          <form @submit.prevent="handleRegister">
            <div class="form-group">
              <label for="register-username">用户名</label>
              <input 
                id="register-username" 
                v-model="registerForm.username" 
                type="text" 
                required 
                placeholder="请输入用户名"
              >
            </div>
            <div class="form-group">
              <label for="register-email">邮箱</label>
              <input 
                id="register-email" 
                v-model="registerForm.email" 
                type="email" 
                required 
                placeholder="请输入邮箱"
              >
            </div>
            <div class="form-group">
              <label for="register-password">密码</label>
              <input 
                id="register-password" 
                v-model="registerForm.password" 
                type="password" 
                required 
                placeholder="请输入密码"
              >
            </div>
            <div class="form-group">
              <label for="register-confirm-password">确认密码</label>
              <input 
                id="register-confirm-password" 
                v-model="registerForm.confirmPassword" 
                type="password" 
                required 
                placeholder="请再次输入密码"
              >
            </div>
            
            <!-- 横向排列的身份选项 -->
            <div class="identity-section">
      <div class="identity-label">身份</div>
      <div class="identity-options">
        <div class="identity-option" 
             :class="{active: registerForm.role === 'user'}"
             @click="registerForm.role = 'user'">
          <div class="radio-button"></div>
          <span>普通用户</span>
        </div>
        <div class="identity-option" 
             :class="{active: registerForm.role === 'admin'}"
             @click="registerForm.role = 'admin'">
          <div class="radio-button"></div>
          <span>管理员</span>
        </div>
      </div>
    </div>
            
            <button type="submit" class="submit-button">注册</button>
          </form>
          <p class="switch-mode">
            已有账号？<a href="#" @click.prevent="switchMode('login')">立即登录</a>
          </p>
        </div>
        
        <button class="close-button" @click="closeModal">×</button>
      </div>
    </div>
  </template>
 
<script>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'

export default {
  props: {
    initialMode: {
      type: String,
      default: 'login',
      validator: (value) => ['login', 'register'].includes(value)
    }
  },
  emits: ['close', 'switch-mode'],
  setup(props, { emit }) {
    const router = useRouter()
    const mode = ref(props.initialMode)
    
    const loginForm = ref({
      username: '',
      password: ''
    })
    
    const registerForm = ref({
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      role: 'user'
    })

    const switchMode = (newMode) => {
      mode.value = newMode
      emit('switch-mode', newMode)
    }

    const closeModal = () => {
      emit('close')
    }

    const handleLogin = () => {
      // 模拟用户数据库
      const validUsers = {
        admin: { password: 'admin123', name: '管理员', age: 30 },
        user1: { password: 'user1123', name: '普通用户', age: 25 }
      }

      const user = validUsers[loginForm.value.username]
      
      if (user && user.password === loginForm.value.password) {
        // 存储完整用户信息
        localStorage.setItem('currentUser', JSON.stringify({
          username: loginForm.value.username,
          name: user.name,
          age: user.age,
          role: user.role || 'user'
        }))
        
        closeModal()
        router.push('/dashboard') // 跳转到仪表盘
      } else {
        // 清空密码栏
    loginForm.value.password = ''
    // 聚焦到密码输入框
    document.getElementById('login-password')?.focus()
    alert('用户名或密码错误')
      }
    }

    const handleRegister = () => {
      if (registerForm.value.password !== registerForm.value.confirmPassword) {
        alert('两次输入的密码不匹配!')
        return
      }
      
      // 模拟注册成功
      localStorage.setItem('currentUser', JSON.stringify({
        username: registerForm.value.username,
        name: '新用户',
        age: 18,
        role: registerForm.value.role
      }))
      
      alert(`注册成功, ${registerForm.value.username}!`)
      closeModal()
      router.push('/dashboard')
    }

    watch(() => props.initialMode, (newVal) => {
      mode.value = newVal
    })

    return {
      mode,
      loginForm,
      registerForm,
      switchMode,
      closeModal,
      handleLogin,
      handleRegister
    }
  }
}
</script>
  <style scoped>
  /* 新增的身份选择区域样式 */
  .identity-section {
    margin: 16px 0;
    border-top: 1px solid #f0f0f0;
    padding-top: 12px;
  }
  .identity-label {
    font-size: 14px;
    color: #2c3e50;
    margin-bottom: 8px;
    font-weight: 500;
  }
  .identity-options {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  /* 原有身份选项样式保持不变 */
  .identity-option {
    display: flex;
    align-items: center;
    padding: 8px 12px;
    cursor: pointer;
    transition: all 0.2s;
    border-radius: 4px;
  }
  .identity-option:hover {
    background-color: #f8f8f8;
  }
  .identity-option.active {
    font-weight: 500;
  }
  .radio-button {
    width: 16px;
    height: 16px;
    border: 2px solid #999;
    border-radius: 50%;
    margin-right: 12px;
    position: relative;
  }
  .identity-option.active .radio-button {
    border-color: #3498db;
  }
  .identity-option.active .radio-button::after {
    content: '';
    position: absolute;
    top: 3px;
    left: 3px;
    width: 6px;
    height: 6px;
    background-color: #3498db;
    border-radius: 50%;
  }
  .identity-option span {
    font-size: 14px;
    color: #333;
  }
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    padding: 20px; /* 添加外层边距，避免顶着页面边缘 */
  }
  .modal-container {
    position: relative;
    background-color: white;
    padding: 1.5rem;
    border-radius: 8px;
    width: 100%;
    max-width: 380px; /* 稍微缩小宽度 */
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    margin: auto; /* 确保居中 */
  }
  .close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #7f8c8d;
  }
  .close-button:hover {
    color: #2c3e50;
  }
  .auth-form {
    padding: 0.8rem; /* 减小内边距 */
  }
  .auth-form h2 {
    margin-bottom: 1.2rem; /* 减小标题下方间距 */
    color: #2c3e50;
    text-align: center;
    font-size: 1.3rem; /* 减小标题字体 */
  }
  .form-group {
    margin-bottom: 0.6rem; /* 减小表单项间距 */
  }
  .form-group label {
    display: block;
    margin-bottom: 0.3rem; /* 减小标签与输入框间距 */
    color: #2c3e50;
    font-weight: 500;
    font-size: 0.85rem; /* 减小标签字体 */
  }
  .form-group input {
    width: 100%;
    padding: 0.6rem 0.8rem; /* 减小输入框内边距 */
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 0.85rem; /* 减小输入文字 */
  }
  .form-group input:focus {
    border-color: #3498db;
    outline: none;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
  }
  /* 身份选择样式 - 与标签同行 */
  .form-group.role-group {
    display: flex;
    align-items: center; /* 垂直居中 */
    gap: 0.8rem; /* 标签和选项间距 */
    margin: 0.8rem 0;
  }
  .form-group.role-group label {
    margin-bottom: 0;
    white-space: nowrap; /* 防止标签换行 */
  }
  .role-options {
    display: flex;
    gap: 1rem; /* 选项间距 */
  }
  .role-option {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    cursor: pointer;
    font-size: 0.85rem; /* 与输入框字体一致 */
  }
  .submit-button {
    width: 100%;
    padding: 0.7rem; /* 减小按钮内边距 */
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 0.9rem; /* 减小按钮字体 */
    cursor: pointer;
    margin-top: 0.8rem; /* 减小按钮上方间距 */
    transition: background-color 0.3s;
  }
  .submit-button:hover {
    background-color: #2980b9;
  }
  .switch-mode {
    text-align: center;
    margin-top: 0.8rem; /* 减小切换链接上方间距 */
    color: #7f8c8d;
    font-size: 0.85rem; /* 减小字体 */
  }
  .switch-mode a {
    color: #3498db;
    text-decoration: none;
  }
  .switch-mode a:hover {
    text-decoration: underline;
  }
  </style>
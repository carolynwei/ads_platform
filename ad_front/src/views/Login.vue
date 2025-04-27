<template>
  <div class="app-container">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="logo">广告平台</div>
      <div class="nav-links">
        <a href="#" @click.prevent="showLogin">登录</a>
        <a href="#" @click.prevent="showRegister">注册</a>
      </div>
    </nav>
    <!-- 主要内容 -->
    <main class="main-content">
      <section class="hero-section">
        <h1>专业的广告投放平台</h1>
        <p>为您提供精准、高效的广告投放解决方案</p>
        <button class="cta-button" @click="showRegister">立即注册</button>
      </section>
      <section class="features-section">
        <div class="feature-card">
          <h3>精准投放</h3>
          <p>基于大数据分析的精准用户定位</p>
        </div>
        <div class="feature-card">
          <h3>实时监控</h3>
          <p>广告效果实时监测与反馈</p>
        </div>
        <div class="feature-card">
          <h3>多种形式</h3>
          <p>支持图文、视频等多种广告形式</p>
        </div>
      </section>
    </main>
    <!-- 登录注册模态框 -->
    <AuthModal 
      v-if="showAuthModal"
      :initialMode="authMode"
      @close="closeAuthModal"
      @switch-mode="switchAuthMode"
    />
  </div>
</template>
<script>
import { ref } from 'vue'
import AuthModal from '@/components/AuthForm.vue'
export default {
  components: {
    AuthModal
  },
  setup() {
    const showAuthModal = ref(false)
    const authMode = ref('login') // 'login' 或 'register'
    // 显示登录模态框
    const showLogin = () => { 
      authMode.value = 'login'
      showAuthModal.value = true
    }
    // 显示注册模态框
    const showRegister = () => {
      authMode.value = 'register'
      showAuthModal.value = true
    }
    // 关闭模态框
    const closeAuthModal = () => {
      showAuthModal.value = false
    }
    // 切换登录/注册模式
    const switchAuthMode = (mode) => {
      authMode.value = mode
    }
    return {
      showAuthModal,
      authMode,
      showLogin,
      showRegister,
      closeAuthModal,
      switchAuthMode
    }
  }
}
</script>
<style scoped>
/* 全局样式 */
.app-container {
  font-family: 'Arial', sans-serif;
  color: #333;
}
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #2c3e50;
  color: white;
}
.logo {
  font-size: 1.5rem;
  font-weight: bold;
}
.nav-links a {
  color: white;
  margin-left: 1rem;
  text-decoration: none;
  cursor: pointer;
}
.nav-links a:hover {
  text-decoration: underline;
}
.main-content {
  padding: 2rem;
}
.hero-section {
  text-align: center;
  padding: 4rem 0;
  background-color: #f8f9fa;
  margin-bottom: 2rem;
}
.hero-section h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}
.hero-section p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  color: #666;
}
.cta-button {
  padding: 0.8rem 1.5rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}
.cta-button:hover {
  background-color: #2980b9;
}
.features-section {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 1rem;
}
.feature-card {
  flex: 1;
  min-width: 200px;
  padding: 1.5rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}
.feature-card h3 {
  margin-bottom: 0.5rem;
  color: #2c3e50;
}
.feature-card p {
  color: #7f8c8d;
}
</style>
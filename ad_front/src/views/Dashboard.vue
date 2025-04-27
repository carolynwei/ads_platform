<template>
  <div class="home-container">
    <!-- 顶部导航栏 -->
    <header class="dashboard-header">
      <div class="logo">广告平台</div>
      <nav class="main-nav">
        <router-link to="/home">首页</router-link>
        
        <!-- 广告管理（带下拉菜单） -->
        <div class="nav-item with-dropdown" @mouseenter="showAdMenu = true" @mouseleave="showAdMenu = false">
          <router-link to="/ads">广告管理</router-link>
          <transition name="fade">
            <div v-show="showAdMenu" class="dropdown-menu">
              <router-link to="/ads/list">我的广告</router-link>
              <router-link to="/ads/api">广告接口</router-link>
            </div>
          </transition>
        </div>
        
        <router-link to="/account">我的账户</router-link>
        <router-link to="/profile">个人中心</router-link>
      </nav>
      <div class="user-info">
        <span>{{ userName }}</span>
        <button @click="logout">退出</button>
      </div>
    </header>

    <!-- 内容区 -->
    <main class="dashboard-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const showAdMenu = ref(false)

// 获取当前用户信息
const user = ref(JSON.parse(localStorage.getItem('currentUser')) || {})
const userName = computed(() => user.value.name || user.value.username || '用户')

// 退出登录
const logout = () => {
  localStorage.removeItem('currentUser')
  router.push('/login')
}
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.dashboard-header {
  display: flex;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background: #2c3e50;
  color: white;
  position: relative;
}

.logo {
  font-size: 20px;
  font-weight: bold;
  margin-right: 40px;
}

.main-nav {
  display: flex;
  gap: 15px;
  height: 100%;
}

.main-nav > a,
.main-nav > .nav-item > a {
  display: flex;
  align-items: center;
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  padding: 0 15px;
  height: 100%;
  position: relative;
}

.main-nav a:hover,
.main-nav a.router-link-active {
  color: white;
  background: rgba(255,255,255,0.1);
}

.nav-item {
  position: relative;
  height: 100%;
}

.with-dropdown {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  min-width: 160px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  border-radius: 4px;
  z-index: 100;
}

.dropdown-menu a {
  display: block;
  padding: 10px 15px;
  color: #333 !important;
}

.dropdown-menu a:hover {
  background: #f5f5f5;
  color: #2c3e50 !important;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.user-info {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-info button {
  background: transparent;
  color: white;
  border: 1px solid rgba(255,255,255,0.5);
  border-radius: 4px;
  padding: 3px 10px;
  cursor: pointer;
}

.dashboard-content {
  flex: 1;
  padding: 20px;
  background: #f5f7fa;
}
</style>
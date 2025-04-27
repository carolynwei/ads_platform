<template>
    <div class="profile-container">
      <!-- 面包屑导航 -->
      <div class="breadcrumb">
        <router-link to="/home">首页</router-link>
        <span class="separator">/</span>
        <span>个人中心</span>
      </div>
  
      <!-- 返回按钮（移动端更显眼） -->
      <button class="back-button" @click="goToHome">
        <span class="icon">←</span> 返回首页
      </button>
      
      <h2 class="profile-title">个人中心</h2>
      
      <div class="profile-card">
        <div class="avatar-section">
          <div class="avatar">
            {{ userAvatar }}
          </div>
          <h3 class="username">{{ user.username }}</h3>
          <el-tag :type="user.role === 'admin' ? 'danger' : ''" class="role-tag">
            {{ user.role === 'admin' ? '管理员' : '普通用户' }}
          </el-tag>
        </div>
  
        <div class="info-section">
          <div class="info-item">
            <span class="info-label">用户名：</span>
            <span class="info-value">{{ user.username }}</span>
          </div>
          
          <div class="info-item">
            <span class="info-label">电子邮箱：</span>
            <span class="info-value">{{ user.email || '未绑定' }}</span>
            <el-button 
              v-if="user.email" 
              type="text" 
              size="small"
              @click="showEmailDialog = true"
            >
              修改
            </el-button>
            <el-button 
              v-else 
              type="text" 
              size="small"
              @click="showEmailDialog = true"
            >
              绑定邮箱
            </el-button>
          </div>
          
          <div class="info-item">
            <span class="info-label">注册时间：</span>
            <span class="info-value">{{ formatDate(user.registerTime) }}</span>
          </div>
          
          <div class="info-item">
            <span class="info-label">最后登录：</span>
            <span class="info-value">{{ formatDate(user.lastLogin) }}</span>
          </div>
        </div>
      </div>
  
      <!-- 修改邮箱对话框 -->
      <el-dialog
        v-model="showEmailDialog"
        title="修改邮箱"
        width="30%"
      >
        <el-form :model="emailForm" :rules="emailRules" ref="emailFormRef">
          <el-form-item label="新邮箱地址" prop="email">
            <el-input v-model="emailForm.email" placeholder="请输入有效邮箱"></el-input>
          </el-form-item>
          <el-form-item label="验证码" prop="code" v-if="emailForm.email">
            <div class="code-input">
              <el-input v-model="emailForm.code" placeholder="6位验证码"></el-input>
              <el-button 
                type="primary" 
                :disabled="!emailForm.email || isSending"
                @click="sendVerificationCode"
              >
                {{ isSending ? `${countdown}秒后重发` : '获取验证码' }}
              </el-button>
            </div>
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="showEmailDialog = false">取消</el-button>
          <el-button type="primary" @click="updateEmail">确认修改</el-button>
        </template>
      </el-dialog>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  // 返回首页方法
  const goToHome = () => {
    router.push('/dashboard')
  }
  // 用户数据
  const user = ref({
    username: 'advertiser1',
    email: 'user@example.com',
    role: 'user', // admin/user
    registerTime: '2023-06-15T08:30:00',
    lastLogin: new Date().toISOString()
  })
  
  // 从本地存储获取真实用户数据
  onMounted(() => {
    const savedUser = JSON.parse(localStorage.getItem('currentUser'))
    if (savedUser) {
      user.value = { ...user.value, ...savedUser }
    }
  })
  
  // 生成用户头像
  const userAvatar = computed(() => {
    return user.value.username.charAt(0).toUpperCase()
  })
  
  // 邮箱修改相关
  const showEmailDialog = ref(false)
  const emailForm = ref({
    email: '',
    code: ''
  })
  const emailFormRef = ref(null)
  const isSending = ref(false)
  const countdown = ref(60)
  
  const emailRules = {
    email: [
      { required: true, message: '请输入邮箱地址', trigger: 'blur' },
      { type: 'email', message: '请输入正确的邮箱格式', trigger: ['blur', 'change'] }
    ],
    code: [
      { required: true, message: '请输入验证码', trigger: 'blur' },
      { len: 6, message: '验证码长度为6位', trigger: 'blur' }
    ]
  }
  
  // 发送验证码
  const sendVerificationCode = () => {
    isSending.value = true
    const timer = setInterval(() => {
      if (countdown.value <= 0) {
        clearInterval(timer)
        isSending.value = false
        countdown.value = 60
      } else {
        countdown.value--
      }
    }, 1000)
    
    // 模拟发送验证码
    setTimeout(() => {
      ElMessage.success(`验证码已发送至 ${emailForm.value.email}`)
    }, 1000)
  }
  
  // 更新邮箱
  const updateEmail = () => {
    emailFormRef.value.validate(valid => {
      if (valid) {
        // 这里应该是API调用
        user.value.email = emailForm.value.email
        showEmailDialog.value = false
        ElMessage.success('邮箱更新成功')
        emailForm.value = { email: '', code: '' }
      }
    })
  }
  
  // 格式化日期
  const formatDate = (dateString) => {
    if (!dateString) return '未知'
    const date = new Date(dateString)
    return date.toLocaleString()
  }
  </script>
  
  <style scoped>
  .profile-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .profile-title {
    text-align: center;
    margin-bottom: 30px;
    color: #333;
  }
  
  .profile-card {
    display: flex;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
    overflow: hidden;
  }
  
  .avatar-section {
    width: 250px;
    padding: 30px;
    background: #f5f7fa;
    text-align: center;
  }
  
  .avatar {
    width: 100px;
    height: 100px;
    margin: 0 auto 20px;
    background: #409eff;
    color: white;
    font-size: 40px;
    line-height: 100px;
    text-align: center;
    border-radius: 50%;
  }
  
  .username {
    margin: 10px 0;
    font-size: 18px;
  }
  
  .role-tag {
    margin-top: 10px;
  }
  
  .info-section {
    flex: 1;
    padding: 30px;
  }
  
  .info-item {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 1px dashed #eee;
  }
  
  .info-label {
    width: 100px;
    color: #909399;
  }
  
  .info-value {
    flex: 1;
    color: #606266;
  }
  
  .code-input {
    display: flex;
    gap: 10px;
  }
  
  /* 响应式设计 */
  @media (max-width: 768px) {
    .profile-card {
      flex-direction: column;
    }
    
    .avatar-section {
      width: 100%;
      padding: 20px 0;
    }
    
    .info-item {
      flex-wrap: wrap;
    }
    
    .info-label {
      width: 100%;
      margin-bottom: 5px;
    }
  }
  .breadcrumb {
  margin-bottom: 20px;
  font-size: 14px;
  color: #606266;
}

.breadcrumb a {
  color: #409eff;
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.separator {
  margin: 0 8px;
  color: #c0c4cc;
}

.back-button {
  display: none; /* 默认隐藏，移动端显示 */
  background: none;
  border: none;
  color: #409eff;
  cursor: pointer;
  margin-bottom: 15px;
  padding: 8px 12px;
  border-radius: 4px;
}

.back-button:hover {
  background-color: #ecf5ff;
}

.back-button .icon {
  margin-right: 5px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .breadcrumb {
    display: none;
  }
  
  .back-button {
    display: inline-block;
  }
}
</style>
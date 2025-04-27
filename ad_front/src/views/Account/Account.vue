<template>
   <div class="account-container">
    <!-- 面包屑导航（PC端） -->
    <div class="breadcrumb">
      <router-link to="/home">首页</router-link>
      <span class="separator">/</span>
      <span>我的账户</span>
    </div>

    <h2 class="account-title">我的账户</h2>
      <!-- 账户概览 -->
      <div class="balance-card">
        <div class="balance-info">
          <span class="balance-label">账户余额</span>
          <span class="balance-amount">¥ {{ balance.toFixed(2) }}</span>
        </div>
        <button class="recharge-btn" @click="showRechargeDialog = true">立即充值</button>
      </div>
  
      <!-- 充值记录 -->
      <div class="section">
        <h3 class="section-title">充值记录</h3>
        <div class="record-list">
          <div v-for="record in rechargeRecords" :key="record.id" class="record-item">
            <div class="record-detail">
              <span class="record-type">{{ record.type }}</span>
              <span class="record-time">{{ formatDate(record.time) }}</span>
            </div>
            <div class="record-amount" :class="{ 'income': record.amount > 0 }">
              {{ record.amount > 0 ? '+' : '' }}{{ record.amount.toFixed(2) }}
            </div>
          </div>
        </div>
      </div>
  
      <!-- 发票管理 -->
      <div class="section">
        <h3 class="section-title">发票开具</h3>
        <button class="invoice-btn" @click="showInvoiceDialog = true">申请开票</button>
        <div class="invoice-list">
          <div v-for="invoice in invoices" :key="invoice.id" class="invoice-item">
            <div class="invoice-info">
              <span class="invoice-title">发票编号：{{ invoice.id }}</span>
              <span class="invoice-time">{{ formatDate(invoice.time) }}</span>
            </div>
            <div class="invoice-status" :class="invoice.status">
              {{ invoice.status === 'completed' ? '已开具' : '处理中' }}
            </div>
          </div>
        </div>
      </div>
  
      <!-- 充值对话框 -->
      <div v-if="showRechargeDialog" class="dialog-mask">
        <div class="recharge-dialog">
          <h3>账户充值</h3>
          <div class="amount-options">
            <button 
              v-for="amount in presetAmounts" 
              :key="amount"
              :class="{ 'selected': rechargeAmount === amount }"
              @click="rechargeAmount = amount"
            >
              ¥{{ amount }}
            </button>
          </div>
          <div class="custom-amount">
            <label>自定义金额：</label>
            <input 
              type="number" 
              v-model="rechargeAmount" 
              placeholder="请输入充值金额"
              min="1"
              step="0.01"
            >
          </div>
          <div class="payment-methods">
            <h4>选择支付方式</h4>
            <div class="method-option">
              <input 
                type="radio" 
                id="alipay" 
                value="alipay" 
                v-model="paymentMethod"
              >
              <label for="alipay">支付宝</label>
            </div>
            <div class="method-option">
              <input 
                type="radio" 
                id="wechat" 
                value="wechat" 
                v-model="paymentMethod"
              >
              <label for="wechat">微信支付</label>
            </div>
          </div>
          <div class="dialog-footer">
            <button class="cancel-btn" @click="showRechargeDialog = false">取消</button>
            <button class="confirm-btn" @click="handleRecharge">立即支付</button>
          </div>
        </div>
      </div>
  
      <!-- 发票对话框 -->
      <div v-if="showInvoiceDialog" class="dialog-mask">
        <div class="invoice-dialog">
          <h3>申请发票</h3>
          <div class="form-group">
            <label>发票类型</label>
            <select v-model="invoiceForm.type">
              <option value="personal">个人发票</option>
              <option value="company">企业发票</option>
            </select>
          </div>
          <div class="form-group" v-if="invoiceForm.type === 'company'">
            <label>企业名称</label>
            <input 
              type="text" 
              v-model="invoiceForm.company" 
              placeholder="请输入企业名称"
            >
          </div>
          <div class="form-group">
            <label>发票金额</label>
            <input 
              type="number" 
              v-model="invoiceForm.amount" 
              placeholder="请输入开票金额"
              min="1"
              :max="balance"
            >
          </div>
          <div class="form-group">
            <label>邮箱地址</label>
            <input 
              type="email" 
              v-model="invoiceForm.email" 
              placeholder="接收电子发票的邮箱"
            >
          </div>
          <div class="dialog-footer">
            <button class="cancel-btn" @click="showInvoiceDialog = false">取消</button>
            <button class="confirm-btn" @click="handleInvoice">提交申请</button>
          </div>
        </div>
      </div>
  
      <!-- 支付模拟弹窗 -->
      <div v-if="showPaymentPopup" class="payment-popup">
        <div class="payment-content">
          <h3>模拟支付</h3>
          <p>正在使用 {{ paymentMethod === 'alipay' ? '支付宝' : '微信支付' }} 支付 ¥{{ rechargeAmount }}</p>
          <div class="qr-code">
            <div class="code-placeholder"></div>
            <p>请扫描二维码完成支付</p>
          </div>
          <div class="payment-buttons">
            <button class="cancel-btn" @click="showPaymentPopup = false">取消支付</button>
            <button class="confirm-btn" @click="completePayment">支付成功</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  
  // 账户数据
  const balance = ref(1250.50)
  const rechargeRecords = ref([
    { id: 1, type: '账户充值', amount: 500, time: '2023-07-10T14:30:00' },
    { id: 2, type: '广告消费', amount: -120, time: '2023-07-08T09:15:00' },
    { id: 3, type: '账户充值', amount: 1000, time: '2023-07-01T16:45:00' }
  ])
  
  const invoices = ref([
    { id: 'INV20230710001', amount: 500, time: '2023-07-10T15:30:00', status: 'completed' },
    { id: 'INV20230705001', amount: 320, time: '2023-07-05T11:20:00', status: 'completed' },
    { id: 'INV20230715001', amount: 1000, time: '2023-07-15T10:00:00', status: 'processing' }
  ])
  
  // 充值相关
  const showRechargeDialog = ref(false)
  const presetAmounts = [100, 500, 1000, 2000, 5000]
  const rechargeAmount = ref(100)
  const paymentMethod = ref('alipay')
  const showPaymentPopup = ref(false)
  
  // 发票相关
  const showInvoiceDialog = ref(false)
  const invoiceForm = ref({
    type: 'personal',
    company: '',
    amount: '',
    email: ''
  })
  
  // 格式化日期
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleString()
  }
  
  // 处理充值
  const handleRecharge = () => {
    showRechargeDialog.value = false
    showPaymentPopup.value = true
  }
  
  // 完成支付
  const completePayment = () => {
    const amount = parseFloat(rechargeAmount.value)
    if (isNaN(amount) || amount <= 0) {
      alert('请输入有效的充值金额')
      return
    }
  
    balance.value += amount
    rechargeRecords.value.unshift({
      id: Date.now(),
      type: '账户充值',
      amount: amount,
      time: new Date().toISOString()
    })
    
    showPaymentPopup.value = false
    alert(`充值成功！¥${amount.toFixed(2)} 已到账`)
  }
  
  // 处理发票申请
  const handleInvoice = () => {
    const amount = parseFloat(invoiceForm.value.amount)
    if (isNaN(amount) || amount <= 0) {
      alert('请输入有效的开票金额')
      return
    }
  
    if (amount > balance.value) {
      alert('开票金额不能大于账户余额')
      return
    }
  
    if (invoiceForm.value.type === 'company' && !invoiceForm.value.company) {
      alert('请输入企业名称')
      return
    }
  
    if (!invoiceForm.value.email) {
      alert('请输入接收发票的邮箱地址')
      return
    }
  
    const newInvoice = {
      id: `INV${new Date().getTime()}`,
      amount: amount,
      time: new Date().toISOString(),
      status: 'processing'
    }
  
    invoices.value.unshift(newInvoice)
    showInvoiceDialog.value = false
    alert('发票申请已提交，我们将在1-3个工作日内处理')
  }
  </script>
  
  <style scoped>
  .account-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .account-title {
    text-align: center;
    margin-bottom: 30px;
    color: #333;
  }
  
  .balance-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 30px;
  }
  
  .balance-info {
    display: flex;
    flex-direction: column;
  }
  
  .balance-label {
    font-size: 14px;
    color: #666;
    margin-bottom: 5px;
  }
  
  .balance-amount {
    font-size: 28px;
    font-weight: bold;
    color: #333;
  }
  
  .recharge-btn {
    padding: 10px 20px;
    background: #409eff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
  }
  
  .recharge-btn:hover {
    background: #66b1ff;
  }
  
  .section {
    background: #fff;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 30px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }
  
  .section-title {
    margin-top: 0;
    margin-bottom: 20px;
    color: #333;
    font-size: 18px;
  }
  
  .record-list, .invoice-list {
    border-top: 1px solid #eee;
  }
  
  .record-item, .invoice-item {
    display: flex;
    justify-content: space-between;
    padding: 15px 0;
    border-bottom: 1px solid #eee;
  }
  
  .record-detail {
    display: flex;
    flex-direction: column;
  }
  
  .record-type {
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .record-time, .invoice-time {
    font-size: 12px;
    color: #999;
  }
  
  .record-amount {
    font-weight: bold;
  }
  
  .record-amount.income {
    color: #67c23a;
  }
  
  .invoice-info {
    display: flex;
    flex-direction: column;
  }
  
  .invoice-title {
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .invoice-status {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
  }
  
  .invoice-status.completed {
    background: #f0f9eb;
    color: #67c23a;
  }
  
  .invoice-status.processing {
    background: #fdf6ec;
    color: #e6a23c;
  }
  
  .invoice-btn {
    padding: 8px 16px;
    background: #409eff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-bottom: 15px;
  }
  
  .dialog-mask {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  
  .recharge-dialog, .invoice-dialog {
    background: white;
    border-radius: 8px;
    padding: 20px;
    width: 500px;
    max-width: 90%;
  }
  
  .amount-options {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 20px;
  }
  
  .amount-options button {
    padding: 10px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    background: white;
    cursor: pointer;
  }
  
  .amount-options button.selected {
    border-color: #409eff;
    background: #ecf5ff;
    color: #409eff;
  }
  
  .custom-amount {
    margin-bottom: 20px;
  }
  
  .custom-amount label {
    display: block;
    margin-bottom: 8px;
    color: #606266;
  }
  
  .custom-amount input {
    width: 100%;
    padding: 10px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
  }
  
  .payment-methods {
    margin-bottom: 20px;
  }
  
  .payment-methods h4 {
    margin-top: 0;
    margin-bottom: 15px;
  }
  
  .method-option {
    margin-bottom: 10px;
  }
  
  .method-option input {
    margin-right: 8px;
  }
  
  .dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
  }
  
  .cancel-btn, .confirm-btn {
    padding: 8px 15px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .cancel-btn {
    background: white;
    border: 1px solid #dcdfe6;
  }
  
  .confirm-btn {
    background: #409eff;
    color: white;
    border: none;
  }
  
  .payment-popup {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
  }
  
  .payment-content {
    background: white;
    padding: 30px;
    border-radius: 8px;
    text-align: center;
    width: 400px;
    max-width: 90%;
  }
  
  .qr-code {
    margin: 20px 0;
  }
  
  .code-placeholder {
    width: 200px;
    height: 200px;
    margin: 0 auto;
    background: #f5f5f5;
    border: 1px dashed #ccc;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #999;
  }
  
  .payment-buttons {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 20px;
  }
  
  /* 响应式设计 */
  @media (max-width: 768px) {
    .amount-options {
      grid-template-columns: repeat(2, 1fr);
    }
    
    .balance-card {
      flex-direction: column;
      align-items: flex-start;
    }
    
    .recharge-btn {
      width: 100%;
      margin-top: 15px;
    }
  }
  .breadcrumb {
  margin-bottom: 15px;
  font-size: 14px;
  color: #606266;
  padding: 10px 0;
}

.breadcrumb a {
  color: #409eff;
  text-decoration: none;
  transition: color 0.3s;
}

.breadcrumb a:hover {
  color: #66b1ff;
  text-decoration: underline;
}

.separator {
  margin: 0 8px;
  color: #c0c4cc;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .breadcrumb {
    display: none;
  }
  
  .account-title {
    margin-top: 10px;
  }
}
</style>
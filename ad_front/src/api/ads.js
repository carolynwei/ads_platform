import service from './index'  // 你定义的axios实例

export default {
  // 获取广告列表（对应 GET /ads/）
  getAdsList(params) {
    return service.get('/ads/', { params })
  },

  // 创建广告（对应 POST /ads/）
  createAd(data) {
    return service.post('/ads/', data)
  },

  // 获取单个广告详情（对应 GET /ads/:id/）
  getAdDetail(id) {
    return service.get(`/ads/${id}/`)
  },

  // 更新广告（对应 PUT /ads/:id/）
  updateAd(id, data) {
    return service.put(`/ads/${id}/`, data)
  },

  // 删除广告（对应 DELETE /ads/:id/）
  deleteAd(id) {
    return service.delete(`/ads/${id}/`)
  },

  // 获取充值记录（对应 GET /recharge/）
  getRechargeRecords(params) {
    return service.get('/recharge/', { params })
  },

  // 创建充值记录（对应 POST /recharge/）
  createRechargeRecord(data) {
    return service.post('/recharge/', data)
  },

  // 自定义的充值历史列表接口（GET /recharge-history/）
  getRechargeHistory(params) {
    return service.get('/recharge-history/', { params })
  },

  // 导出充值历史（GET /recharge-history/export/），通常返回文件流
  exportRechargeHistory(params) {
    return service.get('/recharge-history/export/', { 
      params, 
      responseType: 'blob'  // 如果是文件下载，需加这个
    })
  },

  // 获取发票列表（GET /invoices/）
  getInvoices(params) {
    return service.get('/invoices/', { params })
  },

  // 创建发票（POST /invoices/）
  createInvoice(data) {
    return service.post('/invoices/', data)
  },

  // 获取单个发票详情（GET /invoices/:id/）
  getInvoiceDetail(id) {
    return service.get(`/invoices/${id}/`)
  },

  // 更新发票（PUT /invoices/:id/）
  updateInvoice(id, data) {
    return service.put(`/invoices/${id}/`, data)
  },

  // 删除发票（DELETE /invoices/:id/）
  deleteInvoice(id) {
    return service.delete(`/invoices/${id}/`)
  }
}

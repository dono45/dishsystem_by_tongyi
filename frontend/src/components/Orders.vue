<template>
  <div class="orders">
    <h2>我的订单</h2>
    
    <div v-if="orders.length === 0">
      <p>暂无订单</p>
      <router-link to="/" class="btn btn-primary">去点餐</router-link>
    </div>
    
    <div v-else>
      <div class="card mb-3" v-for="order in orders" :key="order.id">
        <div class="card-header">
          <div class="d-flex justify-content-between">
            <span>订单号: {{ order.id }}</span>
            <span class="badge bg-primary">{{ order.status }}</span>
          </div>
        </div>
        <div class="card-body">
          <div v-for="item in order.items" :key="item.dish.id" class="mb-2">
            <div class="d-flex justify-content-between">
              <span>{{ item.dish.name }} ({{ item.specifications }}) x {{ item.quantity }}</span>
              <span>¥{{ (item.price * item.quantity).toFixed(2) }}</span>
            </div>
          </div>
          <hr>
          <div class="d-flex justify-content-between">
            <strong>总计:</strong>
            <strong>¥{{ order.total_amount.toFixed(2) }}</strong>
          </div>
          <div class="text-muted">
            <small>下单时间: {{ formatDate(order.created_at) }}</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Orders',
  data() {
    return {
      orders: []
    }
  },
  
  async mounted() {
    this.checkAuthAndLoad()
  },
  
  methods: {
    checkAuthAndLoad() {
      if (!localStorage.getItem('token')) {
        this.$root.showMessage('请先登录')
        this.$router.push('/login')
        return
      }
      
      this.loadOrders()
    },
    
    async loadOrders() {
      try {
        const response = await axios.get('/api/orders', {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        })
        this.orders = response.data
      } catch (error) {
        if (error.response && error.response.status === 401) {
          // Token无效或过期，清除本地存储并跳转到登录页
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          this.$root.showMessage('登录已过期，请重新登录')
          this.$router.push('/login')
        } else {
          this.$root.showMessage('加载订单失败：' + (error.response?.data?.message || '未知错误'))
        }
      }
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN')
    }
  }
}
</script>
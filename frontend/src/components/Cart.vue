<template>
  <div class="cart">
    <h2>购物车</h2>
    
    <div v-if="cartItems.length === 0">
      <p>购物车为空</p>
      <router-link to="/" class="btn btn-primary">去点餐</router-link>
    </div>
    
    <div v-else>
      <div class="card mb-3" v-for="item in cartItems" :key="item.id">
        <div class="card-body">
          <div class="d-flex justify-content-between">
            <div>
              <h5 class="card-title">{{ item.dish.name }}</h5>
              <p class="card-text">
                <small class="text-muted">{{ item.specifications }}</small>
              </p>
              <p class="card-text">单价: ¥{{ item.dish.price.toFixed(2) }}</p>
            </div>
            
            <div class="d-flex align-items-center">
              <div class="input-group" style="width: 150px;">
                <button 
                  class="btn btn-outline-secondary" 
                  type="button"
                  @click="updateQuantity(item.id, item.quantity - 1)"
                  style="background-color: #f8f9fa;"
                >
                  -
                </button>
                <input 
                  type="number" 
                  class="form-control text-center" 
                  :value="item.quantity"
                  @change="updateQuantity(item.id, $event.target.value)"
                  min="1"
                >
                <button 
                  class="btn btn-outline-secondary" 
                  type="button"
                  @click="updateQuantity(item.id, item.quantity + 1)"
                  style="background-color: #f8f9fa;"
                >
                  +
                </button>
              </div>
              
              <div class="ms-3">
                <strong>¥{{ (item.dish.price * item.quantity).toFixed(2) }}</strong>
              </div>
              
              <button 
                class="btn btn-danger ms-3" 
                @click="removeItem(item.id)"
              >
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="d-flex justify-content-end">
        <h4>总计: ¥{{ totalAmount.toFixed(2) }}</h4>
      </div>
      
      <div class="d-grid gap-2 d-md-flex justify-content-md-end mt-3">
        <button class="btn btn-success" @click="checkout">结算</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Cart',
  data() {
    return {
      cartItems: []
    }
  },
  
  computed: {
    totalAmount() {
      return this.cartItems.reduce((total, item) => {
        return total + (item.dish.price * item.quantity)
      }, 0)
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
      
      this.loadCart()
    },
    
    async loadCart() {
      try {
        const response = await axios.get('/api/cart', {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        })
        this.cartItems = response.data
      } catch (error) {
        if (error.response && error.response.status === 401) {
          // Token无效或过期，清除本地存储并跳转到登录页
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          this.$root.showMessage('登录已过期，请重新登录')
          this.$router.push('/login')
        } else {
          this.$root.showMessage('加载购物车失败：' + (error.response?.data?.message || '未知错误'))
        }
      }
    },
    
    async updateQuantity(itemId, quantity) {
      if (quantity <= 0) {
        this.removeItem(itemId)
        return
      }
      
      try {
        await axios.put(`/api/cart/${itemId}`, {
          quantity: parseInt(quantity)
        }, {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        })
        
        // 更新本地数据
        const item = this.cartItems.find(item => item.id === itemId)
        if (item) {
          item.quantity = parseInt(quantity)
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          // Token无效或过期，清除本地存储并跳转到登录页
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          this.$root.showMessage('登录已过期，请重新登录')
          this.$router.push('/login')
        } else {
          this.$root.showMessage('更新数量失败：' + (error.response?.data?.message || '未知错误'))
        }
      }
    },
    
    async removeItem(itemId) {
      try {
        await axios.delete(`/api/cart/${itemId}`, {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        })
        
        // 更新本地数据
        this.cartItems = this.cartItems.filter(item => item.id !== itemId)
      } catch (error) {
        if (error.response && error.response.status === 401) {
          // Token无效或过期，清除本地存储并跳转到登录页
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          this.$root.showMessage('登录已过期，请重新登录')
          this.$router.push('/login')
        } else {
          this.$root.showMessage('删除商品失败：' + (error.response?.data?.message || '未知错误'))
        }
      }
    },
    
    async checkout() {
      try {
        const response = await axios.post('/api/orders', {}, {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        })
        
        this.$root.showMessage('订单创建成功')
        this.$router.push('/orders')
      } catch (error) {
        if (error.response && error.response.status === 401) {
          // Token无效或过期，清除本地存储并跳转到登录页
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          this.$root.showMessage('登录已过期，请重新登录')
          this.$router.push('/login')
        } else {
          this.$root.showMessage('创建订单失败：' + (error.response?.data?.message || '未知错误'))
        }
      }
    }
  }
}
</script>

<style scoped>
.btn-outline-secondary {
  cursor: pointer;
}
</style>
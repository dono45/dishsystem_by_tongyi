<template>
  <div class="home">
    <h2>今日菜单</h2>
    <div v-if="loading">加载中...</div>
    <div v-else class="dishes-grid">
      <div 
        v-for="dish in dishes" 
        :key="dish.id" 
        class="dish-card card"
      >
        <img :src="dish.image_url" :alt="dish.name" />
        <h3>{{ dish.name }}</h3>
        <p>{{ dish.description }}</p>
        <div class="dish-price">¥{{ dish.price }}</div>
        <div class="card-actions">
          <button @click="addToCart(dish)">加入购物车</button>
          <button @click="viewDetails(dish.id)">查看详情</button>
        </div>
      </div>
    </div>
    
    <!-- 购物车 -->
    <div class="cart" v-if="cart.length > 0">
      <h3>购物车</h3>
      <div class="cart-items">
        <div v-for="(item, index) in cart" :key="index" class="cart-item">
          <span>{{ item.name }} x {{ item.quantity }}</span>
          <span>¥{{ item.price * item.quantity }}</span>
          <button @click="removeFromCart(index)">删除</button>
        </div>
      </div>
      <div class="cart-total">
        总计: ¥{{ cartTotal }}
      </div>
      <button @click="checkout" class="checkout-button">结算</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Home',
  data() {
    return {
      dishes: [],
      loading: true,
      cart: []
    }
  },
  computed: {
    cartTotal() {
      return this.cart.reduce((total, item) => total + (item.price * item.quantity), 0).toFixed(2)
    }
  },
  async mounted() {
    try {
      const response = await axios.get('/api/dishes')
      this.dishes = response.data
      this.loading = false
    } catch (error) {
      console.error('获取菜品失败:', error)
      this.loading = false
    }
  },
  methods: {
    addToCart(dish) {
      const existingItem = this.cart.find(item => item.id === dish.id)
      if (existingItem) {
        existingItem.quantity++
      } else {
        this.cart.push({
          id: dish.id,
          name: dish.name,
          price: dish.price,
          quantity: 1
        })
      }
      alert(`${dish.name} 已加入购物车`)
    },
    removeFromCart(index) {
      this.cart.splice(index, 1)
    },
    viewDetails(dishId) {
      this.$router.push(`/dish/${dishId}`)
    },
    async checkout() {
      try {
        const response = await axios.post('/api/order', {
          items: this.cart
        })
        alert(`订单创建成功! 订单号: ${response.data.order_id}`)
        this.cart = [] // 清空购物车
      } catch (error) {
        console.error('下单失败:', error)
        alert('下单失败，请重试')
      }
    }
  }
}
</script>

<style scoped>
.dishes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.dish-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
}

.dish-card h3 {
  margin: 0.5rem 0;
}

.dish-card p {
  color: #666;
  min-height: 3rem;
}

.dish-price {
  font-size: 1.2rem;
  font-weight: bold;
  color: #e74c3c;
  margin: 0.5rem 0;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.cart {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  width: 300px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.cart-items {
  max-height: 200px;
  overflow-y: auto;
}

.cart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.cart-total {
  font-weight: bold;
  margin: 1rem 0;
  font-size: 1.2rem;
}

.checkout-button {
  width: 100%;
  padding: 0.8rem;
  font-size: 1.1rem;
}
</style>
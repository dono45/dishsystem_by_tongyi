<template>
  <div class="dish-detail">
    <div v-if="loading">加载中...</div>
    <div v-else>
      <button @click="$router.go(-1)" class="back-button">返回</button>
      
      <div class="dish-header">
        <img :src="dish.image_url" :alt="dish.name" />
        <div class="dish-info">
          <h2>{{ dish.name }}</h2>
          <p>{{ dish.description }}</p>
          <div class="dish-price">¥{{ dish.price }}</div>
          <button @click="addToCart" class="add-to-cart-button">加入购物车</button>
        </div>
      </div>
      
      <div class="reviews-section">
        <h3>评价</h3>
        <div class="average-rating">
          平均评分: 
          <span class="stars">{{ renderStars(dish.average_rating) }}</span>
          ({{ dish.average_rating.toFixed(1) }} 星)
        </div>
        
        <div class="reviews-list">
          <div v-for="review in dish.reviews" :key="review.id" class="review card">
            <div class="review-header">
              <span class="stars">{{ renderStars(review.rating) }}</span>
              <span class="review-date">{{ formatDate(review.created_at) }}</span>
            </div>
            <p class="review-comment">{{ review.comment }}</p>
          </div>
        </div>
        
        <div class="add-review">
          <h4>添加评价</h4>
          <div class="rating-input">
            <label>评分:</label>
            <div class="stars">
              <span 
                v-for="star in 5" 
                :key="star"
                :class="{ active: star <= rating }"
                @click="setRating(star)"
              >★</span>
            </div>
          </div>
          <textarea 
            v-model="comment" 
            placeholder="请输入您的评价..." 
            rows="4"
          ></textarea>
          <button @click="submitReview">提交评价</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'DishDetail',
  props: ['id'],
  data() {
    return {
      dish: null,
      loading: true,
      rating: 5,
      comment: ''
    }
  },
  async mounted() {
    await this.fetchDish()
  },
  methods: {
    async fetchDish() {
      try {
        const response = await axios.get(`/api/dishes/${this.id}`)
        this.dish = response.data
        this.loading = false
      } catch (error) {
        console.error('获取菜品详情失败:', error)
        this.loading = false
      }
    },
    renderStars(rating) {
      const fullStars = Math.floor(rating)
      const halfStar = rating % 1 >= 0.5
      let stars = '★'.repeat(fullStars)
      if (halfStar) stars += '☆'
      stars += '★'.repeat(5 - fullStars - (halfStar ? 1 : 0)).replace(/★/g, '☆')
      return stars
    },
    setRating(rating) {
      this.rating = rating
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN')
    },
    addToCart() {
      // 在实际应用中，这里应该与 Vuex 或其他状态管理通信
      alert(`${this.dish.name} 已加入购物车`)
    },
    async submitReview() {
      if (this.rating < 1 || this.rating > 5) {
        alert('请选择有效的评分 (1-5星)')
        return
      }
      
      try {
        await axios.post(`/api/dishes/${this.id}/reviews`, {
          rating: this.rating,
          comment: this.comment
        })
        
        alert('评价提交成功!')
        this.comment = ''
        this.rating = 5
        
        // 重新获取菜品信息以更新评论列表
        await this.fetchDish()
      } catch (error) {
        console.error('提交评价失败:', error)
        alert('提交评价失败，请重试')
      }
    }
  }
}
</script>

<style scoped>
.dish-detail {
  max-width: 800px;
  margin: 0 auto;
}

.back-button {
  background-color: #95a5a6;
  margin-bottom: 1rem;
}

.dish-header {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
}

.dish-header img {
  width: 300px;
  height: 300px;
  object-fit: cover;
  border-radius: 8px;
}

.dish-info h2 {
  margin-top: 0;
}

.dish-price {
  font-size: 1.8rem;
  font-weight: bold;
  color: #e74c3c;
}

.add-to-cart-button {
  padding: 0.8rem 1.5rem;
  font-size: 1.1rem;
}

.average-rating {
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.reviews-list {
  margin: 2rem 0;
}

.review {
  text-align: left;
  margin-bottom: 1rem;
}

.review-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.review-date {
  color: #7f8c8d;
}

.review-comment {
  margin: 0;
}

.add-review {
  border-top: 1px solid #eee;
  padding-top: 1rem;
}

.rating-input {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.rating-input .stars {
  font-size: 1.5rem;
  cursor: pointer;
}

.rating-input .stars span {
  color: #ddd;
}

.rating-input .stars span.active {
  color: #ffc107;
}

textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-family: inherit;
}

@media (max-width: 768px) {
  .dish-header {
    flex-direction: column;
  }
  
  .dish-header img {
    width: 100%;
    height: auto;
  }
}
</style>
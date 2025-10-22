<template>
  <div class="review-page">
    <div class="container mt-4">
      <div class="row">
        <div class="col-md-8">
          <h2>{{ dish?.name }} - 评论</h2>
          
          <!-- 显示菜品信息 -->
          <div class="card mb-4" v-if="dish">
            <div class="row g-0">
              <div class="col-md-4">
                <img :src="dish.image_url || 'https://via.placeholder.com/300x200?text=No+Image'" 
                     class="img-fluid rounded-start" 
                     :alt="dish.name"
                     style="height: 200px; object-fit: cover;">
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <h5 class="card-title">{{ dish.name }}</h5>
                  <p class="card-text">{{ dish.description }}</p>
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <!-- 星星评分 -->
                      <div class="mb-2">
                        <span v-for="n in 5" :key="n" class="star">
                          <span :class="n <= Math.floor(dish.averageRating) ? 'text-warning' : 'text-muted'">
                            ★
                          </span>
                        </span>
                        <span class="ms-1">{{ dish.averageRating }}分 ({{ dish.reviewCount }}条评论)</span>
                      </div>
                    </div>
                    <p class="card-text">
                      <strong>¥{{ dish.price.toFixed(2) }}</strong>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 发表评论表单 (仅限登录用户) -->
          <div class="card mb-4" v-if="isLoggedIn">
            <div class="card-header">
              <h5>发表评论</h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="submitReview">
                <div class="mb-3">
                  <label class="form-label">评分</label>
                  <div>
                    <span v-for="n in 5" :key="n" 
                          class="star fs-3" 
                          :class="n <= rating ? 'text-warning' : 'text-muted'"
                          @click="rating = n"
                          style="cursor: pointer;">
                      ★
                    </span>
                  </div>
                </div>
                <div class="mb-3">
                  <label for="reviewComment" class="form-label">评论内容</label>
                  <textarea class="form-control" id="reviewComment" rows="3" v-model="comment"></textarea>
                </div>
                <button type="submit" class="btn btn-primary">提交评论</button>
              </form>
            </div>
          </div>
          
          <!-- 评论列表 -->
          <div class="card">
            <div class="card-header">
              <h5>用户评论</h5>
            </div>
            <div class="card-body">
              <div v-if="reviews.length === 0">
                <p class="text-muted">暂无评论，快来发表第一条评论吧！</p>
              </div>
              <div v-else>
                <div class="review-item mb-4 pb-3 border-bottom" v-for="review in reviews" :key="review.id">
                  <div class="d-flex justify-content-between">
                    <h6>{{ review.user.username }}</h6>
                    <small class="text-muted">{{ formatDate(review.created_at) }}</small>
                  </div>
                  <div class="mb-2">
                    <span v-for="n in 5" :key="n" class="star">
                      <span :class="n <= review.rating ? 'text-warning' : 'text-muted'">
                        ★
                      </span>
                    </span>
                  </div>
                  <p>{{ review.comment }}</p>
                </div>
                
                <!-- 分页功能 -->
                <nav aria-label="评论分页">
                  <ul class="pagination justify-content-center">
                    <li class="page-item" :class="{ disabled: currentPage === 1 }">
                      <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">上一页</a>
                    </li>
                    <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: page === currentPage }">
                      <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
                    </li>
                    <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                      <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">下一页</a>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-4">
          <!-- 返回首页按钮 -->
          <div class="d-grid gap-2 mb-4">
            <router-link to="/" class="btn btn-secondary">返回首页</router-link>
          </div>
          
          <!-- 购物车按钮 -->
          <div class="card" v-if="isLoggedIn">
            <div class="card-header">
              <h5>操作</h5>
            </div>
            <div class="card-body">
              <div class="d-grid gap-2">
                <button class="btn btn-primary" @click="addToCart">加入购物车</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 规格选择模态框 -->
    <div class="modal fade" id="specModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">选择规格 - {{ dish?.name }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="dish">
            <div class="mb-3">
              <label class="form-label">份量</label>
              <div>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" id="sizeSmall" value="小份" v-model="specifications.size">
                  <label class="form-check-label" for="sizeSmall">小份</label>
                </div>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" id="sizeMedium" value="中份" v-model="specifications.size" checked>
                  <label class="form-check-label" for="sizeMedium">中份</label>
                </div>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" id="sizeLarge" value="大份" v-model="specifications.size">
                  <label class="form-check-label" for="sizeLarge">大份</label>
                </div>
              </div>
            </div>
            
            <div class="mb-3">
              <label class="form-label">辣度</label>
              <div>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" id="spicyNone" value="不辣" v-model="specifications.spicy" checked>
                  <label class="form-check-label" for="spicyNone">不辣</label>
                </div>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" id="spicyMild" value="微辣" v-model="specifications.spicy">
                  <label class="form-check-label" for="spicyMild">微辣</label>
                </div>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" id="spicyHot" value="特辣" v-model="specifications.spicy">
                  <label class="form-check-label" for="spicyHot">特辣</label>
                </div>
              </div>
            </div>
            
            <div class="mb-3">
              <label class="form-label">甜度</label>
              <div>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" id="sweetNone" value="无糖" v-model="specifications.sweetness" checked>
                  <label class="form-check-label" for="sweetNone">无糖</label>
                </div>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" id="sweetLittle" value="少糖" v-model="specifications.sweetness">
                  <label class="form-check-label" for="sweetLittle">少糖</label>
                </div>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" id="sweetNormal" value="正常" v-model="specifications.sweetness">
                  <label class="form-check-label" for="sweetNormal">正常</label>
                </div>
              </div>
            </div>
            
            <div class="mb-3">
              <label class="form-label">数量</label>
              <div class="input-group">
                <button class="btn btn-outline-secondary" type="button" @click="decreaseQuantity">-</button>
                <input type="number" class="form-control text-center" v-model="quantity" min="1">
                <button class="btn btn-outline-secondary" type="button" @click="increaseQuantity">+</button>
              </div>
              <div class="mt-2">
                <strong>总价: ¥{{ (dish.price * quantity).toFixed(2) }}</strong>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
            <button type="button" class="btn btn-primary" @click="confirmAddToCart">加入购物车</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Review',
  data() {
    return {
      dishId: this.$route.params.dishId,
      dish: null,
      reviews: [],
      rating: 5,
      comment: '',
      isLoggedIn: !!localStorage.getItem('token'),
      currentPage: 1,
      totalPages: 1,
      pageSize: 5,
      specifications: {
        size: '中份',
        spicy: '不辣',
        sweetness: '无糖'
      },
      quantity: 1
    }
  },
  
  async mounted() {
    await this.loadDish()
    await this.loadReviews()
  },
  
  methods: {
    async loadDish() {
      try {
        const response = await axios.get(`/api/dishes/${this.dishId}`)
        this.dish = response.data
      } catch (error) {
        this.$root.showMessage('加载菜品信息失败')
      }
    },
    
    async loadReviews() {
      try {
        const response = await axios.get(`/api/dishes/${this.dishId}/reviews`)
        this.reviews = response.data
        
        // 计算分页信息
        this.totalPages = Math.ceil(this.reviews.length / this.pageSize)
        
        // 按创建时间倒序排列（最新评论在前）
        this.reviews.sort((a, b) => {
          return new Date(b.created_at) - new Date(a.created_at)
        })
      } catch (error) {
        this.$root.showMessage('加载评论失败')
      }
    },
    
    async submitReview() {
      if (!this.isLoggedIn) {
        this.$root.showMessage('请先登录')
        this.$router.push('/login')
        return
      }
      
      try {
        await axios.post(`/api/dishes/${this.dishId}/reviews`, {
          rating: this.rating,
          comment: this.comment
        }, {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        })
        
        this.$root.showMessage('评论发表成功')
        this.rating = 5
        this.comment = ''
        
        // 重新加载评论
        await this.loadReviews()
      } catch (error) {
        this.$root.showMessage('发表评论失败：' + (error.response?.data?.message || '未知错误'))
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN')
    },
    
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    },
    
    addToCart() {
      if (!this.isLoggedIn) {
        this.$root.showMessage('请先登录')
        this.$router.push('/login')
        return
      }
      
      this.specifications = {
        size: '中份',
        spicy: '不辣',
        sweetness: '无糖'
      }
      this.quantity = 1
      
      // 显示模态框
      import('bootstrap/dist/js/bootstrap.esm.js').then((bootstrap) => {
        const modal = new bootstrap.Modal(document.getElementById('specModal'))
        modal.show()
      }).catch((error) => {
        console.error('Failed to load Bootstrap:', error)
      })
    },
    
    increaseQuantity() {
      this.quantity++
    },
    
    decreaseQuantity() {
      if (this.quantity > 1) {
        this.quantity--
      }
    },
    
    async confirmAddToCart() {
      // 关闭模态框
      import('bootstrap/dist/js/bootstrap.esm.js').then((bootstrap) => {
        const modalEl = document.getElementById('specModal')
        const modal = bootstrap.Modal.getInstance(modalEl)
        if (modal) {
          modal.hide()
        }
      }).catch((error) => {
        console.error('Failed to load Bootstrap:', error)
        // 如果无法加载Bootstrap，手动隐藏模态框
        const modalEl = document.getElementById('specModal')
        if (modalEl) {
          modalEl.style.display = 'none'
          document.body.classList.remove('modal-open')
        }
      })
      
      try {
        // 将规格转换为字符串
        const specString = `${this.specifications.size},${this.specifications.spicy},${this.specifications.sweetness}`
        
        await axios.post('/api/cart', {
          dish_id: this.dish.id,
          quantity: this.quantity,
          specifications: specString
        }, {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        })
        
        this.$root.showMessage('已添加到购物车')
      } catch (error) {
        this.$root.showMessage('添加到购物车失败：' + (error.response?.data?.message || '未知错误'))
      }
    }
  }
}
</script>

<style scoped>
.star {
  font-size: 1.2em;
  cursor: pointer;
}

.review-item {
  text-align: left;
}
</style>
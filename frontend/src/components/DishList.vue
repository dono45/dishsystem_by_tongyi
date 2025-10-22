<template>
  <div class="dish-list">
    <h2>菜品列表</h2>
    
    <!-- 菜品搜索和排序 -->
    <div class="row mb-3">
      <div class="col-md-6">
        <input 
          type="text" 
          class="form-control" 
          placeholder="搜索菜品..." 
          v-model="searchTerm"
        >
      </div>
      <div class="col-md-6">
        <select class="form-select" v-model="sortBy">
          <option value="">默认排序</option>
          <option value="price_asc">价格升序</option>
          <option value="price_desc">价格降序</option>
          <option value="name_asc">名称升序</option>
          <option value="rating_desc">评分降序</option>
        </select>
      </div>
    </div>
    
    <!-- 菜品展示 -->
    <div class="row">
      <div class="col-md-4 mb-4" v-for="dish in filteredDishes" :key="dish.id">
        <div class="card">
          <img :src="dish.image_url || 'https://via.placeholder.com/300x200?text=No+Image'" 
               class="card-img-top" 
               :alt="dish.name"
               style="height: 200px; object-fit: cover;">
          <div class="card-body">
            <h5 class="card-title">{{ dish.name }}</h5>
            <p class="card-text">{{ dish.description }}</p>
            <p class="card-text">
              <strong>¥{{ dish.price.toFixed(2) }}</strong>
            </p>
            <div class="d-grid gap-2">
              <button class="btn btn-primary" @click="addToCart(dish)">
                选择规格
              </button>
              <router-link :to="'/dishes/' + dish.id + '/reviews'" class="btn btn-outline-secondary">
                查看评论
              </router-link>
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
            <h5 class="modal-title">选择规格 - {{ selectedDish?.name }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="selectedDish">
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
  name: 'DishList',
  data() {
    return {
      dishes: [],
      searchTerm: '',
      sortBy: '',
      selectedDish: null,
      specifications: {
        size: '中份',
        spicy: '不辣',
        sweetness: '无糖'
      },
      quantity: 1
    }
  },
  
  computed: {
    filteredDishes() {
      let result = this.dishes
      
      // 搜索过滤
      if (this.searchTerm) {
        result = result.filter(dish => 
          dish.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          dish.description.toLowerCase().includes(this.searchTerm.toLowerCase())
        )
      }
      
      // 排序
      switch (this.sortBy) {
        case 'price_asc':
          result.sort((a, b) => a.price - b.price)
          break
        case 'price_desc':
          result.sort((a, b) => b.price - a.price)
          break
        case 'name_asc':
          result.sort((a, b) => a.name.localeCompare(b.name))
          break
        // 评分排序需要额外处理
        default:
          // 默认顺序
          break
      }
      
      return result
    }
  },
  
  async mounted() {
    await this.loadDishes()
  },
  
  methods: {
    async loadDishes() {
      try {
        const response = await axios.get('/api/dishes')
        this.dishes = response.data
        
        // 如果没有从后端获取到数据，则使用模拟数据
        if (this.dishes.length === 0) {
          this.dishes = this.getMockDishes()
        }
      } catch (error) {
        // 如果请求失败，使用模拟数据
        this.dishes = this.getMockDishes()
        this.$root.showMessage('无法连接到服务器，显示模拟数据')
      }
    },
    
    getMockDishes() {
      return [
        {
          id: 1,
          name: '宫保鸡丁',
          description: '经典川菜，鸡肉丁与花生米炒制，酸甜微辣',
          price: 28.8,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/53/kung-pao-chicken-1768536_1280.jpg'
        },
        {
          id: 2,
          name: '麻婆豆腐',
          description: '嫩滑豆腐配以麻辣肉糜，口感丰富',
          price: 22.5,
          image_url: 'https://cdn.pixabay.com/photo/2017/08/18/17/16/mapo-tofu-2655484_1280.jpg'
        },
        {
          id: 3,
          name: '红烧肉',
          description: '精选五花肉，慢火炖煮，肥而不腻',
          price: 35.0,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/35/braised-pork-1768568_1280.jpg'
        },
        {
          id: 4,
          name: '鱼香肉丝',
          description: '猪肉丝配木耳胡萝卜，鱼香味浓',
          price: 26.8,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/36/yuxiang-shredded-pork-1768569_1280.jpg'
        },
        {
          id: 5,
          name: '糖醋里脊',
          description: '外酥内嫩的猪里脊，酸甜可口',
          price: 32.0,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/37/sweet-and-sour-pork-1768570_1280.jpg'
        },
        {
          id: 6,
          name: '水煮鱼',
          description: '鲜嫩鱼片配豆芽菜，麻辣鲜香',
          price: 45.0,
          image_url: 'https://cdn.pixabay.com/photo/2016/11/24/10/01/fish-1854444_1280.jpg'
        }
      ]
    },
    
    addToCart(dish) {
      this.selectedDish = dish
      this.specifications = {
        size: '中份',
        spicy: '不辣',
        sweetness: '无糖'
      }
      this.quantity = 1
      
      // 显示模态框
      const modal = new bootstrap.Modal(document.getElementById('specModal'))
      modal.show()
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
      const modalEl = document.getElementById('specModal')
      const modal = bootstrap.Modal.getInstance(modalEl)
      modal.hide()
      
      if (!localStorage.getItem('token')) {
        this.$root.showMessage('请先登录')
        this.$router.push('/login')
        return
      }
      
      try {
        // 将规格转换为字符串
        const specString = `${this.specifications.size},${this.specifications.spicy},${this.specifications.sweetness}`
        
        await axios.post('/api/cart', {
          dish_id: this.selectedDish.id,
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
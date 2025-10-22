<template>
  <div class="home-page">
    <!-- 页头 -->
    <header class="page-header bg-primary text-white py-5">
      <div class="container">
        <div class="row">
          <div class="col-lg-8">
            <h1 class="display-4 fw-bold">欢迎来到餐饮点餐系统</h1>
            <p class="lead">在这里您可以浏览我们的美味菜品，在线点餐并享受送餐服务。</p>
          </div>
        </div>
      </div>
    </header>
    
    <div class="container-fluid">
      <div class="row">
        <!-- 侧边栏 - 菜品分类筛选 -->
        <div class="col-lg-2 d-none d-lg-block">
          <div class="category-filter bg-light p-3 mt-4 rounded">
            <h5 class="border-bottom pb-2">菜品分类</h5>
            <div class="form-check mb-2">
              <input class="form-check-input" type="radio" name="category" id="allCategories" value="" v-model="selectedCategory" checked>
              <label class="form-check-label" for="allCategories">所有商品</label>
            </div>
            <div class="form-check mb-2" v-for="category in allCategories" :key="category.id">
              <input class="form-check-input" type="radio" name="category" :id="'cat_' + category.id" :value="category.name" v-model="selectedCategory">
              <label class="form-check-label" :for="'cat_' + category.id">{{ category.name }}</label>
            </div>
          </div>
        </div>
        
        <!-- 主内容区 -->
        <div class="col-lg-10">
          <div class="container">
            <!-- 筛选和排序区域 -->
            <div class="row mb-4 mt-4">
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
            
            <!-- 响应式分类筛选（仅在小屏幕上显示） -->
            <div class="row mb-3 d-lg-none">
              <div class="col-12">
                <select class="form-select" v-model="selectedCategory">
                  <option value="">所有商品</option>
                  <option v-for="category in allCategories" :key="category.id" :value="category.name">{{ category.name }}</option>
                </select>
              </div>
            </div>
            
            <!-- 菜品展示 -->
            <div class="row" id="menu-section">
              <div class="col-md-6 col-lg-4 mb-4" v-for="dish in paginatedDishes" :key="dish.id">
                <div class="card h-100 dish-card">
                  <img :src="dish.image_url || 'https://via.placeholder.com/300x200?text=No+Image'" 
                       class="card-img-top" 
                       :alt="dish.name"
                       style="height: 200px; object-fit: cover;">
                  <div class="card-body d-flex flex-column">
                    <h5 class="card-title">{{ dish.name }}</h5>
                    <p class="card-text">{{ dish.description }}</p>
                    
                    <!-- 星星评分 -->
                    <div class="mb-2">
                      <span v-for="n in 5" :key="n" class="star">
                        <span :class="n <= Math.floor(dish.rating) ? 'text-warning' : 'text-muted'">
                          ★
                        </span>
                      </span>
                      <span class="ms-1 text-muted">({{ dish.rating }}分)</span>
                    </div>
                    
                    <p class="card-text mt-auto">
                      <strong>¥{{ dish.price.toFixed(2) }}</strong>
                    </p>
                    <div class="d-grid gap-2">
                      <button class="btn btn-primary" @click="addToCart(dish)">
                        选择规格
                      </button>
                      <button class="btn btn-outline-secondary" @click="viewReviews(dish)">
                        查看评论 ({{ dish.reviewCount }})
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 分页控件 -->
            <div class="row mt-4">
              <div class="col-12">
                <nav aria-label="菜品分页">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <label for="pageSize" class="me-2">每页显示:</label>
                      <select id="pageSize" class="form-select d-inline-block w-auto" :value="pageSize" @change="onPageSizeChange">
                        <option value="5">5</option>
                        <option value="10">10</option>
                        <option value="20">20</option>
                        <option value="50">50</option>
                      </select>
                    </div>
                    
                    <ul class="pagination mb-0">
                      <li class="page-item" :class="{ disabled: currentPage === 1 }">
                        <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">上一页</a>
                      </li>
                      
                      <li class="page-item" v-for="page in visiblePages" :key="page" :class="{ active: page === currentPage }">
                        <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
                      </li>
                      
                      <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                        <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">下一页</a>
                      </li>
                    </ul>
                    
                    <div>
                      <span>第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
                    </div>
                  </div>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 页尾 -->
    <footer class="page-footer bg-dark text-white mt-5">
      <div class="container py-5">
        <div class="row">
          <div class="col-md-4 mb-4 mb-md-0">
            <h5>关于我们</h5>
            <p>我们致力于为您提供最新鲜、最美味的餐饮服务。拥有多年餐饮经验，严格把控食材质量，用心做好每一道菜。</p>
          </div>
          <div class="col-md-4 mb-4 mb-md-0">
            <h5>联系方式</h5>
            <p><i class="fas fa-phone"></i> 电话: 400-123-4567</p>
            <p><i class="fas fa-envelope"></i> 邮箱: info@fooddelivery.com</p>
            <p><i class="fas fa-map-marker-alt"></i> 地址: 北京市朝阳区美食街123号</p>
          </div>
          <div class="col-md-4">
            <h5>营业时间</h5>
            <p><i class="fas fa-clock"></i> 周一至周五: 9:00 - 22:00</p>
            <p><i class="fas fa-clock"></i> 周末及节假日: 8:00 - 23:00</p>
          </div>
        </div>
        <div class="text-center py-3 border-top mt-4">
          <p class="mb-0">&copy; 2025 餐饮点餐系统. 保留所有权利.</p>
        </div>
      </div>
    </footer>
    
    <!-- 右侧栏功能 -->
    <div class="side-toolbar">
      <div class="tool-item" @click="showFeedback" title="问题反馈">
        <i class="bi bi-chat-square-dots"></i>
      </div>
      <div class="tool-item" @click="scrollToTop" title="回到顶部">
        <i class="bi bi-arrow-up"></i>
      </div>
      <div class="tool-item" @click="contactSupport" title="联系客服">
        <i class="bi bi-headset"></i>
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
              <div class="mt-2">
                <strong>总价: ¥{{ (selectedDish.price * quantity).toFixed(2) }}</strong>
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
    
    <!-- 反馈模态框 -->
    <div class="modal fade" id="feedbackModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">问题反馈</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitFeedback">
              <div class="mb-3">
                <label class="form-label">反馈类型</label>
                <select class="form-select" v-model="feedbackForm.type">
                  <option value="suggestion">建议</option>
                  <option value="problem">问题</option>
                  <option value="complaint">投诉</option>
                  <option value="other">其他</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">反馈内容</label>
                <textarea class="form-control" rows="4" v-model="feedbackForm.content" required></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">联系方式（可选）</label>
                <input type="text" class="form-control" v-model="feedbackForm.contact">
              </div>
              <button type="submit" class="btn btn-primary">提交反馈</button>
            </form>
          </div>
        </div>
      </div>
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
      searchTerm: '',
      sortBy: '',
      selectedCategory: '',
      selectedDish: null,
      specifications: {
        size: '中份',
        spicy: '不辣',
        sweetness: '无糖'
      },
      quantity: 1,
      feedbackForm: {
        type: 'suggestion',
        content: '',
        contact: ''
      },
      // 分页相关数据
      currentPage: 1,
      pageSize: 10  // 默认每页显示10条
    }
  },
  
  computed: {
    filteredDishes() {
      let result = this.dishes
      
      // 搜索过滤
      if (this.searchTerm) {
        result = result.filter(dish => 
          dish.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          dish.description.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          (dish.category && dish.category.name.toLowerCase().includes(this.searchTerm.toLowerCase()))
        )
      }
      
      // 分类筛选
      if (this.selectedCategory) {
        result = result.filter(dish => 
          dish.category && dish.category.name === this.selectedCategory
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
        case 'rating_desc':
          result.sort((a, b) => b.rating - a.rating)
          break
        default:
          // 默认顺序
          break
      }
      
      return result
    },
    
    // 计算所有分类
    allCategories() {
      const categories = []
      this.dishes.forEach(dish => {
        if (dish.category && !categories.find(cat => cat.name === dish.category.name)) {
          categories.push(dish.category)
        }
      })
      return categories
    },
    
    // 计算总页数
    totalPages() {
      return Math.ceil(this.filteredDishes.length / this.pageSize)
    },
    
    // 计算当前页要显示的菜品
    paginatedDishes() {
      // 确保当前页不会超出范围
      if (this.currentPage > this.totalPages && this.totalPages > 0) {
        this.currentPage = this.totalPages;
      } else if (this.currentPage < 1) {
        this.currentPage = 1;
      }
      
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      
      // 确保不会超出数组范围
      return this.filteredDishes.slice(startIndex, Math.min(endIndex, this.filteredDishes.length));
    },
    
    // 计算可见的页码（最多显示5个页码）
    visiblePages() {
      const pages = []
      let start = Math.max(1, this.currentPage - 2)
      let end = Math.min(this.totalPages, start + 4)
      
      // 确保始终显示5个页码（除非总页数少于5）
      if (end - start < 4) {
        start = Math.max(1, end - 4)
      }
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      
      return pages
    }
  },
  
  watch: {
    // 当筛选条件改变时，重置到第一页
    filteredDishes() {
      this.currentPage = 1
    },
    
    // 监听总页数变化，确保当前页不会超出范围
    totalPages(newVal) {
      if (this.currentPage > newVal && newVal > 0) {
        this.currentPage = newVal
      } else if (newVal === 0) {
        this.currentPage = 1
      }
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
      } catch (error) {
        console.error('加载菜品失败:', error)
        // 出错时使用模拟数据
        this.dishes = this.getMockDishes()
        this.$root.showMessage('加载真实菜品数据失败，使用模拟数据')
      }
    },
    
    getMockDishes() {
      return [
        {
          id: 1,
          name: '宫保鸡丁',
          description: '经典川菜，鸡肉丁与花生米炒制，酸甜微辣',
          price: 28.8,
          category: {id: 1, name: '川菜'},
          rating: 4.5,
          reviewCount: 24,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/53/kung-pao-chicken-1768536_1280.jpg'
        },
        {
          id: 2,
          name: '麻婆豆腐',
          description: '嫩滑豆腐配以麻辣肉糜，口感丰富',
          price: 22.5,
          category: {id: 1, name: '川菜'},
          rating: 4.3,
          reviewCount: 18,
          image_url: 'https://cdn.pixabay.com/photo/2017/08/18/17/16/mapo-tofu-2655484_1280.jpg'
        },
        {
          id: 3,
          name: '红烧肉',
          description: '精选五花肉，慢火炖煮，肥而不腻',
          price: 35.0,
          category: {id: 2, name: '粤菜'},
          rating: 4.8,
          reviewCount: 32,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/35/braised-pork-1768568_1280.jpg'
        },
        {
          id: 4,
          name: '鱼香肉丝',
          description: '猪肉丝配木耳胡萝卜，鱼香味浓',
          price: 26.8,
          category: {id: 1, name: '川菜'},
          rating: 4.2,
          reviewCount: 15,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/36/yuxiang-shredded-pork-1768569_1280.jpg'
        },
        {
          id: 5,
          name: '糖醋里脊',
          description: '外酥内嫩的猪里脊，酸甜可口',
          price: 32.0,
          category: {id: 3, name: '鲁菜'},
          rating: 4.6,
          reviewCount: 21,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/37/sweet-and-sour-pork-1768570_1280.jpg'
        },
        {
          id: 6,
          name: '水煮鱼',
          description: '鲜嫩鱼片配豆芽菜，麻辣鲜香',
          price: 45.0,
          category: {id: 1, name: '川菜'},
          rating: 4.7,
          reviewCount: 28,
          image_url: 'https://cdn.pixabay.com/photo/2016/11/24/10/01/fish-1854444_1280.jpg'
        },
        {
          id: 7,
          name: '意大利面',
          description: '经典意式面条，配以番茄酱和新鲜罗勒',
          price: 38.5,
          category: {id: 4, name: '西式'},
          rating: 4.4,
          reviewCount: 19,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/38/pasta-1768582_1280.jpg'
        },
        {
          id: 8,
          name: '牛排',
          description: '优质牛肉，煎至完美，配以黑椒汁',
          price: 68.0,
          category: {id: 4, name: '西式'},
          rating: 4.9,
          reviewCount: 35,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/40/steak-1768599_1280.jpg'
        },
        {
          id: 9,
          name: '奶油蘑菇汤',
          description: '浓郁奶油汤底，配以新鲜蘑菇',
          price: 18.0,
          category: {id: 5, name: '汤类'},
          rating: 4.1,
          reviewCount: 14,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/41/mushroom-soup-1768593_1280.jpg'
        },
        {
          id: 10,
          name: '番茄蛋花汤',
          description: '新鲜番茄配鸡蛋，酸甜开胃',
          price: 15.5,
          category: {id: 5, name: '汤类'},
          rating: 4.0,
          reviewCount: 12,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/42/tomato-soup-1768596_1280.jpg'
        },
        {
          id: 11,
          name: '柠檬汽水',
          description: '新鲜柠檬制作，清凉解渴',
          price: 12.0,
          category: {id: 6, name: '饮品'},
          rating: 4.2,
          reviewCount: 16,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/43/lemonade-1768603_1280.jpg'
        },
        {
          id: 12,
          name: '拿铁咖啡',
          description: '意式浓缩咖啡配以丝滑牛奶',
          price: 22.0,
          category: {id: 6, name: '饮品'},
          rating: 4.5,
          reviewCount: 22,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/44/latte-1768607_1280.jpg'
        },
        {
          id: 13,
          name: '提拉米苏',
          description: '经典意式甜点，咖啡与奶油的完美结合',
          price: 26.5,
          category: {id: 7, name: '甜点'},
          rating: 4.8,
          reviewCount: 27,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/45/tiramisu-1768612_1280.jpg'
        },
        {
          id: 14,
          name: '芒果布丁',
          description: '新鲜芒果制作，口感细腻',
          price: 18.8,
          category: {id: 7, name: '甜点'},
          rating: 4.3,
          reviewCount: 15,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/46/mango-pudding-1768615_1280.jpg'
        },
        {
          id: 15,
          name: '炸鸡翅',
          description: '香脆外皮，鲜嫩多汁',
          price: 29.9,
          category: {id: 8, name: '小吃'},
          rating: 4.4,
          reviewCount: 20,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/47/fried-chicken-wings-1768620_1280.jpg'
        },
        {
          id: 16,
          name: '春卷',
          description: '酥脆外皮，配以新鲜蔬菜',
          price: 16.5,
          category: {id: 8, name: '小吃'},
          rating: 4.0,
          reviewCount: 11,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/48/spring-rolls-1768623_1280.jpg'
        },
        {
          id: 17,
          name: '扬州炒饭',
          description: '经典中式炒饭，配以虾仁、火腿、鸡蛋',
          price: 24.0,
          category: {id: 2, name: '粤菜'},
          rating: 4.3,
          reviewCount: 17,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/50/fried-rice-1768550_1280.jpg'
        },
        {
          id: 18,
          name: '海鲜披萨',
          description: '薄脆饼底，配以新鲜海鲜和芝士',
          price: 52.0,
          category: {id: 4, name: '西式'},
          rating: 4.6,
          reviewCount: 23,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/52/pizza-1768557_1280.jpg'
        },
        {
          id: 19,
          name: '紫菜蛋花汤',
          description: '清淡营养，紫菜配鸡蛋花',
          price: 13.5,
          category: {id: 5, name: '汤类'},
          rating: 3.9,
          reviewCount: 9,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/42/tomato-soup-1768596_1280.jpg'
        },
        {
          id: 20,
          name: '芝士蛋糕',
          description: '浓郁芝士口感，丝滑细腻',
          price: 28.0,
          category: {id: 7, name: '甜点'},
          rating: 4.7,
          reviewCount: 19,
          image_url: 'https://cdn.pixabay.com/photo/2016/10/25/12/51/cheesecake-1768554_1280.jpg'
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
      import('bootstrap/dist/js/bootstrap.esm.js').then((bootstrap) => {
        const modal = new bootstrap.Modal(document.getElementById('specModal'))
        modal.show()
      }).catch((error) => {
        console.error('Failed to load Bootstrap:', error)
      })
    },
    
    viewReviews(dish) {
      // 跳转到评论页面
      this.$router.push(`/dishes/${dish.id}/reviews`)
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
    },
    
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },
    
    scrollToMenu() {
      document.getElementById('menu-section').scrollIntoView({ behavior: 'smooth' })
    },
    
    showFeedback() {
      this.feedbackForm = {
        type: 'suggestion',
        content: '',
        contact: ''
      }
      
      import('bootstrap/dist/js/bootstrap.esm.js').then((bootstrap) => {
        const modal = new bootstrap.Modal(document.getElementById('feedbackModal'))
        modal.show()
      }).catch((error) => {
        console.error('Failed to load Bootstrap:', error)
      })
    },
    
    submitFeedback() {
      // 关闭模态框
      import('bootstrap/dist/js/bootstrap.esm.js').then((bootstrap) => {
        const modalEl = document.getElementById('feedbackModal')
        const modal = bootstrap.Modal.getInstance(modalEl)
        if (modal) {
          modal.hide()
        }
      }).catch((error) => {
        console.error('Failed to load Bootstrap:', error)
        // 如果无法加载Bootstrap，手动隐藏模态框
        const modalEl = document.getElementById('feedbackModal')
        if (modalEl) {
          modalEl.style.display = 'none'
          document.body.classList.remove('modal-open')
        }
      })
      
      this.$root.showMessage('感谢您的反馈！')
    },
    
    contactSupport() {
      this.$root.showMessage('客服电话: 400-123-4567')
    },
    
    // 页面大小更改处理
    onPageSizeChange(event) {
      this.pageSize = parseInt(event.target.value);
      this.currentPage = 1;
    },
    
    // 分页相关方法
    changePage(page) {
      // 添加边界检查
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        // 滚动到菜品区域顶部
        document.getElementById('menu-section').scrollIntoView({ behavior: 'smooth' })
      } else if (this.totalPages > 0 && page > this.totalPages) {
        // 如果页面超出范围，转到最后一页面
        this.currentPage = this.totalPages
        document.getElementById('menu-section').scrollIntoView({ behavior: 'smooth' })
      } else if (page < 1) {
        // 如果页面小于1，转到第一页
        this.currentPage = 1
        document.getElementById('menu-section').scrollIntoView({ behavior: 'smooth' })
      }
    }
  }
}
</script>

<style scoped>
.page-header {
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('https://cdn.pixabay.com/photo/2016/10/25/12/39/noodles-1768577_1280.jpg') center/cover;
}

.dish-card {
  transition: transform 0.3s ease;
}

.dish-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.category-filter {
  position: sticky;
  top: 20px;
}

.side-toolbar {
  position: fixed;
  right: 20px;
  top: 60%;
  transform: translateY(-50%);
  z-index: 1000;
}

.tool-item {
  background-color: #007bff;
  color: white;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
  border-radius: 50%;
  cursor: pointer;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  transition: background-color 0.3s;
  font-size: 1.2rem;
}

.tool-item:hover {
  background-color: #0056b3;
}

.star {
  font-size: 1.2em;
}
</style>
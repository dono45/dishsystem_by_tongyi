<template>
  <div class="admin-dashboard">
    <h2>管理后台</h2>
    
    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'dishes' }" @click="activeTab = 'dishes'" href="#">菜品管理</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'orders' }" @click="activeTab = 'orders'" href="#">订单管理</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'statistics' }" @click="activeTab = 'statistics'" href="#">统计报表</a>
      </li>
    </ul>
    
    <!-- 菜品管理 -->
    <div v-if="activeTab === 'dishes'">
      <div class="d-flex justify-content-between mb-3">
        <h4>菜品列表</h4>
        <button class="btn btn-primary" @click="showAddDishModal">添加菜品</button>
      </div>
      
      <div class="row">
        <div class="col-md-4 mb-4" v-for="dish in dishes" :key="dish.id">
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
              <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                <button class="btn btn-sm btn-outline-primary" @click="editDish(dish)">编辑</button>
                <button class="btn btn-sm btn-outline-danger" @click="deleteDish(dish.id)">删除</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 订单管理 -->
    <div v-if="activeTab === 'orders'">
      <h4>所有订单</h4>
      
      <div class="card mb-3" v-for="order in orders" :key="order.id">
        <div class="card-header">
          <div class="d-flex justify-content-between">
            <span>订单号: {{ order.id }} - 用户: {{ order.user.username }}</span>
            <select class="form-select form-select-sm" style="width: auto;" 
                    :value="order.status" @change="updateOrderStatus(order.id, $event.target.value)">
              <option value="pending">待处理</option>
              <option value="confirmed">已确认</option>
              <option value="delivered">已送达</option>
            </select>
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
    
    <!-- 统计报表 -->
    <div v-if="activeTab === 'statistics'">
      <h4>统计报表</h4>
      <div class="row">
        <div class="col-md-4">
          <div class="card text-white bg-primary mb-3">
            <div class="card-header">总订单数</div>
            <div class="card-body">
              <h5 class="card-title">{{ orders.length }}</h5>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-success mb-3">
            <div class="card-header">总收入</div>
            <div class="card-body">
              <h5 class="card-title">¥{{ totalIncome.toFixed(2) }}</h5>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-info mb-3">
            <div class="card-header">菜品总数</div>
            <div class="card-body">
              <h5 class="card-title">{{ dishes.length }}</h5>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 添加/编辑菜品模态框 -->
    <div class="modal fade" id="dishModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingDish ? '编辑菜品' : '添加菜品' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label class="form-label">菜品名称</label>
                <input type="text" class="form-control" v-model="dishForm.name" required>
              </div>
              <div class="mb-3">
                <label class="form-label">描述</label>
                <textarea class="form-control" v-model="dishForm.description" rows="3"></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">价格</label>
                <input type="number" class="form-control" v-model="dishForm.price" step="0.01" required>
              </div>
              <div class="mb-3">
                <label class="form-label">图片URL</label>
                <input type="text" class="form-control" v-model="dishForm.image_url">
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
            <button type="button" class="btn btn-primary" @click="saveDish">{{ editingDish ? '更新' : '添加' }}</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      activeTab: 'dishes',
      dishes: [],
      orders: [],
      dishForm: {
        name: '',
        description: '',
        price: 0,
        image_url: ''
      },
      editingDish: null
    }
  },
  
  computed: {
    totalIncome() {
      return this.orders.reduce((total, order) => total + order.total_amount, 0)
    }
  },
  
  async mounted() {
    // 检查是否为管理员
    const user = JSON.parse(localStorage.getItem('user'))
    if (!user || !user.is_admin) {
      this.$router.push('/')
      return
    }
    
    await this.loadDishes()
    await this.loadOrders()
  },
  
  methods: {
    async loadDishes() {
      try {
        const response = await axios.get('/api/admin/dishes', {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        })
        this.dishes = response.data
      } catch (error) {
        this.$root.showMessage('加载菜品失败：' + (error.response?.data?.message || '未知错误'))
      }
    },
    
    async loadOrders() {
      try {
        const response = await axios.get('/api/admin/orders', {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        })
        this.orders = response.data
      } catch (error) {
        this.$root.showMessage('加载订单失败：' + (error.response?.data?.message || '未知错误'))
      }
    },
    
    showAddDishModal() {
      this.editingDish = null
      this.dishForm = {
        name: '',
        description: '',
        price: 0,
        image_url: ''
      }
      
      // 修复：显式导入Bootstrap模块
      import('bootstrap/dist/js/bootstrap.esm.js').then((bootstrap) => {
        const modal = new bootstrap.Modal(document.getElementById('dishModal'))
        modal.show()
      }).catch((error) => {
        console.error('Failed to load Bootstrap:', error)
      })
    },
    
    editDish(dish) {
      this.editingDish = dish
      this.dishForm = { ...dish }
      
      // 修复：显式导入Bootstrap模块
      import('bootstrap/dist/js/bootstrap.esm.js').then((bootstrap) => {
        const modal = new bootstrap.Modal(document.getElementById('dishModal'))
        modal.show()
      }).catch((error) => {
        console.error('Failed to load Bootstrap:', error)
      })
    },
    
    async saveDish() {
      try {
        if (this.editingDish) {
          // 更新菜品
          await axios.put(`/api/admin/dishes/${this.editingDish.id}`, this.dishForm, {
            headers: {
              'Authorization': 'Bearer ' + localStorage.getItem('token')
            }
          })
          this.$root.showMessage('菜品更新成功')
        } else {
          // 添加菜品
          await axios.post('/api/admin/dishes', this.dishForm, {
            headers: {
              'Authorization': 'Bearer ' + localStorage.getItem('token')
            }
          })
          this.$root.showMessage('菜品添加成功')
        }
        
        // 修复：显式导入Bootstrap模块
        import('bootstrap/dist/js/bootstrap.esm.js').then((bootstrap) => {
          // 关闭模态框
          const modalEl = document.getElementById('dishModal')
          const modal = bootstrap.Modal.getInstance(modalEl)
          modal.hide()
        }).catch((error) => {
          console.error('Failed to load Bootstrap:', error)
          // 如果无法加载Bootstrap，手动隐藏模态框
          const modalEl = document.getElementById('dishModal')
          if (modalEl) {
            modalEl.style.display = 'none'
            document.body.classList.remove('modal-open')
          }
        })
        
        // 重新加载菜品列表
        await this.loadDishes()
      } catch (error) {
        this.$root.showMessage('操作失败：' + (error.response?.data?.message || '未知错误'))
      }
    },
    
    async deleteDish(dishId) {
      if (!confirm('确定要删除这个菜品吗？')) {
        return
      }
      
      try {
        await axios.delete(`/api/admin/dishes/${dishId}`, {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        })
        
        this.$root.showMessage('菜品删除成功')
        await this.loadDishes()
      } catch (error) {
        this.$root.showMessage('删除失败：' + (error.response?.data?.message || '未知错误'))
      }
    },
    
    async updateOrderStatus(orderId, status) {
      try {
        await axios.put(`/api/admin/orders/${orderId}/status`, { status }, {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        })
        
        this.$root.showMessage('订单状态更新成功')
        await this.loadOrders()
      } catch (error) {
        this.$root.showMessage('更新失败：' + (error.response?.data?.message || '未知错误'))
      }
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN')
    }
  }
}
</script>
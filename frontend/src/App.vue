<template>
  <div id="app">
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <router-link class="navbar-brand" to="/">餐饮点餐系统</router-link>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">首页</router-link>
            </li>
          </ul>
          
          <ul class="navbar-nav">
            <template v-if="isLoggedIn">
              <!-- 购物车按钮 -->
              <li class="nav-item">
                <router-link class="nav-link" to="/cart">购物车</router-link>
              </li>
              
              <!-- 我的订单按钮 -->
              <li class="nav-item">
                <router-link class="nav-link" to="/orders">我的订单</router-link>
              </li>
            </template>
            
            <template v-if="!isLoggedIn">
              <li class="nav-item">
                <router-link class="nav-link" to="/login">登录</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/register">注册</router-link>
              </li>
            </template>
            
            <template v-else>
              <!-- 用户头像和信息 -->
              <li class="nav-item dropdown" ref="userDropdown">
                <a class="nav-link dropdown-toggle d-flex align-items-center" href="#" role="button" @click="toggleDropdown">
                  <div class="bg-light rounded-circle d-flex align-items-center justify-content-center me-2" style="width: 30px; height: 30px;">
                    <span class="text-primary fw-bold">{{ currentUser?.username?.charAt(0)?.toUpperCase() }}</span>
                  </div>
                  {{ currentUser?.username }}
                </a>
                <ul class="dropdown-menu dropdown-menu-end" ref="dropdownMenu">
                  <li><span class="dropdown-item-text">欢迎, {{ currentUser?.username }}!</span></li>
                  <li><hr class="dropdown-divider"></li>
                  <li><a class="dropdown-item" href="#" @click="logout">退出</a></li>
                </ul>
              </li>
            </template>
            
            <!-- 管理员入口 -->
            <template v-if="isLoggedIn && currentUser && currentUser.is_admin">
              <li class="nav-item">
                <router-link class="nav-link" to="/admin">管理后台</router-link>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>
    
    <!-- 页面内容 -->
    <div class="container-fluid p-0">
      <router-view />
    </div>
    
    <!-- 消息提示 -->
    <div class="toast-container position-fixed bottom-0 end-0 p-3">
      <div id="messageToast" class="toast" role="alert">
        <div class="toast-header">
          <strong class="me-auto">提示</strong>
          <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">
          {{ message }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: false,
      currentUser: null,
      message: '',
      isDropdownOpen: false
    }
  },
  
  mounted() {
    // 检查本地存储的token
    this.checkLoginStatus()
    
    // 监听路由变化，重新检查登录状态
    this.$router.afterEach(() => {
      this.checkLoginStatus()
    })
    
    // 添加全局点击监听器，用于关闭下拉菜单
    document.addEventListener('click', this.handleDocumentClick)
  },
  
  beforeUnmount() {
    // 清理事件监听器
    document.removeEventListener('click', this.handleDocumentClick)
  },
  
  methods: {
    checkLoginStatus() {
      const token = localStorage.getItem('token')
      if (token) {
        try {
          this.isLoggedIn = true
          this.currentUser = JSON.parse(localStorage.getItem('user'))
        } catch (e) {
          // 如果解析失败，清除无效的存储数据
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          this.isLoggedIn = false
          this.currentUser = null
        }
      } else {
        this.isLoggedIn = false
        this.currentUser = null
      }
    },
    
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      this.isLoggedIn = false
      this.currentUser = null
      this.$router.push('/')
    },
    
    showMessage(text) {
      this.message = text
      const toastEl = document.getElementById('messageToast')
      if (toastEl) {
        // 动态导入 Bootstrap Toast
        import('bootstrap/dist/js/bootstrap.esm.js').then((bootstrap) => {
          const toast = new bootstrap.Toast(toastEl)
          toast.show()
        }).catch((error) => {
          console.error('Failed to load Bootstrap:', error)
          // 如果 Bootstrap 加载失败，使用简单的 alert
          alert(text)
        })
      }
    },
    
    toggleDropdown(event) {
      event.preventDefault()
      this.isDropdownOpen = !this.isDropdownOpen
      
      // 使用动态导入确保 Bootstrap 可用
      import('bootstrap/dist/js/bootstrap.esm.js').then((bootstrap) => {
        const dropdownMenu = this.$refs.dropdownMenu
        if (this.isDropdownOpen) {
          dropdownMenu.classList.add('show')
        } else {
          dropdownMenu.classList.remove('show')
        }
      }).catch(() => {
        // 如果 Bootstrap 不可用，使用手动方式
        const dropdownMenu = this.$refs.dropdownMenu
        if (this.isDropdownOpen) {
          dropdownMenu.style.display = 'block'
        } else {
          dropdownMenu.style.display = 'none'
        }
      })
    },
    
    handleDocumentClick(event) {
      // 如果下拉菜单是打开的，并且点击不在下拉菜单或触发元素上，则关闭下拉菜单
      if (this.isDropdownOpen && this.$refs.userDropdown && !this.$refs.userDropdown.contains(event.target)) {
        this.isDropdownOpen = false
        import('bootstrap/dist/js/bootstrap.esm.js').then((bootstrap) => {
          const dropdownMenu = this.$refs.dropdownMenu
          dropdownMenu.classList.remove('show')
        }).catch(() => {
          // 如果 Bootstrap 不可用，使用手动方式
          const dropdownMenu = this.$refs.dropdownMenu
          dropdownMenu.style.display = 'none'
        })
      }
    }
  }
}
</script>

<style>
.navbar-brand, .nav-link {
  cursor: pointer;
}
</style>
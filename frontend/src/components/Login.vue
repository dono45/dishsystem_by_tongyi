<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card">
        <div class="card-header">
          <h3 class="text-center">用户登录</h3>
        </div>
        <div class="card-body">
          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label for="username" class="form-label">用户名</label>
              <input 
                type="text" 
                class="form-control" 
                id="username" 
                v-model="form.username" 
                required
              >
            </div>
            
            <div class="mb-3">
              <label for="password" class="form-label">密码</label>
              <input 
                type="password" 
                class="form-control" 
                id="password" 
                v-model="form.password" 
                required
              >
            </div>
            
            <div class="d-grid">
              <button type="submit" class="btn btn-primary">登录</button>
            </div>
          </form>
          
          <div class="mt-3 text-center">
            <router-link to="/register">没有账户？立即注册</router-link>
            <br>
            <a href="#" @click="forgotPassword">忘记密码？</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      form: {
        username: '',
        password: ''
      }
    }
  },
  
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post('/api/login', this.form)
        
        // 保存token和用户信息到本地存储
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        
        // 显示成功消息
        this.$root.showMessage('登录成功')
        
        // 跳转到主页
        this.$router.push('/')
      } catch (error) {
        this.$root.showMessage('登录失败：' + (error.response?.data?.message || '未知错误'))
      }
    },
    
    forgotPassword() {
      // 这里应该跳转到忘记密码页面或显示模态框
      this.$root.showMessage('请联系管理员重置密码')
    }
  }
}
</script>
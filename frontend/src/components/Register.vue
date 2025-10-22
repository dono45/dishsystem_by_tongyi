<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card">
        <div class="card-header">
          <h3 class="text-center">用户注册</h3>
        </div>
        <div class="card-body">
          <form @submit.prevent="handleRegister">
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
              <label for="email" class="form-label">邮箱</label>
              <input 
                type="email" 
                class="form-control" 
                id="email" 
                v-model="form.email" 
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
            
            <div class="mb-3">
              <label for="confirmPassword" class="form-label">确认密码</label>
              <input 
                type="password" 
                class="form-control" 
                id="confirmPassword" 
                v-model="form.confirmPassword" 
                required
              >
            </div>
            
            <div class="d-grid">
              <button type="submit" class="btn btn-success">注册</button>
            </div>
          </form>
          
          <div class="mt-3 text-center">
            <router-link to="/login">已有账户？立即登录</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Register',
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      }
    }
  },
  
  methods: {
    async handleRegister() {
      // 验证密码匹配
      if (this.form.password !== this.form.confirmPassword) {
        this.$root.showMessage('两次输入的密码不一致')
        return
      }
      
      try {
        // 发送注册请求
        await axios.post('/api/register', {
          username: this.form.username,
          email: this.form.email,
          password: this.form.password
        })
        
        // 显示成功消息
        this.$root.showMessage('注册成功，请登录')
        
        // 跳转到登录页面
        this.$router.push('/login')
      } catch (error) {
        this.$root.showMessage('注册失败：' + (error.response?.data?.message || '未知错误'))
      }
    }
  }
}
</script>
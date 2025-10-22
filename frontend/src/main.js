import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './components/Home.vue'
import Login from './components/Login.vue'
import Register from './components/Register.vue'
import AdminDashboard from './components/AdminDashboard.vue'
import Cart from './components/Cart.vue'
import Orders from './components/Orders.vue'
import Review from './components/Review.vue'

// 引入 Bootstrap 的 CSS 和 JavaScript
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css'

// 定义路由
const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/dishes/:dishId/reviews', component: Review, props: true },
  { path: '/cart', component: Cart },
  { path: '/orders', component: Orders },
  { path: '/admin', component: AdminDashboard },
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 创建Vue应用实例
const app = createApp(App)
app.use(router)
app.mount('#app')
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import { marked } from 'marked'
import hljs from 'highlight.js'

// 导入样式
import './assets/styles/main.css'

// 配置 marked
marked.setOptions({
  highlight: function (code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value
    }
    return hljs.highlightAuto(code).value
  },
  breaks: true
})

Vue.prototype.$marked = marked

Vue.config.productionTip = false

// 配置 axios
const axiosInstance = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'https://resume-match-api.bitboy.games',
  timeout: 1200000,
  headers: {
    'Content-Type': 'application/json'
  }
})

Vue.prototype.$axios = axiosInstance

new Vue({
  router,
  render: h => h(App)
}).$mount('#app') 
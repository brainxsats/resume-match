import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import { marked } from 'marked'
import hljs from 'highlight.js'

// 导入样式
import './assets/styles/main.css'

// 配置 axios
axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000'
// 配置请求超时时间
axios.defaults.timeout = 120000
// 配置请求头
axios.defaults.headers.post['Content-Type'] = 'application/json'

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
Vue.prototype.$axios = axios

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app') 
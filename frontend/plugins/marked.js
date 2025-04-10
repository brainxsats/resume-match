import Vue from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'

// 配置marked选项
marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value
    }
    return hljs.highlightAuto(code).value
  },
  breaks: true,
  gfm: true
})

// 注册为Vue插件
Vue.prototype.$marked = marked 
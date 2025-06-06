<template>
  <div class="min-h-screen bg-gray-900 py-8">
    <div class="container mx-auto px-4 max-w-7xl">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-bold text-gray-100">分析报告</h1>
        <button
          @click="$router.push('/')"
          class="px-4 py-2 text-sm text-gray-300 border border-gray-600 rounded-md hover:bg-gray-800 transition-colors"
        >
          返回首页
        </button>
      </div>
      
      <div class="bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-700">
        <div ref="reportContent" class="report-content"></div>
      </div>

      <!-- 添加获取总结报告按钮 -->
      <div class="mt-4 flex justify-center">
        <button
          @click="fetchSummaryReport"
          :disabled="isLoading"
          class="px-4 py-2 text-sm text-gray-300 border border-gray-600 rounded-md hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="isLoading" class="flex items-center">
            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-gray-300" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            正在生成总结报告...
          </span>
          <span v-else>获取总结报告</span>
        </button>
      </div>

      <!-- 添加加载弹窗 -->
      <div v-if="isLoading" class="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center z-50">
        <div class="bg-gray-800 p-8 rounded-lg shadow-xl border border-gray-700 max-w-md w-full mx-4">
          <div class="flex flex-col items-center">
            <svg class="animate-spin h-12 w-12 text-blue-500 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <h3 class="text-lg font-medium text-gray-100 mb-2">正在生成总结报告</h3>
            <p class="text-gray-400 text-center">请稍候，我们正在为您生成一份简洁的总结报告...</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked'
import hljs from 'highlight.js'
import axios from 'axios'

export default {
  name: 'Report',
  
  data() {
    return {
      content: '',
      isAnimating: false,
      summaryContent: '',
      isLoading: false
    }
  },

  created() {
    // 配置 marked
    marked.setOptions({
      highlight: function(code, lang) {
        if (lang && hljs.getLanguage(lang)) {
          try {
            return hljs.highlight(code, { language: lang }).value
          } catch (e) {
            console.error(e)
          }
        }
        return code
      },
      breaks: true,
      gfm: true,
      mangle: false,
      headerIds: false
    })

    // 从路由参数或缓存中获取报告内容
    let content = ''
    if (this.$route.params.report) {
      content = this.$route.params.report
      // 保存到 sessionStorage，这样返回时可以恢复
      sessionStorage.setItem('reportContent', content)
    } else {
      // 如果没有路由参数，尝试从 sessionStorage 恢复
      const cachedContent = sessionStorage.getItem('reportContent')
      if (cachedContent) {
        content = cachedContent
      }
    }

    // 解析 Unicode 转义序列
    if (content) {
      try {
        // 将 JSON 字符串中的 Unicode 转义序列解析为实际字符
        const jsonStr = `{"content": ${JSON.stringify(content)}}`
        const parsed = JSON.parse(jsonStr)
        this.content = parsed.content
      } catch (e) {
        console.error('解析内容失败:', e)
        this.content = content
      }
    }
  },

  beforeDestroy() {
    // 组件销毁前保存内容到 sessionStorage
    if (this.content) {
      sessionStorage.setItem('reportContent', this.content)
    }
  },

  mounted() {
    // 在 DOM 挂载完成后展示内容
    if (this.content) {
      this.$nextTick(() => {
        // 如果是从缓存恢复的内容，直接显示
        if (this.$route.params.report) {
          this.animateContent() // 新内容使用动画展示
        } else {
          this.displayContent() // 缓存内容直接显示
        }
      })
    }
  },

  methods: {
    async fetchSummaryReport() {
      try {
        // 从 localStorage 获取数据
        const formDataStr = localStorage.getItem('formData')
        if (!formDataStr) {
          throw new Error('缺少必要的简历或职位信息')
        }
        
        const formData = JSON.parse(formDataStr)
        const resume = formData.resume
        const job = formData.job
        
        if (!resume || !job) {
          throw new Error('缺少必要的简历或职位信息')
        }

        this.isLoading = true
        const apiUrl = process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000'
        const response = await axios.post(`${apiUrl}/api/analyze-dify-summary`, {
          resume: resume,
          job: job,
          report: this.content
        }, {
          responseType: 'text',
          headers: {
            'Content-Type': 'application/json'
          }
        })

        if (response.status !== 200) {
          throw new Error(`请求失败: ${response.status} ${response.statusText}`)
        }

        let content = ''
        const lines = response.data.split('\n')
        for (const line of lines) {
          if (line.trim() && line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              if (data.content) {
                content += data.content
              }
            } catch (e) {
              console.error('解析响应数据失败:', e)
            }
          }
        }

        if (content) {
          // 保存到 sessionStorage，这样返回时可以恢复
          sessionStorage.setItem('summaryContent', content)
          // 跳转到新页面展示总结报告，标记为新数据
          this.$router.push({
            name: 'summary',
            params: { 
              summary: content,
              isNew: true
            }
          })
        } else {
          throw new Error('获取总结报告失败：返回内容为空')
        }
      } catch (error) {
        console.error('获取总结报告出错:', error)
        alert('获取总结报告出错：' + (error.response?.data?.message || error.message))
      } finally {
        this.isLoading = false
      }
    },

    displayContent() {
      if (!this.content || !this.$refs.reportContent) return

      const container = this.$refs.reportContent
      container.innerHTML = ''

      // 将内容按段落分割
      const segments = this.processContent(this.content)
      
      // 一次性显示所有内容
      const allContent = segments.map(segment => {
        const htmlContent = marked(segment)
        const element = document.createElement('div')
        element.innerHTML = htmlContent
        
        // 添加样式
        const children = Array.from(element.children)
        if (children.length > 0) {
          children.forEach(child => {
            this.applyStyles(child)
          })
        } else {
          // 如果没有子元素，说明是纯文本，创建一个段落包装它
          const p = document.createElement('p')
          p.className = 'markdown-paragraph'
          p.innerHTML = htmlContent
          element.innerHTML = ''
          element.appendChild(p)
        }
        
        return element.outerHTML
      }).join('')

      container.innerHTML = allContent
    },

    async animateContent() {
      if (!this.content || this.isAnimating || !this.$refs.reportContent) return

      this.isAnimating = true
      const container = this.$refs.reportContent
      container.innerHTML = ''

      // 将内容按段落分割
      const segments = this.processContent(this.content)
      
      // 逐段显示内容
      for (const segment of segments) {
        const htmlContent = marked(segment)
        const element = document.createElement('div')
        element.innerHTML = htmlContent
        
        // 添加样式
        const children = Array.from(element.children)
        if (children.length > 0) {
          children.forEach(child => {
            this.applyStyles(child)
          })
        } else {
          // 如果没有子元素，说明是纯文本，创建一个段落包装它
          const p = document.createElement('p')
          p.className = 'markdown-paragraph'
          p.innerHTML = htmlContent
          element.innerHTML = ''
          element.appendChild(p)
        }

        // 添加到容器并设置动画
        container.appendChild(element)
        element.style.opacity = '0'
        element.style.transform = 'translateY(20px)'
        
        await new Promise(resolve => {
          window.requestAnimationFrame(() => {
            element.style.transition = 'opacity 0.5s ease, transform 0.5s ease'
            element.style.opacity = '1'
            element.style.transform = 'translateY(0)'
            
            // 计算滚动位置
            const elementBottom = element.offsetTop + element.offsetHeight
            const containerBottom = window.scrollY + window.innerHeight
            
            // 如果新添加的元素底部超出可视区域，则滚动到合适位置
            if (elementBottom > containerBottom) {
              const scrollTarget = elementBottom - window.innerHeight + 100 // 额外偏移量，确保内容在视野中
              window.scrollTo({
                top: scrollTarget,
                behavior: 'smooth'
              })
            }
            
            setTimeout(resolve, 500)
          })
        })
      }

      this.isAnimating = false
    },

    processContent(content) {
      if (!content) return []
      
      const segments = []
      let currentSegment = ''
      const lines = content.split('\n')
      
      for (const line of lines) {
        // 检查是否是新的段落开始
        if (line.match(/^#{1,6}\s/) || // 标题
            line.match(/^[-*+]\s/) || // 无序列表
            line.match(/^\d+\.\s/) || // 有序列表
            !line.trim()) { // 空行
          if (currentSegment.trim()) {
            segments.push(currentSegment.trim())
          }
          if (line.trim()) {
            segments.push(line)
          }
          currentSegment = ''
        } else {
          if (currentSegment && !line.startsWith(' ') && !line.startsWith('\t')) {
            currentSegment += ' '
          }
          currentSegment += line
        }
      }
      
      if (currentSegment.trim()) {
        segments.push(currentSegment.trim())
      }
      
      return segments.filter(Boolean) // 过滤掉空字符串
    },

    applyStyles(element) {
      if (!element) return

      // 根据元素类型添加对应的类名和样式
      if (element.tagName.match(/^H[1-6]$/)) {
        element.classList.add('markdown-heading')
        if (element.tagName === 'H1') {
          element.style.fontSize = '1.4em'
          element.style.borderBottom = '1px solid #4b5563'
          element.style.paddingBottom = '0.5em'
        } else if (element.tagName === 'H2') {
          element.style.fontSize = '1.2em'
          element.style.marginTop = '1.5em'
        } else if (element.tagName === 'H3') {
          element.style.fontSize = '1.1em'
          element.style.marginTop = '1.2em'
        }
      } else if (element.tagName === 'P') {
        element.classList.add('markdown-paragraph')
      } else if (element.tagName === 'UL' || element.tagName === 'OL') {
        element.classList.add('markdown-list')
        const items = element.getElementsByTagName('li')
        Array.from(items).forEach(item => {
          item.classList.add('markdown-list-item')
          const text = item.textContent
          if (text.startsWith('✓')) {
            item.style.color = '#34D399'
            item.style.listStyleType = 'none'
          } else if (text.startsWith('⚠️')) {
            item.style.color = '#FBBF24'
            item.style.listStyleType = 'none'
          }
        })
      }
    }
  }
}
</script>

<style scoped>
.report-content {
  color: #e5e7eb;
  font-size: 16px;
  line-height: 1.8;
  letter-spacing: 0.3px;
}

.markdown-heading {
  color: #f3f4f6;
  margin: 1.8em 0 1em;
  line-height: 1.4;
  font-weight: bold;
}

.markdown-paragraph {
  margin: 0.8em 0;
  line-height: 1.8;
}

.markdown-list {
  margin: 1em 0;
  padding-left: 1.5em;
}

.markdown-list-item {
  margin: 0.5em 0;
  line-height: 1.8;
}

/* 确保纯文本内容也有正确的样式 */
.report-content > div {
  margin-bottom: 1em;
}

.report-content > div:last-child {
  margin-bottom: 0;
}
</style> 
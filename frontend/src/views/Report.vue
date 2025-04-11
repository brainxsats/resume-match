<template>
  <div class="min-h-screen bg-gray-900 py-8">
    <div class="container mx-auto px-4 max-w-7xl">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-bold text-gray-100">人才报告</h1>
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
    </div>
  </div>
</template>

<script>
import { marked } from 'marked'
import hljs from 'highlight.js'

export default {
  name: 'Report',
  
  data() {
    return {
      content: '',
      isAnimating: false
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

    // 从路由参数获取报告内容
    if (this.$route.params.report) {
      this.content = this.$route.params.report
    }
  },

  mounted() {
    // 在 DOM 挂载完成后执行动画
    if (this.content) {
      this.$nextTick(() => {
        this.animateContent()
      })
    }
  },

  methods: {
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
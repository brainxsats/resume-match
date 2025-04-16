<template>
  <div class="min-h-screen bg-gray-900 py-8">
    <div class="container mx-auto px-4 max-w-7xl">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-bold text-gray-100">总结报告</h1>
        <button
          @click="goBack"
          class="px-4 py-2 text-sm text-gray-300 border border-gray-600 rounded-md hover:bg-gray-800 transition-colors"
        >
          返回分析报告
        </button>
      </div>
      
      <div class="bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-700">
        <Report 
          :content="content" 
          :animate="isNew"
        />
      </div>
    </div>
  </div>
</template>

<script>
import Report from '@/components/Report.vue'

export default {
  name: 'Summary',
  
  components: {
    Report
  },

  data() {
    return {
      content: '',
      isNew: false
    }
  },

  created() {
    // 从路由参数或缓存中获取报告内容
    let content = ''
    if (this.$route.params.summary) {
      content = this.$route.params.summary
      this.isNew = this.$route.params.isNew || false
      // 保存到 sessionStorage，这样返回时可以恢复
      sessionStorage.setItem('summaryContent', content)
    } else {
      // 如果没有路由参数，尝试从 sessionStorage 恢复
      const cachedContent = sessionStorage.getItem('summaryContent')
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

  methods: {
    goBack() {
      // 返回上一页，保持历史记录
      this.$router.go(-1)
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

/* 代码块样式 */
.report-content pre {
  margin: 1rem 0;
  padding: 1rem;
  background-color: #1f2937;
  border-radius: 0.375rem;
  overflow-x: auto;
}

.report-content code {
  background-color: #374151;
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-size: 0.875em;
}

/* 适配深色模式 */
@media (prefers-color-scheme: dark) {
  .report-content {
    color: #e5e7eb;
  }

  .markdown-heading {
    color: #f3f4f6;
  }

  .markdown-paragraph {
    color: #d1d5db;
  }

  .markdown-list-item {
    color: #d1d5db;
  }
}
</style> 
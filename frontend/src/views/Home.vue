<template>
  <div class="min-h-screen bg-gray-900 py-8">
    <div class="container mx-auto px-4 max-w-7xl">
      <h1 class="text-3xl font-bold text-gray-100 mb-8">简历匹配度分析</h1>
      <!-- <p class="text-gray-400 mb-8">请先填写您的工作经历，例位描述等，AI会根据您的经历定制化您的简历，可提升面试几率。</p> -->
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- 左侧：简历内容 -->
        <div class="bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-700">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">
                简历内容
              </label>
              <!-- PDF 预览区域 -->
              <div v-if="pdfPreviewUrl" class="mb-4">
                <div class="relative w-full h-[600px] bg-gray-700 rounded-lg overflow-hidden">
                  <iframe
                    :src="pdfPreviewUrl"
                    class="absolute inset-0 w-full h-full"
                    frameborder="0"
                  ></iframe>
                </div>
                <div class="mt-2 flex justify-end">
                  <button
                    @click="clearPdf"
                    class="text-sm text-red-400 hover:text-red-300 flex items-center"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    清除 PDF
                  </button>
                </div>
              </div>
              <!-- 文本输入区域 -->
              <textarea
                v-if="!pdfPreviewUrl"
                v-model="formData.resume"
                class="w-full h-[600px] p-4 bg-gray-700 text-gray-100 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-500"
                placeholder="请详细描述您的工作经历、项目经验、技能特长等。建议包含：

1. 工作/实习经历：公司、职位、时间段、主要职责和成就
2. 项目经验：项目名称、角色、技术栈、主要贡献
3. 技能特长：专业技能、证书、语言能力等"
              />
              <!-- PDF 上传区域 -->
              <div class="mt-4">
                <div class="flex items-center justify-center w-full">
                  <label class="flex flex-col w-full h-32 border-2 border-gray-600 border-dashed hover:bg-gray-800 hover:border-gray-500 rounded-lg cursor-pointer">
                    <div class="flex flex-col items-center justify-center pt-7">
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-gray-400 group-hover:text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                      <p class="pt-1 text-sm tracking-wider text-gray-400 group-hover:text-gray-300">
                        点击上传 PDF 简历或将文件拖放到这里
                      </p>
                    </div>
                    <input 
                      type="file" 
                      class="opacity-0" 
                      accept=".pdf"
                      @change="handleFileUpload"
                    />
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：职位信息 -->
        <div class="bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-700">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">
                目标职位信息
              </label>
              <textarea
                v-model="formData.job"
                class="w-full h-[800px] p-4 bg-gray-700 text-gray-100 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-500"
                placeholder="请输入目标职位的要求描述，包括：

1. 岗位职责
2. 任职要求
3. 技能要求
4. 其他要求（如工作年限、学历等）

AI 将帮您分析简历与职位的匹配程度，并提供优化建议。"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- 底部按钮 -->
      <div class="mt-8 flex justify-center">
        <button
          type="button"
          class="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          :class="{ 'opacity-50 cursor-not-allowed': loading }"
          :disabled="loading"
          @click="handleSubmit"
        >
          <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ loading ? '分析中...' : '开始分析' }}
        </button>
      </div>

      <!-- 加载动画 -->
      <div v-if="loading" class="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center">
        <div class="bg-gray-800 p-6 rounded-lg shadow-xl border border-gray-700">
          <div class="spinner"></div>
          <div class="mt-4 text-gray-300">正在分析中，请稍候...</div>
        </div>
      </div>

      <!-- 分析结果 -->
      <div v-show="showResult" class="mt-8 bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-700">
        <div ref="reportContent" class="report-content"></div>
      </div>
    </div>
  </div>
</template>

<script>
import hljs from 'highlight.js'
import { marked } from 'marked'

export default {
  name: 'Home',
  
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

    // 恢复数据
    const savedData = localStorage.getItem('formData')
    if (savedData) {
      this.formData = JSON.parse(savedData)
    }
  },
  
  beforeDestroy() {
    // 保存数据
    localStorage.setItem('formData', JSON.stringify(this.formData))
  },
  
  data() {
    return {
      formData: {
        resume: '',
        job: ''
      },
      pdfFile: null,
      pdfPreviewUrl: null,
      loading: false,
      showResult: false,
      markdownContent: '',
      lastContent: '',
      isProcessing: false
    }
  },

  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0]
      if (file && file.type === 'application/pdf') {
        this.pdfFile = file
        // 创建预览 URL
        this.pdfPreviewUrl = URL.createObjectURL(file)
        // 清空文本输入
        this.formData.resume = ''
      } else {
        alert('请上传 PDF 格式的文件')
      }
    },

    clearPdf() {
      this.pdfFile = null
      if (this.pdfPreviewUrl) {
        URL.revokeObjectURL(this.pdfPreviewUrl)
        this.pdfPreviewUrl = null
      }
    },

    resetForm() {
      this.formData.resume = ''
      this.formData.job = ''
      this.pdfFile = null
      if (this.$refs.pdfFile) {
        this.$refs.pdfFile.value = ''
      }
      this.showResult = false
      this.$refs.reportContent.innerHTML = ''
      this.markdownContent = ''
      this.lastContent = ''
    },

    printReport() {
      window.print()
    },

    processStreamContent(content) {
      const segments = []
      let currentSegment = ''
      const lines = content.split('\n')
      
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i]
        
        if (line.match(/^#{1,6}\s/)) {
          if (currentSegment.trim()) {
            segments.push(currentSegment.trim())
          }
          segments.push(line)
          currentSegment = ''
        }
        else if (line.match(/^[-*+]\s/) || line.match(/^\d+\.\s/)) {
          if (currentSegment.trim() && !currentSegment.match(/(?:^|\n)[-*+]\s/) && !currentSegment.match(/(?:^|\n)\d+\.\s/)) {
            segments.push(currentSegment.trim())
            currentSegment = ''
          }
          if (currentSegment && !currentSegment.endsWith('\n')) {
            currentSegment += '\n'
          }
          currentSegment += line
        }
        else if (!line.trim()) {
          if (currentSegment.trim()) {
            segments.push(currentSegment.trim())
          }
          currentSegment = ''
        }
        else {
          if (currentSegment && !line.startsWith(' ') && !line.startsWith('\t')) {
            currentSegment += ' '
          }
          currentSegment += line.trim()
        }
      }
      
      if (currentSegment.trim()) {
        segments.push(currentSegment.trim())
      }
      
      return segments
    },

    createStreamBlock(content) {
      const block = document.createElement('div')
      block.className = 'stream-block stream-content'
      block.style.display = 'block'
      block.innerHTML = content
      return block
    },

    smoothScrollToElement(element) {
      const container = document.documentElement
      const elementTop = element.offsetTop
      const containerTop = container.scrollTop
      const targetScroll = elementTop - containerTop - 100

      window.scrollTo({
        top: targetScroll,
        behavior: 'smooth'
      })
    },

    async displayContentWithDelay(content, container) {
      // 解析 markdown 内容
      const htmlContent = marked(content, {
        breaks: true,
        gfm: true,
        mangle: false,
        headerIds: false
      })

      // 创建临时容器
      const tempDiv = document.createElement('div')
      tempDiv.innerHTML = htmlContent

      // 处理不同类型的元素并添加对应的类名
      const elements = tempDiv.children
      for (let i = 0; i < elements.length; i++) {
        const element = elements[i]
        
        // 根据元素类型添加对应的类名
        if (element.tagName === 'H1' || element.tagName === 'H2' || 
            element.tagName === 'H3' || element.tagName === 'H4' || 
            element.tagName === 'H5' || element.tagName === 'H6') {
          element.classList.add('markdown-heading')
          
          // 为不同级别的标题添加特定样式
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
          for (let j = 0; j < items.length; j++) {
            const item = items[j]
            item.classList.add('markdown-list-item')
            
            // 处理特殊的列表项标记
            const text = item.textContent
            if (text.startsWith('✓')) {
              item.style.color = '#34D399' // 绿色
              item.style.listStyleType = 'none'
            } else if (text.startsWith('⚠️')) {
              item.style.color = '#FBBF24' // 黄色
              item.style.listStyleType = 'none'
            }
          }
        }

        // 如果是第一个内容，清空容器
        if (!container.hasChildNodes()) {
          container.innerHTML = ''
        }

        // 将处理后的元素添加到容器中
        container.appendChild(element)

        // 添加渐入动画效果
        element.style.opacity = '0'
        element.style.transform = 'translateY(10px)'
        
        // 使用 requestAnimationFrame 确保动画流畅
        requestAnimationFrame(() => {
          element.style.transition = 'opacity 0.3s ease, transform 0.3s ease'
          element.style.opacity = '1'
          element.style.transform = 'translateY(0)'
        })

        // 等待一小段时间再显示下一个元素
        await new Promise(resolve => setTimeout(resolve, 50))
      }
    },

    async handleSubmit() {
      if (!this.formData.resume.trim() && !this.pdfFile) {
        alert('请输入简历内容或上传PDF文件')
        return
      }

      if (!this.formData.job.trim()) {
        alert('请输入目标职位信息')
        return
      }

      this.loading = true
      this.showResult = false
      this.markdownContent = ''
      
      try {
        let resumeContent = this.formData.resume
        
        if (this.pdfFile) {
          const formData = new FormData()
          formData.append('file', this.pdfFile)
          
          try {
            const response = await this.$axios.post('/api/extract-pdf', formData, {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            })
            
            if (response.data && response.data.content) {
              resumeContent = response.data.content
              // 保存提取的文本内容
              this.formData.resume = resumeContent
            } else {
              throw new Error('PDF解析结果为空')
            }
          } catch (error) {
            console.error('PDF解析失败:', error)
            const errorMessage = error.response?.data?.message || error.message || '未知错误'
            alert('PDF解析失败：' + errorMessage)
            this.loading = false
            return
          }
        }

        try {
          const response = await this.$axios.post('/api/analyze-dify', {
            resume: resumeContent,
            job: this.formData.job
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

          // 跳转到报告页面
          this.$router.push({
            name: 'report',
            params: { report: content }
          })

        } catch (error) {
          console.error('分析过程出错:', error)
          alert('分析过程出错：' + (error.response?.data?.message || error.message))
        }
      } catch (error) {
        console.error('分析过程出错:', error)
        alert('分析过程出错：' + error.message)
      } finally {
        this.loading = false
      }
    },

    isCompleteBlock(text) {
      // 检查是否是完整的内容块
      const lines = text.split('\n');
      const lastLine = lines[lines.length - 1];
      
      // 检查是否是标题行
      if (lastLine.match(/^#{1,6}\s.*$/)) {
        return true;
      }
      
      // 检查是否是列表项（包括特殊标记）
      const listItemPattern = /^[-*+]\s.*$|^\d+\.\s.*$/;
      if (listItemPattern.test(lastLine)) {
        // 如果是列表项，确保它是完整的句子
        return lastLine.trim().endsWith('。') || 
               lastLine.trim().endsWith('！') || 
               lastLine.trim().endsWith('？') ||
               lastLine.trim().endsWith('.') || 
               lastLine.trim().endsWith('!') || 
               lastLine.trim().endsWith('?');
      }
      
      // 检查是否是完整的句子
      if (lastLine.trim().endsWith('。') || 
          lastLine.trim().endsWith('！') || 
          lastLine.trim().endsWith('？') ||
          lastLine.trim().endsWith('.') || 
          lastLine.trim().endsWith('!') || 
          lastLine.trim().endsWith('?')) {
        return true;
      }
      
      // 检查是否有段落分隔符
      if (text.endsWith('\n\n')) {
        return true;
      }
      
      return false;
    }
  }
}
</script>

<style>
@media print {
  .container {
    max-width: none !important;
    padding: 0 !important;
    background: white !important;
    color: black !important;
  }
  
  button {
    display: none !important;
  }

  .markdown-body {
    background: white !important;
    color: black !important;
  }
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto;
  border: 3px solid #374151;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.stream-block {
  color: #e5e7eb;
  margin-bottom: 1rem;
  transition: opacity 0.2s ease, transform 0.2s ease;
  transform: translateY(10px);
  display: block;
  width: 100%;
  max-width: 100%;
}

.stream-block p,
.stream-block li,
.stream-block h1,
.stream-block h2,
.stream-block h3,
.stream-block h4,
.stream-block h5,
.stream-block h6 {
  white-space: pre-line !important;
  text-align: left !important;
  word-break: normal !important;
  overflow-wrap: anywhere !important;
  width: 100% !important;
  max-width: 100% !important;
  padding-right: 1rem !important;
}

/* 调整报告内容容器样式 */
.report-content {
  /* padding: 1.5rem; */
  background-color: #1f2937;
  /* border: 1px solid #374151; */
  font-size: 16px;
  line-height: 1.8;
  color: #e5e7eb;
  overflow: auto;
  word-wrap: break-word;
  white-space: normal;
}

.report-content h1,
.report-content h2,
.report-content h3,
.report-content h4,
.report-content h5,
.report-content h6 {
  color: #f3f4f6;
  margin: 1.5em 0 0.5em;
  line-height: 1.4;
}

.report-content p {
  margin: 0.8em 0;
  line-height: 1.8;
}

.report-content ul,
.report-content ol {
  margin: 1em 0;
  padding-left: 0.5em;
}

.report-content li {
  margin: 0.5em 0;
  padding-left: 1.2em;
}

/* 移除可能影响文本显示的样式 */
.stream-content,
.markdown-body,
.prose {
  white-space: pre-line !important;
  word-break: normal !important;
  overflow-wrap: anywhere !important;
  width: 100% !important;
  max-width: 100% !important;
}

/* 确保列表正确显示 */
.stream-block ul,
.stream-block ol,
.report-content ul,
.report-content ol {
  padding-left: 1rem;
  margin: 0.5rem 0;
  width: calc(100% - 1rem);
}

/* 调整代码块样式 */
.stream-block pre,
.report-content pre {
  white-space: pre-wrap !important;
  word-wrap: break-word !important;
  overflow-x: auto;
  max-width: 100%;
  margin: 1rem 0;
  padding: 1rem;
  background-color: #1f2937;
  border-radius: 0.375rem;
}

/* 移除之前的冲突样式 */
.stream-content {
  display: none;
}

/* 确保内容在容器内正确显示 */
.container {
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  padding: 0 1rem;
}

/* 调整分析结果容器样式 */
.mt-8.bg-gray-800 {
  background-color: #1a202c;
  padding: 1.5rem;
}

/* 拖拽上传区域样式 */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

/* 暗黑模式下的错误提示样式 */
.bg-red-50 {
  @apply bg-red-900 bg-opacity-20;
}

.text-red-700 {
  @apply text-red-400;
}

.text-red-600 {
  @apply text-red-300;
}

/* 暗黑模式下的 Markdown 样式调整 */
.prose-invert {
  --tw-prose-body: #e5e7eb;
  --tw-prose-headings: #f3f4f6;
  --tw-prose-links: #60a5fa;
  --tw-prose-links-hover: #93c5fd;
  --tw-prose-underline: #6b7280;
  --tw-prose-underline-hover: #9ca3af;
  --tw-prose-bold: #f3f4f6;
  --tw-prose-counters: #9ca3af;
  --tw-prose-bullets: #4b5563;
  --tw-prose-hr: #374151;
  --tw-prose-quote-borders: #4b5563;
  --tw-prose-captions: #9ca3af;
  --tw-prose-code: #f3f4f6;
  --tw-prose-code-bg: #374151;
  --tw-prose-pre-code: #e5e7eb;
  --tw-prose-pre-bg: #1f2937;
  --tw-prose-pre-border: #374151;
  --tw-prose-th-borders: #4b5563;
  --tw-prose-td-borders: #374151;
}

.markdown-body {
  color: #e5e7eb !important;
  font-size: 1rem;
  line-height: 1.6;
}

.stream-block {
  opacity: 0;
  animation: fadeIn 0.3s ease-in forwards;
}

.stream-content {
  color: #e5e7eb;
  white-space: pre-wrap;
  word-wrap: break-word;
  margin-bottom: 0.5rem;
}

.stream-content h1,
.stream-content h2,
.stream-content h3,
.stream-content h4,
.stream-content h5,
.stream-content h6 {
  color: #f3f4f6;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.stream-content p {
  margin-bottom: 0.75rem;
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.stream-content ul,
.stream-content ol {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
}

.stream-content li {
  margin-bottom: 0.25rem;
  line-height: 1.6;
}

/* 移除多余的空白 */
.prose {
  margin-top: 0 !important;
}

.prose > :first-child {
  margin-top: 0 !important;
}

.prose > :last-child {
  margin-bottom: 0 !important;
}

/* 确保列表项正确显示 */
.prose ul > li,
.prose ol > li {
  margin: 0;
  padding: 0;
}

/* 调整标题间距 */
.prose h1,
.prose h2,
.prose h3,
.prose h4 {
  margin-top: 1.8em;
  margin-bottom: 1em;
}

/* 调整段落间距 */
.prose p {
  margin: 0.8em 0;
}

/* 添加过渡效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.report-content {
  color: #e5e7eb;
  font-size: 16px;
  line-height: 1.8;
  letter-spacing: 0.3px;
}

.report-content h1,
.report-content h2,
.report-content h3,
.report-content h4,
.report-content h5,
.report-content h6 {
  color: #f3f4f6;
  margin: 1.8em 0 1em;
  line-height: 1.4;
}

.report-content h1 { font-size: 1.4em; }
.report-content h2 { font-size: 1.2em; }
.report-content h3 { font-size: 1.1em; }

.report-content p {
  margin: 0.8em 0;
  line-height: 1.8;
  text-align: left;
  white-space: normal;
}

.report-content ul,
.report-content ol {
  margin: 1rem 0;
  padding-left: 1rem;
}

.report-content li {
  margin: 0.5rem 0;
  line-height: 1.8;
  text-align: left;
}

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

/* 移除之前的样式 */
.stream-block,
.stream-content {
  display: block;
  opacity: 1;
  animation: none;
}

.markdown-body {
  max-width: none;
  width: 100%;
}

/* 确保内容正确显示 */
.prose {
  max-width: none;
  width: 100%;
}

.prose p {
  margin: 1em 0;
  line-height: 1.6;
}

.prose > * + * {
  margin-top: 0;
}

/* 重置所有可能影响文本显示的样式 */
.stream-block,
.report-content,
.markdown-body,
.prose {
  /* all: initial; */
  font-family: system-ui, -apple-system, sans-serif;
  color: #e5e7eb;
  width: 100%;
  display: block;
}

/* 基础文本样式 */
.stream-block {
  margin-bottom: 1rem;
  transition: opacity 0.2s ease, transform 0.2s ease;
  transform: translateY(10px);
}

/* 段落样式 */
.stream-block p,
.report-content p {
  margin: 0.75rem 0;
  line-height: 1.6;
  display: block;
  white-space: normal;
  text-align: left;
}

/* 标题样式 */
.stream-block h1,
.stream-block h2,
.stream-block h3,
.stream-block h4,
.stream-block h5,
.stream-block h6,
.report-content h1,
.report-content h2,
.report-content h3,
.report-content h4,
.report-content h5,
.report-content h6 {
  color: #f3f4f6;
  margin: 1rem 0 0.5rem;
  line-height: 1.4;
  font-weight: bold;
  display: block;
}

/* 列表样式 */
.stream-block ul,
.stream-block ol,
.report-content ul,
.report-content ol {
  margin: 0.75rem 0;
  padding-left: 1rem;
  display: block;
}

.stream-block li,
.report-content li {
  margin: 0.25rem 0;
  line-height: 1.6;
  display: list-item;
}

/* 代码块样式 */
.stream-block pre,
.report-content pre {
  margin: 1rem 0;
  padding: 1rem;
  background-color: #1f2937;
  border-radius: 0.375rem;
  overflow-x: auto;
  display: block;
}

.stream-block code,
.report-content code {
  background-color: #374151;
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-family: monospace;
}

/* 移除所有冲突的样式 */
.stream-block *,
.report-content * {
  white-space: normal !important;
  word-break: normal !important;
  overflow-wrap: break-word !important;
}

/* 容器样式 */
.report-content {
  /* padding: 1.5rem; */
  background-color: #1f2937;
  /* border: 1px solid #374151; */
  font-size: 16px;
  line-height: 1.8;
  color: #e5e7eb;
  overflow: auto;
  word-wrap: break-word;
  white-space: normal;
}

/* 动画相关 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 重置基础样式 */
.report-content {
  font-family: system-ui, -apple-system, sans-serif;
  color: #e5e7eb;
  line-height: 1.6;
  font-size: 16px;
  padding: 2rem;
  background-color: #1f2937;
  border-radius: 0.5rem;
}

/* Markdown 样式优化 */
.markdown-heading {
  margin: 0.5em 0 0.3em;
}

.markdown-heading:first-child {
  margin-top: 0.5em;
}

h1.markdown-heading { 
  font-size: 1.4em; 
  color: #f3f4f6;
  font-weight: bold;
  padding-bottom: 0.5em;
  border-bottom: 1px solid #4b5563;
}

h2.markdown-heading { 
  font-size: 1.2em;
  color: #e5e7eb;
  margin-top: 1.5em;
}

h3.markdown-heading { 
  font-size: 1.1em;
  color: #d1d5db;
  margin-top: 1.2em;
}

.markdown-paragraph {
  margin: 1em 0;
  line-height: 1.6;
}

.markdown-paragraph:not(:last-child) {
  margin-bottom: 1.2em;
}

.markdown-list {
  margin: 1em 0;
  padding-left: 1.5em;
}

.markdown-list-item {
  margin: 0.5em 0;
  padding-left: 1.2em;
}

.markdown-list-item::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #60a5fa;
  font-size: 1em;
}

pre {
  background-color: #1f2937;
  padding: 1rem;
  border-radius: 0.375rem;
  overflow-x: auto;
  margin: 1rem 0;
}

code {
  background-color: #374151;
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-size: 0.875em;
}

blockquote {
  border-left: 4px solid #374151;
  padding-left: 1em;
  color: #9ca3af;
  margin: 0.8em 0;
}

/* 优化列表样式 */
ol.markdown-list {
  list-style-type: decimal;
  padding-left: 1.8em;
}

ol.markdown-list .markdown-list-item::before {
  display: none;
}

ol.markdown-list .markdown-list-item {
  padding-left: 0.2em;
}

/* 调整标题间距 */
.markdown-heading + .markdown-paragraph,
.markdown-heading + .markdown-list {
  margin-top: 0.3em;
}

/* 优化文本对齐和间距 */
.stream-block *,
.report-content * {
  text-align: left;
}

/* 流式输出优化 */
.stream-block {
  opacity: 1;
  transform: none;
  margin-bottom: 0.5em;
}

.stream-content {
  display: block;
  margin-bottom: 0.5em;
}

/* 移除多余的空白和装饰 */
.markdown-list::before {
  display: none;
}

.markdown-paragraph::after {
  display: none;
}

/* 调整内容容器 */
.mt-8.bg-gray-800 {
  background-color: #1a202c;
  padding: 1.5rem;
}

/* 优化标题和段落的间距 */
.prose h1,
.prose h2,
.prose h3,
.prose h4 {
  margin-top: 1.8em;
  margin-bottom: 1em;
}

.prose p {
  margin: 0.8em 0;
}

/* 调整文本行高和字间距 */
.report-content,
.markdown-paragraph,
.markdown-list-item {
  font-size: 16px;
  line-height: 1.8;
  letter-spacing: 0.3px;
}

/* 优化标记符号 */
.markdown-list-item::before {
  top: -1px;
}

/* 调整容器背景和边框 */
.report-content {
  background-color: #1a202c;
  /* border: 1px solid #374151; */
}

/* 打印样式优化 */
@media print {
  .report-content {
    background: white;
    color: black;
    padding: 1.5rem;
    border: none;
  }
  
  .markdown-heading {
    color: #1f2937;
  }
  
  h1.markdown-heading { 
    color: #1f2937;
    border-bottom-color: #9ca3af;
  }
  
  h2.markdown-heading { color: #374151; }
  h3.markdown-heading { color: #4b5563; }
  
  .markdown-paragraph {
    color: #4b5563;
  }
  
  .markdown-list-item {
    color: #4b5563;
  }
  
  .markdown-list-item::before {
    color: #2563eb;
  }
  
  .markdown-paragraph strong {
    color: #2563eb;
  }
  
  .markdown-paragraph em {
    color: #6b7280;
  }
}
</style> 
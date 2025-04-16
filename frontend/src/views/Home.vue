<template>
  <div class="min-h-screen bg-gray-900 py-8">
    <div class="container mx-auto px-4 max-w-7xl">
      <h1 class="text-3xl font-bold text-gray-100 mb-8">简历匹配度分析</h1>
      <!-- <p class="text-gray-400 mb-8">请先填写您的工作经历，例位描述等，AI会根据您的经历定制化您的简历，可提升面试几率。</p> -->
      
      <!-- 简历和职位信息区域 -->
      <transition name="slide-fade" mode="out-in">
        <div v-show="!showReport" class="grid grid-cols-1 md:grid-cols-2 gap-6">
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
      </transition>

      <!-- 分析结果 -->
      <transition name="slide-fade" mode="out-in">
        <div v-show="showReport" class="mt-8 bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-700">
          <!-- <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-100">分析报告</h2>
          </div> -->
          <div v-if="!markdownContent" class="flex flex-col items-center justify-center py-12">
            <div class="tech-loader">
              <div class="tech-loader-inner">
                <div class="tech-loader-line"></div>
                <div class="tech-loader-line"></div>
                <div class="tech-loader-line"></div>
                <div class="tech-loader-line"></div>
                <div class="tech-loader-line"></div>
              </div>
              <div class="tech-loader-text">正在生成报告</div>
              <div class="tech-loader-dots">
                <span>.</span>
                <span>.</span>
                <span>.</span>
              </div>
            </div>
          </div>
          <StreamingMarkdown v-else :content="markdownContent" class="report-content" />
        </div>
      </transition>

      <!-- 底部按钮区域 -->
      <div class="mt-8 flex justify-center">
        <transition name="fade" mode="out-in">
          <button
            v-if="!showResult"
            @click="handleSubmit"
            :disabled="loading"
            class="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300"
            :class="{ 'opacity-50 cursor-not-allowed': loading }"
          >
            <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ loading ? '分析中...' : '开始分析' }}
          </button>
          <button
            v-else
            @click="toggleView"
            class="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300"
          >
            {{ showReport ? '返回简历' : '查看报告' }}
          </button>
        </transition>
      </div>

      <!-- 加载动画 -->
      <transition name="fade">
        <div v-if="loading || isProcessing" class="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center z-50">
          <div class="bg-gray-800 p-8 rounded-lg shadow-xl border border-gray-700 transform transition-all duration-500">
            <div class="flex flex-col items-center">
              <div class="tech-spinner mb-4">
                <div class="tech-spinner-inner">
                  <div class="tech-spinner-circle"></div>
                  <div class="tech-spinner-circle"></div>
                  <div class="tech-spinner-circle"></div>
                  <div class="tech-spinner-circle"></div>
                  <div class="tech-spinner-circle"></div>
                </div>
                <div class="tech-spinner-text">AI 分析中</div>
              </div>
              <div class="text-gray-300 text-lg">{{ loadingText }}</div>
              <div class="mt-4 text-sm text-gray-400">
                <div class="tech-dots">
                  <span>.</span>
                  <span>.</span>
                  <span>.</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import StreamingMarkdown from '@/components/StreamingMarkdown.vue'

export default {
  name: 'Home',
  components: {
    StreamingMarkdown
  },
  
  created() {
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
      isProcessing: false,
      showReport: false
    }
  },

  computed: {
    loadingText() {
      if (this.loading) {
        return '正在分析中，请稍候...'
      } else if (this.isProcessing) {
        return '正在处理中，请稍候...'
      }
      return ''
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
      this.markdownContent = ''
      this.lastContent = ''
    },

    printReport() {
      window.print()
    },

    toggleView() {
      this.showReport = !this.showReport
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

        // 保存表单数据到 localStorage
        localStorage.setItem('formData', JSON.stringify(this.formData))

        // 创建 AbortController 用于取消请求
        const controller = new AbortController()
        
        try {
          const response = await fetch(`${this.$axios.defaults.baseURL}/api/analyze-dify`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              resume: resumeContent,
              job: this.formData.job
            }),
            signal: controller.signal
          })

          if (!response.ok) {
            throw new Error(`请求失败: ${response.status} ${response.statusText}`)
          }

          this.showResult = true
          this.loading = false
          this.showReport = true

          // 创建文本解码器
          const decoder = new TextDecoder()
          const reader = response.body.getReader()
          let buffer = ''
          let isReading = true

          while (isReading) {
            const { value, done } = await reader.read()
            if (done) {
              isReading = false
              break
            }

            // 解码新的数据块
            const chunk = decoder.decode(value, { stream: true })
            buffer += chunk

            // 处理完整的数据行
            const lines = buffer.split('\n')
            buffer = lines.pop() || ''

            for (const line of lines) {
              if (line.trim() && line.startsWith('data: ')) {
                try {
                  const data = JSON.parse(line.slice(6))
                  if (data.content) {
                    this.markdownContent += data.content
                  }
                } catch (e) {
                  console.error('解析响应数据失败:', e)
                }
              }
            }
          }

        } catch (error) {
          if (error.name === 'AbortError') {
            console.log('请求被取消')
          } else {
            throw error
          }
        }

      } catch (error) {
        console.error('分析过程出错:', error)
        alert('分析过程出错：' + (error.response?.data?.message || error.message))
      } finally {
        this.loading = false
      }
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
  width: 50px;
  height: 50px;
  border: 4px solid #374151;
  border-top: 4px solid #3b82f6;
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

/* 添加切换按钮的过渡效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 优化切换按钮样式 */
.toggle-button {
  transition: all 0.3s ease;
}

.toggle-button:hover {
  transform: translateY(-1px);
}

/* 确保内容切换时的平滑过渡 */
.grid {
  transition: opacity 0.3s ease;
}

.grid.hidden {
  opacity: 0;
}

/* 添加过渡动画效果 */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 500ms;
}

.duration-500 {
  transition-duration: 500ms;
}

.ease-in-out {
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* 添加缩放动画 */
.scale-110 {
  transform: scale(1.1);
}

/* 优化报告内容过渡 */
.report-content {
  transition: opacity 0.5s ease-in-out;
}

/* 添加淡入淡出效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 优化内容切换动画 */
.grid {
  transition: all 0.5s ease-in-out;
}

.grid.hidden {
  opacity: 0;
  transform: translateY(-20px);
}

/* 优化报告容器动画 */
.mt-8.bg-gray-800 {
  transition: all 0.5s ease-in-out;
}

.mt-8.bg-gray-800.hidden {
  opacity: 0;
  transform: translateY(-20px);
}

/* 淡入淡出动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 滑动淡入淡出动画 */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* 按钮过渡效果 */
button {
  transition: all 0.3s ease;
}

button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

button:active:not(:disabled) {
  transform: translateY(0);
}

/* 内容区域过渡效果 */
.grid,
.mt-8.bg-gray-800 {
  transition: all 0.3s ease-in-out;
}

.report-content {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 科技感加载动画 */
.tech-spinner {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto;
}

.tech-spinner-inner {
  position: relative;
  width: 100%;
  height: 100%;
}

.tech-spinner-circle {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 2px solid transparent;
  border-radius: 50%;
  animation: tech-spin 2s linear infinite;
}

.tech-spinner-circle:nth-child(1) {
  border-top-color: #3b82f6;
  animation-delay: 0s;
}

.tech-spinner-circle:nth-child(2) {
  border-right-color: #3b82f6;
  animation-delay: 0.5s;
}

.tech-spinner-circle:nth-child(3) {
  border-bottom-color: #3b82f6;
  animation-delay: 1s;
}

.tech-spinner-circle:nth-child(4) {
  border-left-color: #3b82f6;
  animation-delay: 1.5s;
}

.tech-spinner-circle:nth-child(5) {
  border-color: #3b82f6;
  border-style: dashed;
  animation-delay: 2s;
}

.tech-spinner-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #3b82f6;
  font-size: 14px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.tech-dots {
  display: inline-block;
}

.tech-dots span {
  display: inline-block;
  animation: tech-dots 1.4s infinite;
}

.tech-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.tech-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes tech-spin {
  0% {
    transform: rotate(0deg);
    opacity: 0.2;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: rotate(360deg);
    opacity: 0.2;
  }
}

@keyframes tech-dots {
  0%, 100% {
    opacity: 0.2;
    transform: translateY(0);
  }
  50% {
    opacity: 1;
    transform: translateY(-5px);
  }
}

/* 添加科技感背景效果 */
.tech-spinner::before {
  content: '';
  position: absolute;
  top: -10px;
  left: -10px;
  right: -10px;
  bottom: -10px;
  background: linear-gradient(45deg, transparent, rgba(59, 130, 246, 0.1), transparent);
  border-radius: 50%;
  animation: tech-glow 2s linear infinite;
}

@keyframes tech-glow {
  0% {
    transform: rotate(0deg);
    opacity: 0.2;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    transform: rotate(360deg);
    opacity: 0.2;
  }
}

/* 添加科技感边框动画 */
.bg-gray-800::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, #3b82f6, #60a5fa, #3b82f6);
  z-index: -1;
  border-radius: 0.5rem;
  animation: border-glow 2s linear infinite;
}

@keyframes border-glow {
  0% {
    opacity: 0.2;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 0.2;
  }
}

/* 科技感报告加载动画 */
.tech-loader {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 0 auto;
}

.tech-loader-inner {
  position: relative;
  width: 100%;
  height: 100%;
}

.tech-loader-line {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 2px solid transparent;
  border-radius: 50%;
  animation: tech-loader-spin 3s linear infinite;
}

.tech-loader-line:nth-child(1) {
  border-top-color: #3b82f6;
  animation-delay: 0s;
}

.tech-loader-line:nth-child(2) {
  border-right-color: #60a5fa;
  animation-delay: 0.6s;
}

.tech-loader-line:nth-child(3) {
  border-bottom-color: #93c5fd;
  animation-delay: 1.2s;
}

.tech-loader-line:nth-child(4) {
  border-left-color: #bfdbfe;
  animation-delay: 1.8s;
}

.tech-loader-line:nth-child(5) {
  border-color: #dbeafe;
  border-style: dashed;
  animation-delay: 2.4s;
}

.tech-loader-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #3b82f6;
  font-size: 16px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 2px;
  text-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
}

.tech-loader-dots {
  position: absolute;
  top: 60%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #60a5fa;
  font-size: 24px;
  font-weight: bold;
}

.tech-loader-dots span {
  display: inline-block;
  animation: tech-loader-dots 1.4s infinite;
}

.tech-loader-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.tech-loader-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes tech-loader-spin {
  0% {
    transform: rotate(0deg);
    opacity: 0.2;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: rotate(360deg);
    opacity: 0.2;
  }
}

@keyframes tech-loader-dots {
  0%, 100% {
    opacity: 0.2;
    transform: translateY(0);
  }
  50% {
    opacity: 1;
    transform: translateY(-5px);
  }
}

/* 添加科技感背景效果 */
.tech-loader::before {
  content: '';
  position: absolute;
  top: -15px;
  left: -15px;
  right: -15px;
  bottom: -15px;
  background: linear-gradient(45deg, transparent, rgba(59, 130, 246, 0.1), transparent);
  border-radius: 50%;
  animation: tech-loader-glow 3s linear infinite;
}

@keyframes tech-loader-glow {
  0% {
    transform: rotate(0deg);
    opacity: 0.2;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    transform: rotate(360deg);
    opacity: 0.2;
  }
}

/* 添加粒子效果 */
.tech-loader::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  animation: tech-loader-particles 3s linear infinite;
}

@keyframes tech-loader-particles {
  0% {
    transform: scale(1);
    opacity: 0.2;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.5;
  }
  100% {
    transform: scale(1);
    opacity: 0.2;
  }
}
</style>
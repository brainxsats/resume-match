<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container mx-auto px-4 max-w-7xl">
      <h1 class="text-3xl font-bold text-gray-800 mb-8">优化简历</h1>
      <p class="text-gray-600 mb-8">请先填写您的工作经历，例位描述等，AI会根据您的经历定制化您的简历，可提升面试几率。</p>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- 左侧：简历内容 -->
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                项目经历
                <span class="text-gray-400 text-xs ml-1">(0 / 350)</span>
              </label>
              <textarea
                v-model="formData.resume"
                class="w-full h-[600px] p-4 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                placeholder="请描述您最近的工作经历，项目经验，社会实践，实习"
              />
            </div>
            <div class="border-t border-gray-100 pt-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                上传PDF简历
              </label>
              <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg hover:border-gray-400 transition-colors">
                <div class="space-y-1 text-center">
                  <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                    <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4-4m4-4h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                  <div class="flex text-sm text-gray-600">
                    <label for="pdfFile" class="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500">
                      <span>上传文件</span>
                      <input
                        id="pdfFile"
                        ref="pdfFile"
                        type="file"
                        accept=".pdf"
                        class="sr-only"
                        @change="handleFileChange"
                      />
                    </label>
                    <p class="pl-1">或拖拽文件到此处</p>
                  </div>
                  <p class="text-xs text-gray-500">仅支持 PDF 格式</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：职位信息 -->
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                目标职位信息（选填）
                <span class="text-gray-400 text-xs ml-1">(0 / 350)</span>
              </label>
              <textarea
                v-model="formData.job"
                class="w-full h-[600px] p-4 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                placeholder="请输入目标职位的要求描述，AI 会帮您分析匹配度"
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
      <div v-if="loading" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg shadow-xl">
          <div class="spinner"></div>
          <div class="mt-4 text-gray-600">正在分析中，请稍候...</div>
        </div>
      </div>

      <!-- 分析结果 -->
      <div v-if="showResult" class="mt-8 bg-white rounded-lg shadow-sm p-6">
        <div class="flex justify-between items-center mb-6 pb-4 border-b">
          <h2 class="text-2xl font-bold text-gray-800">简历分析报告</h2>
          <div class="space-x-4">
            <button
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
              @click="resetForm"
            >
              重新分析
            </button>
            <button
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              @click="printReport"
            >
              打印报告
            </button>
          </div>
        </div>
        <div ref="reportContent" class="markdown-body prose max-w-none"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResumeAnalyzer',
  
  data() {
    return {
      formData: {
        resume: '',
        job: ''
      },
      loading: false,
      showResult: false,
      markdownContent: '',
      lastContent: ''
    }
  },

  methods: {
    handleFileChange(event) {
      const file = event.target.files[0]
      if (file && file.type === 'application/pdf') {
        this.pdfFile = file
      }
    },

    resetForm() {
      this.formData.resume = ''
      this.formData.job = ''
      this.$refs.pdfFile.value = ''
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
          currentSegment += (currentSegment ? '\n' : '') + line
        }
        else if (!line.trim()) {
          if (currentSegment.trim()) {
            segments.push(currentSegment.trim())
            currentSegment = ''
          }
        }
        else {
          currentSegment += (currentSegment ? '\n' : '') + line
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
      const segments = this.processStreamContent(content)
      for (const segment of segments) {
        if (segment.trim()) {
          const htmlContent = this.$marked(segment)
          const block = this.createStreamBlock(htmlContent)
          container.appendChild(block)
          
          block.querySelectorAll('pre code').forEach((codeBlock) => {
            hljs.highlightBlock(codeBlock)
          })

          this.smoothScrollToElement(block)
          
          await new Promise(resolve => setTimeout(resolve, 100))
        }
      }
    },

    async handleSubmit() {
      if (!this.formData.resume.trim() && !this.pdfFile) {
        alert('请输入简历内容或上传PDF文件')
        return
      }

      this.loading = true
      this.showResult = false
      const reportContent = this.$refs.reportContent
      reportContent.innerHTML = ''
      
      try {
        let resumeContent = this.formData.resume
        
        if (this.pdfFile) {
          const formData = new FormData()
          formData.append('file', this.pdfFile)
          
          const { data } = await this.$axios.post('/api/extract-pdf', formData)
          resumeContent = data.content
        }

        const response = await this.$axios.post('/api/analyze-dify', {
          resume: resumeContent,
          job: this.formData.job
        }, {
          responseType: 'stream'
        })

        this.showResult = true
        this.loading = false
        this.markdownContent = ''
        this.lastContent = ''

        const reader = response.data.getReader()
        const decoder = new TextDecoder()

        while (true) {
          const { value, done } = await reader.read()
          if (done) break
          
          const text = decoder.decode(value)
          const lines = text.split('\n')
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6))
                if (data.content) {
                  this.markdownContent += data.content
                  
                  const newContent = this.markdownContent.slice(this.lastContent.length)
                  if (newContent.trim()) {
                    await this.displayContentWithDelay(newContent, reportContent)
                    this.lastContent = this.markdownContent
                  }
                }
              } catch (e) {
                console.error('解析响应数据失败:', e)
              }
            }
          }
        }

        if (!this.markdownContent.trim()) {
          throw new Error('分析结果为空，请重试')
        }

      } catch (error) {
        this.showResult = true
        reportContent.innerHTML = `
          <div class="bg-red-50 p-4 rounded-lg">
            <h2 class="text-xl font-semibold text-red-700">错误</h2>
            <div class="mt-2 text-red-600">分析过程中出现错误：${error.message}</div>
          </div>
        `
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
  }
  
  button {
    display: none !important;
  }
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
</style> 
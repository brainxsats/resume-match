<template>
  <div class="streaming-markdown">
    <div ref="markdownContainer" class="markdown-content">
      <div v-for="(block, index) in contentBlocks" :key="index" class="stream-block">
        <div v-html="renderMarkdown(block)"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked'
import hljs from 'highlight.js'

export default {
  name: 'StreamingMarkdown',
  
  props: {
    content: {
      type: String,
      default: ''
    }
  },

  data() {
    return {
      contentBlocks: [],
      lastContent: '',
      isProcessing: false
    }
  },

  watch: {
    content: {
      handler(newContent) {
        if (newContent !== this.lastContent) {
          this.processContent(newContent)
        }
      },
      immediate: true
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
  },

  methods: {
    async processContent(content) {
      if (this.isProcessing) return
      
      this.isProcessing = true
      try {
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
        
        this.contentBlocks = segments
        this.lastContent = content
        
        // 滚动到最新内容
        this.$nextTick(() => {
          const container = this.$refs.markdownContainer
          if (container) {
            container.scrollTop = container.scrollHeight
          }
        })
      } finally {
        this.isProcessing = false
      }
    },

    renderMarkdown(content) {
      return marked(content)
    }
  }
}
</script>

<style>
.streaming-markdown {
  width: 100%;
  height: 100%;
  overflow-y: auto;
}

.markdown-content {
  padding: 1rem;
}

.stream-block {
  opacity: 0;
  animation: fadeIn 0.3s ease-in forwards;
  margin-bottom: 1rem;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Markdown 样式 */
.markdown-content h1 {
  font-size: 1.4em;
  color: #f3f4f6;
  font-weight: bold;
  padding-bottom: 0.5em;
  border-bottom: 1px solid #4b5563;
  margin: 1.5em 0 1em;
}

.markdown-content h2 {
  font-size: 1.2em;
  color: #e5e7eb;
  margin-top: 1.5em;
  margin-bottom: 0.8em;
}

.markdown-content h3 {
  font-size: 1.1em;
  color: #d1d5db;
  margin-top: 1.2em;
  margin-bottom: 0.6em;
}

.markdown-content p {
  margin: 0.8em 0;
  line-height: 1.6;
}

.markdown-content ul,
.markdown-content ol {
  margin: 0.8em 0;
  padding-left: 1.5em;
}

.markdown-content li {
  margin: 0.4em 0;
  line-height: 1.6;
}

.markdown-content pre {
  background-color: #1f2937;
  padding: 1rem;
  border-radius: 0.375rem;
  overflow-x: auto;
  margin: 1rem 0;
}

.markdown-content code {
  background-color: #374151;
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-size: 0.875em;
}

.markdown-content blockquote {
  border-left: 4px solid #374151;
  padding-left: 1em;
  color: #9ca3af;
  margin: 0.8em 0;
}

/* 代码块样式 */
.markdown-content pre code {
  background-color: transparent;
  padding: 0;
  font-size: 0.9em;
  line-height: 1.5;
}

/* 列表样式优化 */
.markdown-content ul {
  list-style-type: disc;
}

.markdown-content ol {
  list-style-type: decimal;
}

/* 链接样式 */
.markdown-content a {
  color: #60a5fa;
  text-decoration: underline;
  text-decoration-style: dashed;
}

.markdown-content a:hover {
  color: #93c5fd;
}

/* 表格样式 */
.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
}

.markdown-content th,
.markdown-content td {
  border: 1px solid #374151;
  padding: 0.5em;
  text-align: left;
}

.markdown-content th {
  background-color: #1f2937;
  font-weight: bold;
}

/* 图片样式 */
.markdown-content img {
  max-width: 100%;
  height: auto;
  border-radius: 0.375rem;
  margin: 1em 0;
}

/* 打印样式 */
@media print {
  .markdown-content {
    background: white;
    color: black;
  }
  
  .markdown-content h1 {
    color: #1f2937;
    border-bottom-color: #9ca3af;
  }
  
  .markdown-content h2 {
    color: #374151;
  }
  
  .markdown-content h3 {
    color: #4b5563;
  }
  
  .markdown-content p,
  .markdown-content li {
    color: #4b5563;
  }
  
  .markdown-content a {
    color: #2563eb;
  }
  
  .markdown-content pre {
    background-color: #f3f4f6;
    border: 1px solid #e5e7eb;
  }
  
  .markdown-content code {
    background-color: #f3f4f6;
  }
}
</style> 
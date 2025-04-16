<template>
  <div class="report-container">
    <div ref="reportContent" class="report-content"></div>
  </div>
</template>

<script>
import { marked } from 'marked'
import hljs from 'highlight.js'

export default {
  name: 'Report',

  props: {
    content: {
      type: String,
      default: ''
    },
    animate: {
      type: Boolean,
      default: true
    }
  },

  data() {
    return {
      isAnimating: false,
      markdownContent: '',
      lastContent: ''
    }
  },

  watch: {
    content: {
      immediate: true,
      handler(newContent) {
        if (newContent) {
          this.$nextTick(() => {
            if (this.animate) {
              this.animateContent(newContent)
            } else {
              this.displayContent(newContent)
            }
          })
        }
      }
    }
  },

  created() {
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
    processContent(content) {
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

    displayContent(content) {
      if (!content || !this.$refs.reportContent) return

      const container = this.$refs.reportContent
      container.innerHTML = ''

      const segments = this.processContent(content)
      const allContent = segments.map(segment => {
        const htmlContent = marked(segment)
        const element = document.createElement('div')
        element.innerHTML = htmlContent
        
        const children = Array.from(element.children)
        if (children.length > 0) {
          children.forEach(child => {
            this.applyStyles(child)
          })
        } else {
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

    async animateContent(content) {
      if (!content || this.isAnimating || !this.$refs.reportContent) return

      this.isAnimating = true
      const container = this.$refs.reportContent
      container.innerHTML = ''

      const segments = this.processContent(content)
      for (const segment of segments) {
        const htmlContent = marked(segment)
        const element = document.createElement('div')
        element.innerHTML = htmlContent
        element.style.opacity = '0'
        
        const children = Array.from(element.children)
        if (children.length > 0) {
          children.forEach(child => {
            this.applyStyles(child)
          })
        } else {
          const p = document.createElement('p')
          p.className = 'markdown-paragraph'
          p.innerHTML = htmlContent
          element.innerHTML = ''
          element.appendChild(p)
        }
        
        container.appendChild(element)
        await new Promise(resolve => setTimeout(resolve, 50))
        element.style.transition = 'opacity 0.3s ease-in-out'
        element.style.opacity = '1'
      }

      this.isAnimating = false
    },

    applyStyles(element) {
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
          } else if (text.startsWith('⭐')) {
            item.style.color = '#60A5FA'
            item.style.listStyleType = 'none'
          }
        })
      }
    }
  }
}
</script>

<style scoped>
.report-container {
  color: #e5e7eb;
  font-size: 16px;
  line-height: 1.8;
  letter-spacing: 0.3px;
}

.report-content {
  color: inherit;
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
  position: relative;
}
</style> 
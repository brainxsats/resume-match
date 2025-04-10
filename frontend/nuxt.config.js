export default {
  // Global page headers
  head: {
    title: '简历职位匹配分析',
    htmlAttrs: {
      lang: 'zh'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '简历职位匹配分析系统' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      { rel: 'stylesheet', href: 'https://cdn.jsdelivr.net/npm/highlight.js@11.7.0/styles/github.min.css' }
    ],
    script: [
      { src: 'https://cdn.jsdelivr.net/npm/marked/marked.min.js' },
      { src: 'https://cdn.jsdelivr.net/npm/highlight.js@11.7.0/lib/highlight.min.js' }
    ]
  },

  // Global CSS
  css: [
    '@/assets/css/main.css'
  ],

  // Plugins to run before rendering page
  plugins: [
    '@/plugins/marked.js'
  ],

  // Auto import components
  components: true,

  // Modules for dev and build
  buildModules: [
    '@nuxt/postcss8'
  ],

  // Modules
  modules: [
    '@nuxtjs/axios'
  ],

  // PostCSS configuration
  postcss: {
    plugins: {
      'tailwindcss': {},
      'autoprefixer': {},
    },
  },

  // Axios module configuration
  axios: {
    baseURL: process.env.API_BASE_URL || 'http://localhost:8000'
  },

  // Build Configuration
  build: {
    transpile: ['marked']
  },

  // Server configuration
  server: {
    host: '0.0.0.0',
    port: 3000
  }
} 
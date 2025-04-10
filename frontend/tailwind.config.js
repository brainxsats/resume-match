/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
  // 确保不会被 purge 掉需要的样式
  safelist: [
    'prose',
    'prose-sm',
    'prose-lg',
    'prose-xl',
    'markdown-body',
    'bg-gray-50',
    'bg-white',
    'bg-red-50',
    'text-gray-600',
    'text-gray-700',
    'text-gray-800',
    'text-red-600',
    'text-red-700',
  ]
} 
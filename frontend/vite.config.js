import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://backend:5000', // Instead of 127.0.0.1
        changeOrigin: true,
        secure: false,
      }
    }
  },
  resolve : {
    alias: {
      '@' : path.resolve(__dirname, './src')
    }
  }
})

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'https://indmoney-faq-api.onrender.com', // This will be your Render backend URL
        changeOrigin: true,
      }
    }
  },
  build: {
    outDir: './dist',
    assetsDir: 'assets',
    sourcemap: false,
    emptyOutDir: true
  }
})
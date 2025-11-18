import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'https://your-backend-url.com', // This will be replaced with your actual backend URL
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
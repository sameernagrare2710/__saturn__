import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),       // landing page → dist/index.html
        app:  resolve(__dirname, 'app/index.html'),   // React SPA   → dist/app/index.html
      },
    },
  },
})

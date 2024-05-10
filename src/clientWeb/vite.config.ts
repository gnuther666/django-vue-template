import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

let PORT =  8001
if (process.env.FRONT_WEB_PORT) {
  PORT = parseInt(process.env.FRONT_WEB_PORT)
}

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
  ],
  // include: [
  //   'src/*.ts',
  //   'src/*.vue',
  //   'src/**/*.ts',
  //   'src/**/*.vue',
  //   'src/**/**/*.vue',
  // ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0', // 绑定所有可用网络接口，包括本地IP和公网IP
    port: PORT, // 设置开发服务器运行在3000端口上
    watch: {
      usePolling: true
    },
  }
})

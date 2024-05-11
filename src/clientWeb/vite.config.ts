import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

const env = loadEnv('', process.cwd());

let PORT =  JSON.stringify(env.FRONT_WEB_PORT)
if (PORT) {
  PORT = parseInt(PORT)
} else {
  PORT = 8001
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
  },
  define: {
    VITE_BACKEND_PATH: JSON.stringify(env.BACKEND_PATH),
  }
})

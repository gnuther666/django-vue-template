<template>
  <div class="fullscreen-background">
    <div class="login_prj_title">
      <img src="@/assets/image/project_logo.png" alt="logo" class="login_prj_icon" />
      <p class="login_prj_title_text">全栈模板系统前台</p>
    </div>
    <div class="login_area">
      <el-form>
        <el-form-item label="账号">
          <el-input v-model="local_value.login_info.username" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input type="password" v-model="local_value.login_info.password" />
        </el-form-item>
        <el-form-item label="验证码" v-if="enable_verify()">
          <img :src="local_value.image_url" v-if="local_value.image_url" alt="Hexadecimal image" />
          <el-icon><RefreshRight /></el-icon>
          <el-input v-model="local_value.login_info.verify_input" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit" v-bind:disabled="!enable_login()"
            >登录</el-button
          >
          <el-button type="primary" @click="onSubmit">注册</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, nextTick } from 'vue'
import { getCaptcha, postLogin } from '../api'
import { useRouter } from 'vue-router'

const local_value = ref({
  login_info: {
    username: '',
    password: '',
    verify_key: '',
    verify_input: ''
  },
  image_hex: '',
  is_lock_captcha: false,
  image_url: '',
  access_token: '',
  refresh_token: '',
  out_username: ''
})

function enable_login() {
  if (
    local_value.value.login_info.username.length === 0 ||
    local_value.value.login_info.password.length === 0 ||
    local_value.value.login_info.verify_input.length === 0
  ) {
    return false
  }
  return true
}

function enable_verify() {
  if (
    local_value.value.login_info.username.length === 0 ||
    local_value.value.login_info.password.length === 0
  ) {
    return false
  }
  get_captcha()
  return true
}

function get_captcha() {
  if (local_value.value.is_lock_captcha) {
    return
  }
  getCaptcha().then((res) => {
    local_value.value.login_info.verify_key = res.data.key
    local_value.value.image_hex = res.data.image_hex
    local_value.value.image_url = hexToBlob(local_value.value.image_hex)
  })
  local_value.value.is_lock_captcha = true
  setTimeout(() => {
    local_value.value.is_lock_captcha = false
  }, 60 * 1000)
}

function hexToBlob(hexString) {
  // 将16进制字符串转换为字节数组
  var bytes = new Uint8Array(hexString.match(/.{2}/g).map((byte) => parseInt(byte, 16)))

  // 创建Blob对象
  var blob = new Blob([bytes], { type: 'image/png' })

  // 创建一个指向该Blob对象的URL
  return URL.createObjectURL(blob)
}
const router = useRouter()

const onSubmit = () => {
  const login_info = local_value.value.login_info
  console.log('接口返回数据', login_info)
  postLogin(login_info).then((res) => {
    local_value.value.access_token = res.data.access_token
    local_value.value.refresh_token = res.data.refresh_token
    local_value.value.out_username = res.data.username
    localStorage.setItem('access_token', local_value.value.access_token)
    localStorage.setItem('refresh_token', local_value.value.refresh_token)
    localStorage.setItem('out_username', local_value.value.out_username)
    nextTick(() => {
      console.log('已设置登录信息', localStorage.getItem('access_token'))
      router.push('/')
    })
  })
}
</script>
<style>
.fullscreen-background {
  height: 100vh; /* 确保元素高度等于视口高度 */
  width: 100vw; /* 确保元素宽度等于视口宽度 */
  position: absolute;
  left: 0;
  top: 0;
  background-image: url('@/assets/image/login_backend.png'); /* 替换为你的背景图片路径 */
  object-fit: fill;
  z-index: 0;
  overflow-x: hidden;
  overflow-y: hidden;
}
.login_prj_title {
  position: relative;
  top: 3%;
  left: 10%;
  z-index: 1;
  height: 6vh;
  line-height: 6vh;
  display: flex;
  align-items: center;
}
.login_prj_icon {
  height: 100%;
}
.login_prj_title_text {
  line-height: inherit;
  font-size: 40px;
  margin-left: 30px;
}
.login_area {
  position: absolute;
  right: 10%;
  top: 30%;
  border: #eeeeee solid 1px;
  background-color: rgba(255, 255, 229, 0.5);
  border-radius: 15px;
  padding: 20px;
}
</style>

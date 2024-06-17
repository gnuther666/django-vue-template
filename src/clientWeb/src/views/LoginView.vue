<template>
  <div class="fullscreen-background">
    <div class="top_title">
      <img src="@/assets/image/project_logo.png" alt="logo" class="login_prj_icon" />
      <p class="login_prj_text">djagno-vue-template</p>
    </div>
    <div class="login_area">
      <el-form :label-position="login_form_label_position">
        <el-form-item label="account" class="form_item" :label-width="60">
          <el-input v-model="local_value.login_info.username" />
        </el-form-item>
        <el-form-item label="password" class="form_item" :label-width="60">
          <el-input type="password" v-model="local_value.login_info.password" />
        </el-form-item>
        <el-form-item label="varify" v-if="is_need_capthca === 'base' && enable_verify " class="form_item" :label-width="60">
          <el-input v-model="local_value.login_info.verify_input" class="short_input" />
          <img :src="local_value.image_url" v-if="local_value.image_url" alt="Hexadecimal image" class="captcha_img"/>
          <el-icon>
            <RefreshRight />
          </el-icon>
          
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit" v-bind:disabled="!enable_login()">login</el-button>
          <el-button type="primary" @click="onSubmit">sing up</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, nextTick } from 'vue'
import { getCaptcha, postLogin } from '@/api/login'
import { useRouter } from 'vue-router'
import type { FormProps } from 'element-plus'

let is_need_capthca:string|undefine = ref(undefined)
if (import.meta.env.VITE_BACKEND_PATH == 'base'){
  is_need_capthca.value = 'base'
}


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

const login_form_label_position = ref<FormProps['labelPosition']>('right')
function enable_login() {
  if (
    local_value.value.login_info.username.length === 0 ||
    local_value.value.login_info.password.length === 0 
  ) {
    return false
  }
  if (is_need_capthca.value == 'base'){
    if (local_value.value.login_info.verify_input.length !== 4) {
      return false
    }
  }
  return true
}

function enable_verify() {
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
    if (local_value.value.image_hex) {
      let image_url = hexToBlob(local_value.value.image_hex)
      if (image_url) {
        local_value.value.image_url = image_url
      }
    }
  })
  local_value.value.is_lock_captcha = true
  setTimeout(() => {
    local_value.value.is_lock_captcha = false
  }, 60 * 1000)
}

function hexToBlob(hexString: string) {
  const matched_list = hexString.match(/.{2}/g)
  if (!matched_list) {
    console.log('get an empty hex str')
    return
  }
  // 将16进制字符串转换为字节数组
  var bytes = new Uint8Array(matched_list.map((byte: any) => parseInt(byte, 16)))

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
  height: 100vh;
  /* 确保元素高度等于视口高度 */
  width: 100vw;
  /* 确保元素宽度等于视口宽度 */
  position: absolute;
  left: 0;
  top: 0;
  background-image: url('@/assets/image/login_backend.png');
  /* 替换为你的背景图片路径 */
  object-fit: cover;
  background-repeat: no-repeat;
  background-size: cover;
  z-index: 0;
  overflow-x: hidden;
  overflow-y: hidden;
}


@media (max-width: 900px) {
  .top_title {
    width: 70vw;
    margin-top: 15vh;
    height: 6vh;
    position: absolute;
    top: 0vh;
    left: 20vw;
  }

  .login_prj_icon {
    height: 100%;
    position: absolute;
    left: 0px;
    top: 0px;
  }

  .login_prj_text {
    font-size: 1.5rem;
    position: absolute;
    margin-left: 10px;
    left: 40px;
    top: 0px;
  }

  .login_area {
    position: absolute;
    right: 5%;
    top: 40vh;
    width: 90vw;
    height: 40vh;
    border: #eeeeee solid 1px;
    background-color: rgba(255, 255, 229, 0.5);
    border-radius: 15px;
    padding: 20px;
  }

  .short_input {
    width: 20vw;
  }

  .captcha_img {
    width: 35vw;
    margin-left: 5vw;
  }

  .form_item {
  width: 80vw;
}

}

@media (min-width: 901px) {
  .top_title {
    width: 40vw;
    margin-top: 15vh;
    height: 6vh;
    position: absolute;
    top: 0vh;
    left: 15vw;
  }

  .login_prj_icon {
    height: 100%;
    position: absolute;
    left: 0px;
    top: 0px;
  }

  .login_prj_text {
    font-size: 1.8rem;
    position: absolute;
    margin-left: 10px;
    left: 40px;
    top: -5px;
  }

  .login_area {
    position: absolute;
    right: 10%;
    top: 30%;
    width: 30em;
    /* height: 20em; */
    border: #eeeeee solid 1px;
    background-color: rgba(255, 255, 229, 0.5);
    border-radius: 15px;
    padding: 20px;
  }

  .short_input {
    width: 5vw;
  }

  .captcha_img {
    width: 6vw;
    margin-left: 0.5vw;
  }
  
  .long_input {
  width: 80%;
}
}



</style>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const local_value = ref({
  is_login: false,
  username: '' as string|null
})

onMounted(() => {
  const token = localStorage.getItem('access_token')
  console.log('在用户组件里检查token', token)
  const username = localStorage.getItem('out_username')
  if (token) {
    local_value.value.username = username
    local_value.value.is_login = true
    console.log('查看设置的本地变量', local_value.value)
  } else {
    local_value.value.is_login = false
  }
})
</script>

<template>
  <div class="user_info">
    <div class="unlogin" v-if="!local_value.is_login">please click and login</div>
    <div class="loged" v-if="local_value.is_login" v-html="'Hellow,' + local_value.username"></div>
  </div>
</template>

<style>
</style>

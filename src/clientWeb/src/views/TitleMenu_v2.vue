<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import TopMenuUser from '@/views/TopMenuUser.vue'
import { is_mobile } from '@/util/isMobile'
const local_value = ref({
  activueIndex2: '1',
  logoutDialogVisible: false,
  menu_config: {
    menu_direction: 'horizontal',
    show_mobie_menu: false,
  }
})
const router = useRouter()
const use_router = ref(true)
function handleSelect(key: string, keyPath: string[]) {
  if (key.startsWith('ignore_')) {
    console.log('不做处理')
  } else {
    router.push(key)
  }
}

function confirmLogout() {
  // 确认退出登录的逻辑，例如清除token、跳转到登录页面等
  localStorage.removeItem('access_token') // 假设token存放在localStorage
  router.push('/login')
  local_value.value.logoutDialogVisible = false
}

function showLogoutConfirm(event: any) {
  // event.preventDefault() // 阻止默认行为（如果需要的话）
  console.log('退出登录')
  local_value.value.logoutDialogVisible = true
}

const updateMenuProps = () => {
  const is_moble_value = is_mobile(window.innerWidth);
  if (is_moble_value) {
    console.log('手机显示')
    local_value.value.menu_config.menu_direction = "vertical";
  } else {
    console.log('网页显示')
    local_value.value.menu_config.menu_direction = "horizontal";
  }
}

function onMobileMenuButtonClicked(event: any) {
  local_value.value.menu_config.show_mobie_menu = !local_value.value.menu_config.show_mobie_menu
}
const MobileDrawerDirection = ref<any>('ltr')
onMounted(() => {
  window.addEventListener('resize', updateMenuProps);
  window.addEventListener('load', updateMenuProps);
})

onUnmounted(() => {
  window.removeEventListener('resize', updateMenuProps);
  window.removeEventListener('load', updateMenuProps);
})
</script>

<template>
  <div class="base_page">
    <el-container>
      <el-header style="padding: 0" v-if="local_value.menu_config.menu_direction === 'horizontal'">
        <el-menu :default-active="$route.path" class="el-menu-demo" :router="use_router"
          :mode="local_value.menu_config.menu_direction" background-color="#545c64" text-color="#fff"
          active-text-color="#ffd04b" @select="handleSelect" flex>
          <div>
            <a href="/"><img src="@/assets/image/project_logo.png" class="homepage_logo" alt="" /><label
                style="margin-left: 10px; font-size: 20px; font-weight: bold; margin-right: 10px">django_vue_template</label></a>
          </div>
          <el-menu-item index="/">HomePage</el-menu-item>
          <el-menu-item index="/example">Example</el-menu-item>
          <el-menu-item index="/notebook">NoteBook</el-menu-item>
          <el-sub-menu index="ignore_submenu_1" style="position: absolute; right: 0"><template #title>
              <TopMenuUser />
            </template>
            <el-menu-item index="/user">UserCenter</el-menu-item>
            <el-menu-item index="/help">Help</el-menu-item>
            <el-menu-item index="/login" @click="showLogoutConfirm">Log Out</el-menu-item>
          </el-sub-menu>
        </el-menu></el-header>
      <el-main>
        <el-button type="primary" style="position: absolute;left: 0vw; top:0vh;"
          v-if="local_value.menu_config.menu_direction === 'vertical' && !local_value.menu_config.show_mobie_menu"
          @click="onMobileMenuButtonClicked"
        ><el-icon><Menu /></el-icon></el-button>
        <el-drawer v-if="local_value.menu_config.menu_direction === 'vertical' && local_value.menu_config.show_mobie_menu"
          v-model="local_value.menu_config.show_mobie_menu" :with-header="false" :direction="MobileDrawerDirection" size="60vw">
          <el-menu :default-active="$route.path" class="el-menu-demo" :router="use_router"
            :mode="local_value.menu_config.menu_direction"  @select="handleSelect" flex>
            <el-menu-item index="/">HomePage</el-menu-item>
            <el-menu-item index="/example">Example</el-menu-item>
            <el-menu-item index="/notebook">NoteBook</el-menu-item>
            <el-sub-menu index="ignore_submenu_1" ><template #title>
                <TopMenuUser />
              </template>
              <el-menu-item index="/user">UserCenter</el-menu-item>
              <el-menu-item index="/help">Help</el-menu-item>
              <el-menu-item index="/login" @click="showLogoutConfirm">Log out</el-menu-item>
            </el-sub-menu>
          </el-menu>
        </el-drawer>
        <RouterView />
      </el-main>
      <el-dialog title="makrsure you will logout" v-model="local_value.logoutDialogVisible" width="30%" append-to-body
        style="z-index: 99">
        <span>marksure you will logout?</span>
        <div slot="footer">
          <el-button @click="local_value.logoutDialogVisible = false">cancel</el-button>
          <el-button type="primary" @click="confirmLogout">sure</el-button>
        </div>
      </el-dialog>
    </el-container>
  </div>
</template>

<style>

</style>

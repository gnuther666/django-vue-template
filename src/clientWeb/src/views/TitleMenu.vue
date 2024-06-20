<template>
  <div class="flex h-screen">
    <div
      class="flex flex-col flex-shrink-0 w-1/5 min-w-36 max-w-40  bg-slate-200">
      <div class="h-40 bg-slate-300 border border-solid border-slate-400 border-b border-x-0 border-t-0">
        <img src="@/assets/image/project_logo.png"
          class="relative w-1/3 max-w-48 min-w-10 bg-gradient-to-b from-blue-500 to-red-500 rounded-lg left-12 top-6" title="prj_logo"
          alt="prj_log"
          @click="go_home"/>
        <div class="relative top-10 text-lg text-center text-zinc-950" @click="go_home">django vue template system</div>
      </div>
      <div class="flex flex-col flex-grow">
        <el-menu :key="local_value.menu_key" mode="vertical" @open="handleOpen" @close="handleClose" :default-active="default_url"
          :router="use_router" class="my_el_menu flex flex-col flex-grow" >
          <el-menu-item index="/">
            <el-icon><House /></el-icon>
            <span>HomePage</span>
          </el-menu-item>
          <el-menu-item index="/example">
            <el-icon><View /></el-icon>
            <span>example</span>
          </el-menu-item>
          <el-menu-item index="/notebook">
            <el-icon><Memo /></el-icon>
            <span>NoteBook</span>
          </el-menu-item>
          <div class="flex-grow" ></div>
          <el-sub-menu index="ignore_submenu_2"><template #title>
            <el-icon><Avatar /></el-icon>
            <span>Admin</span>
          </template>
            <el-menu-item index="/admin/permission">Permission</el-menu-item>
          </el-sub-menu>
          <el-sub-menu index="ignore_submenu_1"><template #title>
              <TopMenuUser />
            </template>
            <el-menu-item index="/user">UserCenter</el-menu-item>
            <el-menu-item index="/help">Help</el-menu-item>
            <el-menu-item index="/login">Log Out</el-menu-item>
          </el-sub-menu>
        </el-menu></div>
      <!-- <div class="h-24">buttom</div> -->
    </div>
    <div class="flex-grow w-4/5 border-solid border-2 border-indigo-600">

      <RouterView class="w-full"/>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import type { type_menu_tree_inner } from '@/api/sys'
import { useRouter } from 'vue-router'
import TopMenuUser from '@/views/TopMenuUser.vue'


const router = useRouter()
const use_router = ref(true)
const default_url = ref('/')
interface LocalValueInterface {
  side_width: number,
  menu_tree: type_menu_tree_inner[] | undefined,
  menu_item_html: string,
  menu_key: number,
  is_menu_fold: boolean,
}

const local_value = ref<LocalValueInterface>({
  side_width: 10,
  menu_tree: undefined,
  menu_item_html: '',
  menu_key: 1,
  is_menu_fold: false,
})

const go_home = async () => {
  default_url.value = '/'
  await nextTick();
  local_value.value.menu_key++;
  router.push('/');
}

function handleOpen() {

}
function handleClose() {

}
onMounted(() => {
})

</script>

<style>
.my_el_menu {
  --el-menu-bg-color: #e2e8f0;
  --el-menu-hover-bg-color: #64748b;
  --el-menu-text-color: #222831;
  --el-menu-hover-text-color: #393e46;
}
</style>
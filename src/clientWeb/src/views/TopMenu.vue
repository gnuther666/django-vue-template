<script setup lang="ts">
import { DArrowLeft } from '@element-plus/icons-vue';
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import type {RouteRecordName} from 'vue-router'
import TopMenuUser from '@/views/TopMenuUser.vue'

const route = useRoute()
const router = useRouter()
const use_router = ref(true)
const default_url = ref('/')
interface LocalValueInterface {
    is_menu_open: boolean,
    left_menu_class: string,
    menu_key: number,
    breadcrumbList: {
        'path': string ,
        'title': RouteRecordName|undefined,
        
    }[],
    last_access_url: string|undefined,
}

const local_value = ref<LocalValueInterface>({
    is_menu_open: true,
    left_menu_class: '',
    menu_key: 1,
    breadcrumbList: [{'path': '/', 'title': 'HomePage' }, ],
    last_access_url: undefined
})

onMounted(() => {
    setMenuClass()
})

function setMenuClass() {
    if (local_value.value.is_menu_open) {
        local_value.value.left_menu_class = "flex flex-col mr-1 h-screen border border-solid border-slate-400 max-w-40"
    } else {
        local_value.value.left_menu_class = "flex flex-col mr-1 h-screen border border-solid border-slate-400 min-w-16"
    }
}

function onFoldClicked() {
    local_value.value.is_menu_open = !local_value.value.is_menu_open
    setMenuClass()
}

watch(route, async (newRoute, oldRoute) => {
    console.log('inspect a url change', newRoute.path, oldRoute.path, local_value.value.last_access_url)
    if (local_value.value.last_access_url === undefined) {
        if (newRoute === undefined) {
            return
        }
        else {
            generateBreadcrumbList(newRoute);
            return;
        }
    } else {
        if (newRoute.path !== local_value.value.last_access_url) {
            generateBreadcrumbList(newRoute);
            return;
        } else {
            return
        }
    }
})

const go_home = async () => {
    default_url.value = '/'
    await nextTick();
    local_value.value.menu_key++;
    router.push('/');
    generateBreadcrumbList(route)
}

const generateBreadcrumbList = (route: any) => {
    let path = route.path;
    const breadcrumbList = [];
    if (path === '/') {
        breadcrumbList.push({ path: '/', title: 'Homepage' });
    } else {
        let root = router.options.routes.find(r => r.path === '/');
        let url_list = path.split('/').filter((y:string) => y !== '');
        let last_path = ''
        for (let index:number=0; index<url_list.length; index++) {
            if (root === undefined || root.children === undefined) {
                continue
            }
            let tmp_node_list:any[] = root.children.filter(y =>y.path===url_list[index])
            if (tmp_node_list.length === 0) {
                break;
            }
            let tmp_node = tmp_node_list[0]
            let tmp_path = last_path 
            tmp_path += '/'
            tmp_path += tmp_node.path
            breadcrumbList.push({ path: tmp_path, title: tmp_node.name})
            last_path = tmp_path
            root = tmp_node

        }
    }
    local_value.value.breadcrumbList = breadcrumbList
    local_value.value.last_access_url = path
    console.log('breadcrumbList changed:', local_value.value.breadcrumbList)
}

</script>

<template>
    <div class="flex w-full h-screen  border-solid border-2 border-indigo-600">
        <div :class="local_value.left_menu_class">
            <div v-if="local_value.is_menu_open"
                class="h-40 bg-slate-300 border border-solid border-slate-400 border-b border-x-0 border-t-0">
                <img src="@/assets/image/project_logo.png"
                    class="relative w-1/3 max-w-48 min-w-10 bg-gradient-to-b from-blue-500 to-red-500 rounded-lg left-12 top-6"
                    title="prj_logo" alt="prj_log" @click="go_home" />
                <div class="relative top-10 text-lg text-center text-zinc-950" @click="go_home">django vue template
                    system</div>
            </div>
            <div class="flex flex-col flex-grow">
                <el-menu :key="local_value.menu_key" mode="vertical" :collapse="!local_value.is_menu_open"
                    :default-active="default_url" :router="use_router" class="flex flex-col flex-grow">
                    <el-menu-item index="/">
                        <el-icon>
                            <House />
                        </el-icon>
                        <span>HomePage</span>
                    </el-menu-item>
                    <el-menu-item index="/example">
                        <el-icon>
                            <View />
                        </el-icon>
                        <span>example</span>
                    </el-menu-item>
                    <el-menu-item index="/notebook">
                        <el-icon>
                            <Memo />
                        </el-icon>
                        <span>NoteBook</span>
                    </el-menu-item>
                    <div class="flex-grow"></div>
                    <el-sub-menu index="ignore_submenu_2"><template #title>
                            <el-icon>
                                <Avatar />
                            </el-icon>
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
                </el-menu>
            </div>
        </div>
        <div class="flex flex-col h-screen border border-solid border-red-500 flex-grow">
            <div class="flex h-10 mb-0.5 border border-solid border-blue-500">
                <div class="mr-4">
                    <div @click="onFoldClicked">
                        <el-icon v-if="local_value.is_menu_open" size="30">
                            <DArrowLeft />
                        </el-icon>
                        <el-icon v-else size="30">
                            <DArrowRight />
                        </el-icon>
                    </div>
                </div>
                <div class="content-center">
                    <el-breadcrumb separator="/">
                        <el-breadcrumb-item v-for="item in local_value.breadcrumbList" :key="item.path"  :to="{ path: item.path }">{{ item.title }}</el-breadcrumb-item>
                    </el-breadcrumb>
                </div>
            </div>
            <div class="flex flex-grow border-solid border-green-500 overflow-auto">
                <router-view class="w-full"></router-view>
            </div>
        </div>
    </div>
</template>

<style></style>

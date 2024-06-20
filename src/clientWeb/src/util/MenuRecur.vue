<template>
    <template v-for="item in menu_data" :key="item.item_key">
        <el-menu-item :index="item.item_key" v-if="!item.children">{{ item.item_title }}</el-menu-item>
        <el-sub-menu v-else :index=item.item_key>
            <template #title>{{ item.item_title }}</template>
            <MenuRecur :menu_data=item.children />
        </el-sub-menu>
        
    </template>
</template>

<script setup lang="ts">
import type { type_menu_tree_inner } from '@/api/sys'
defineProps<{
    menu_data: type_menu_tree_inner[]
}>();
defineOptions({
    name:'MenuRecur'
})
</script>
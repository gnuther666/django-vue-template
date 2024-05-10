<template>
    <div class="popup-menu" :style="{ left: $props.x + 'px', top: $props.y+ 'px' }">
      <ul>
        <li @click="handleRename">重命名</li>
        <li @click="handleDelete">删除</li>
        <li @click="handleCancel">取消</li>
      </ul>
    </div>
</template>
  
<script setup lang='ts'>
import { emitChangeFn } from 'element-plus';
import { defineProps, defineEmits } from 'vue';
  
const props = defineProps<{x:number, y:number}>()
const emit = defineEmits(['rename', 'delete', 'cancel'])
function handleRename() {
  console.log('rename event')
  emit('rename')
}

function handleDelete() {
  console.log('delete event')
  emit('delete')
}

function handleCancel() {
  emit('cancel')
}
  </script>
  
  <style scoped>
  .popup-menu {
  position: absolute;
  background-color: #fff;
  border: 1px solid #ccc;
  list-style-type: none;
  padding: 5px;
}
.popup-menu li {
  cursor: pointer;
  padding: 3px 10px;
}
.popup-menu li:hover {
  background-color: #eee;
}
  </style>
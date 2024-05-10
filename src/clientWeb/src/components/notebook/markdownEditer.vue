<script setup lang="ts">
import { ref , onMounted, onUnmounted} from 'vue';
import { defineProps, onUpdated } from 'vue';
import { MdEditor } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
import { getDocContent, saveDocContent } from '@/api/notebook.ts'
import { ElMessage } from 'element-plus';

const props = defineProps(['doc_id'])

onUpdated(() => {
    if (props.doc_id !== undefined && local_value.value.current_doc_id !== props.doc_id) {
        local_value.value.current_doc_id = props.doc_id
        getDocContent(props.doc_id).then((res) => {
            local_value.value.editor_content = res.data
        })
    }
})
interface LocalValueInterface {
    current_doc_id: number|undefined
    editor_content: string
    timer: number|undefined
}

const local_value = ref<LocalValueInterface>({
    current_doc_id: props.doc_id,
    editor_content: 'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss',
    timer: undefined
})

function auto_save_content(v=undefined, h=undefined) {
    if (props.doc_id !== undefined && local_value.value.editor_content !== '') {
        saveDocContent(props.doc_id, local_value.value.editor_content).then((res) => {
            if (res.code === 200) {
                ElMessage({
                    type: 'success',
                    message: 'save success',
                })
            } else {
                ElMessage({
                    type: 'error',
                    message: `save error ${res.msg}`
                })
            }
        })
    }
}

onMounted(()=>{
    local_value.value.timer = setInterval(auto_save_content, 30000)
})

onUnmounted(() => {
    clearInterval(local_value.value.timer);
})
</script>

<template>
  <main>
    <MdEditor v-model="local_value.editor_content" @onSave="auto_save_content" />
  </main>
</template>

<script setup lang="ts">
import bookSelect from "@/components/notebook/bookSelect.vue"
import markdownEditer from "@/components/notebook/markdownEditer.vue"
import { ref, nextTick } from 'vue'
interface LocalValueInterface {
  doc_id: number|undefined
  book_id: number|undefined
}

const local_value = ref<LocalValueInterface>({
  doc_id: undefined,
  book_id: undefined
})
</script>

<template>
  <main>
    <div :style="{position: 'absolute', left: '20px', top:'15vh', backgroundColor: 'white', zIndex: '1'}">
      <bookSelect @book_id_change="(doc_id, book_id) => (local_value.doc_id = doc_id, local_value.book_id = book_id)"/>
    </div>
    
    <markdownEditer :doc_id=local_value.doc_id :book_id=local_value.book_id v-if="local_value.doc_id"/>
  </main>
</template>

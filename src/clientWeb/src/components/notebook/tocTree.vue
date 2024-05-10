<script setup lang="ts">
import { defineProps, onUpdated, ref } from 'vue';
import { getTocBooks, addNote as ApiAddNote } from '@/api/notebook'
import isEmptyObject from '@/util/isEmptyObject'
import { ElMessage, ElMessageBox } from 'element-plus'
const props = defineProps(['book_id'])

interface TocStruct {
    id: number,
    type: string,
    label: string,
    children?: TocStruct[]
}

enum DocType {
    PlainText = 'plain text',
    MarkDown = 'Markdown',
}

interface LocalValueInterface {
    current_book_id: number | undefined,
    current_doc_id: number | undefined,
    toc: TocStruct | undefined,
    showAddTocDialog: boolean,
    AddNote: {
        addNoteParentId: number | undefined,
        addNoteName: string,
        addNoteType: string,
    }
    searchText: string | undefined

}

const local_value = ref<LocalValueInterface>({
    current_book_id: undefined,
    current_doc_id: undefined,
    toc: undefined,
    showAddTocDialog: false,
    AddNote: {
        addNoteParentId: undefined,
        addNoteName: 'default name',
        addNoteType: DocType.MarkDown
    },
    searchText: undefined
})

onUpdated(() => {
    console.log('book_id changed', props.book_id)
    if (local_value.value.current_book_id !== props.book_id) {
        local_value.value.current_book_id = props.book_id
        local_value.value.current_doc_id = undefined
        getToc()
    }
})

function getToc() {
    if (local_value.value.current_book_id !== undefined) {
        getTocBooks(local_value.value.current_book_id).then((res) => {
            local_value.value.toc = res.data
        })
    }
}

function addDoc(parent = undefined) {
    if (local_value.value.current_book_id === undefined) {
        ElMessage({
            message: `unselect book`,
            type: 'error',
        })
        return
    }
    console.log('add note', local_value.value.AddNote)
    local_value.value.showAddTocDialog = false
    ApiAddNote(local_value.value.current_doc_id, local_value.value.AddNote.addNoteName, local_value.value.AddNote.addNoteType, local_value.value.current_book_id).then((res) => {
        if (res.code === 200) {
            ElMessage({
                message: 'Add success',
                type: 'success',
            })
            local_value.value.toc = res.data
        } else {
            ElMessage({
                message: `Add failed ${res.msg}`,
                type: 'error',
            })
        }
    })
}

function DocClicked(data: TocStruct) {
    console.log('doc clicked', data)
    local_value.value.current_doc_id = data.id
}
</script>

<template>
    <main>
        <div class="tree_window">
            <el-button v-if="local_value.toc === undefined || isEmptyObject(local_value.toc)"
                @click="() => local_value.showAddTocDialog = true">新增文档</el-button>
            <div v-else>
                <div>
                    <el-popover placement="right" :width="400" trigger="click">
                        <template #reference>
                            <el-button link><el-icon>
                                    <Search />
                                </el-icon></el-button>
                        </template>
                        <el-input placeholder="search" :clearable=true v-model="local_value.searchText"></el-input>

                    </el-popover>
                    <el-button @click="() => {
                        local_value.showAddTocDialog = true
                    }" link><el-icon>
                            <CirclePlus />
                        </el-icon></el-button>

                    <el-popover placement="right" :width="400" trigger="click">
                        <template #reference>
                            <el-button @click="() => local_value.toc = undefined" link><el-icon>
                                    <Delete />
                                </el-icon></el-button>
                        </template>
                        delete
                    </el-popover>


                </div>
                <el-tree :data="[local_value.toc]" @node-click="DocClicked" :highlight-current="true">
                </el-tree>
            </div>

        </div>
        <el-dialog v-model="local_value.showAddTocDialog" title="add note" width="40vw" align-center>
            <el-form :model="local_value.AddNote">
                <el-form-item label="parent id">
                    <el-text>{{ local_value.current_doc_id === undefined ? 'root' : local_value.current_doc_id }}</el-text>
                </el-form-item>
                <el-form-item label="note type">
                    <el-radio-group v-model="local_value.AddNote.addNoteType">
                        <el-radio :key="type_name" :value="type_name" v-for="(type_name, type_string) in DocType">{{
                            type_string }}</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="note name">
                    <el-input v-model="local_value.AddNote.addNoteName" />
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="() => local_value.showAddTocDialog = false">Cancel</el-button>
                    <el-button type="primary" @click="addDoc">
                        Confirm
                    </el-button>
                </div>
            </template>
        </el-dialog>

    </main>
</template>

<style scoped>
@media (min-width: 601px) {
    .tree_window {
        width: 20vw;
        height: 60vh;
        border: 1px solid #ccc;
    }
}
</style>

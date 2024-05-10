<script setup lang="ts">
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import { ElMessageBox, ElMessage, tagEmits } from 'element-plus'
import bookMenu from '@/components/notebook/bookMenu.vue'
import tocTree from '@/components/notebook/tocTree.vue'
import { getGetBooks, type_get_books, addBooks, type_add_books, renameBooks, deleteBooks } from '@/api/notebook'
interface LocalValueInterface {
    is_close: boolean;
    current_text: string;
    current_select_index: number | undefined;
    books: type_get_books | undefined;
    touched: number;
    showMenu: boolean;
    menuPosition: Record<string, number>;
    currentPosition: Record<string, number>;

    DoubleClickedButtonBookId?: number;
    clickTimer: number | undefined;
}
const longTouchDuration = 500;
const menu = ref(null)
const local_value = ref<LocalValueInterface>({
    is_close: false,
    current_text: '默认笔记本',
    current_select_index: undefined,
    books: undefined,
    touched: 0,
    showMenu: false,
    menuPosition: { x: 0, y: 0 },
    currentPosition: { x: 0, y: 0 },

    DoubleClickedButtonBookId: undefined,
    clickTimer: undefined
})

function handleNormalBookClicked(key: number | undefined): undefined {
    clearTimeout(local_value.value.clickTimer);
    local_value.value.clickTimer = setTimeout(() => {
        local_value.value.current_select_index = key
        handleFoldClicked()
    }, 300);

}
function handleNormalBookDoubleClick(key: number | undefined): undefined {
    clearTimeout(local_value.value.clickTimer);
    console.log('double clicked', key)
    local_value.value.menuPosition['x'] = local_value.value.currentPosition['x']
    local_value.value.menuPosition['y'] = local_value.value.currentPosition['y']
    local_value.value.showMenu = true
    local_value.value.DoubleClickedButtonBookId = key
}

function handleFoldClicked() {
    // local_value.value.is_close = !local_value.value.is_close
    if (!local_value.value.is_close) {
        updateBooks()
    }
}

function getCurrentSelectBookName(): string {
    if (local_value.value.current_select_index === undefined) {
        return 'books'
    } else {
        let book_name = undefined
        if (local_value.value.books !== undefined) {
            book_name = local_value.value.books[local_value.value.current_select_index]
        }
        if (book_name === undefined) {
            return 'books'
        } else {
            return book_name
        }
    }
}



function updateBooks(): undefined {
    getGetBooks().then((res) => {
        local_value.value.books = res.data
    })
    console.log('本次获取到的books', local_value.value.books)
}

function addBook() {
    ElMessageBox.prompt('please input your book name', undefined, {
        confirmButtonText: 'Ok',
        cancelButtonText: 'Cancel',
        inputPattern: /.{4,30}/,
        inputErrorMessage: '长度在4到30位之间'
    }).then(({ value }) => {
        addBooks(value).then((res) => {
            if (res.code === 200) {
                updateBooks()
                ElMessage({
                    type: 'success',
                    message: `Your add the book:${value}`,
                })
            } else {
                ElMessage({
                    type: 'warning',
                    message: `Your add the book:${value} occurred an error ${res.msg}`,
                })
            }
        })



    })
        .catch(() => {
            ElMessage({
                type: 'error',
                message: 'Input canceled',
            })
        })
}


function handleMouseLeave() {
    local_value.value.showMenu = false
    console.log('鼠标离开')
}

function rename_book(): undefined {
    console.log('重命名操作', local_value.value.DoubleClickedButtonBookId);
    handleMouseLeave()
    // 调用实际的重命名逻辑
    const default_text = local_value.value.books !== undefined && local_value.value.DoubleClickedButtonBookId !== undefined ? local_value.value.books[local_value.value.DoubleClickedButtonBookId] : ''
    ElMessageBox.prompt('please input your book name', undefined, {
        confirmButtonText: 'Ok',
        cancelButtonText: 'Cancel',
        inputPattern: /.{4,30}/,
        inputErrorMessage: '长度在4到30位之间',
        inputValue: default_text,
    }).then(({ value }) => {

        renameBooks(local_value.value.DoubleClickedButtonBookId as number, value).then((res) => {
            if (res.code === 200) {
                ElMessage({
                    type: 'success',
                    message: `Your rename the book:${value}`,
                })
                updateBooks()
            } else {
                ElMessage({
                    type: 'warning',
                    message: `Your rename the book:${value} occurred an error ${res.msg}`,
                })
            }
        })



    })
        .catch(() => {
            ElMessage({
                type: 'error',
                message: 'Input canceled',
            })
        })
}
function delete_book(): undefined {
    console.log('删除操作', local_value.value.DoubleClickedButtonBookId);
    handleMouseLeave()
    // 调用实际的删除逻辑
    ElMessageBox.confirm(
        'will delete the file. Continue?',
        'Warning',
        {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            type: 'warning',
        }
    )
        .then(() => {
            deleteBooks(local_value.value.DoubleClickedButtonBookId as number).then((res) => {
                if (res.code === 200) {
                    ElMessage({
                        type: 'success',
                        message: 'Delete completed',
                    })
                    updateBooks()
                } else {
                    ElMessage({
                        type: 'warning',
                        message: `Your delete the book occurred an error ${res.msg}`,
                    })
                }
            })

        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: 'Delete canceled',
            })
        })
}

function cancel_book_menu_popu(): undefined {
    handleMouseLeave()
}

function HandleMousePosition(event: MouseEvent) {
    local_value.value.currentPosition['x'] = event.clientX;
    local_value.value.currentPosition['y'] = event.clientY;
}
onMounted(() => {
    document.addEventListener('mousemove', HandleMousePosition);
    updateBooks()
})

onUnmounted(() => {
    document.removeEventListener('mousemove', HandleMousePosition)
})
</script>

<template>
    <main>
        <div @mousemove="HandleMousePosition">
            <el-button @click="()=> {
                handleFoldClicked()
                local_value.is_close = !local_value.is_close
            }" link><el-icon>
                    <ArrowLeftBold />
                </el-icon> {{ getCurrentSelectBookName() }}</el-button>
            <el-button v-if="!local_value.is_close" v-for="(value, key) in local_value.books" :key="key"
                @click="handleNormalBookClicked(key)" @dblclick.native="handleNormalBookDoubleClick(key)"
                :type="key === local_value.current_select_index ? 'primary' : 'info'">
                {{ value }}
            </el-button>
            <el-button v-if="!local_value.is_close" @click="addBook"><el-icon>
                    <Plus />
                </el-icon></el-button>
        </div>
        <div ref="menu">
            <bookMenu :x="local_value.menuPosition['x']" :y="local_value.menuPosition['y']" v-if="local_value.showMenu"
                @delete="delete_book" @rename="rename_book" @cancel="cancel_book_menu_popu" />
        </div>

        <div :style="{ display: local_value.is_close ? 'none' : 'block' }">
            <tocTree :book_id="local_value.current_select_index"/>
        </div>
    </main>
</template>

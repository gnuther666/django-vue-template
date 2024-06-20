<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getAuthGroups, setAuthGroup } from '@/api/admin'
import type { type_auth_group_inner } from '@/api/admin'
import { ElTable, ElTableColumn, ElMessage } from 'element-plus';

interface Column {
  prop: string;
  label: string;
  editRender?: any; // Ideally, you would define a proper type for the editRender if possible
}

const group_table_column: Column[] = [
  //'group_id', 'group__name', 'outer_name', 'description'
  { prop: 'group_id', label: 'Name' },
  { prop: 'group__name', label: 'group name' },
  { prop: 'outer_name', label: 'outer name' },
  { prop: 'description', label: 'description' },
  // Add more columns
];


interface LocalValueInterface {
  auth_groups: undefined | type_auth_group_inner[],
  activeTabName: string,
  showGroupEditor: boolean,
  editingGroupIndex: number,
}


const local_value = ref<LocalValueInterface>({
  auth_groups: undefined,
  activeTabName: 'group',
  showGroupEditor: false,
  editingGroupIndex: 0,
})

onMounted(() => {
  getAuthGroups().then((res) => {
    local_value.value.auth_groups = res.data
  }
  )
})

const onGroupEditClicked = (index: number) => {
  local_value.value.editingGroupIndex = index
  local_value.value.showGroupEditor = true
}
function hideGroupEditDialog() {
  local_value.value.editingGroupIndex = 0
  local_value.value.showGroupEditor = false
}

function submitGroupInfo() {
  let index = local_value.value.editingGroupIndex;
  if (index === undefined || local_value.value.auth_groups === undefined || local_value.value.auth_groups.length < index) {
    return
  }
  setAuthGroup(local_value.value.auth_groups[index]).then((res) => {
    if (local_value.value.auth_groups && local_value.value.auth_groups.length < index)
      local_value.value.auth_groups[index] = res.data
  })
}

</script>

<template>
  <main class="w-full">
    <el-tabs v-model="local_value.activeTabName" class="demo-tabs">
      <el-tab-pane label="group" name="group">
        <el-table :data="local_value.auth_groups" style="width: 100%">
          <el-table-column v-for="(column, index) in group_table_column" :key="index" :prop="column.prop"
            :label="column.label" />
          <el-table-column align="right">
            <template #header>
              operate
            </template>
            <template #default="scope">
              <el-button size="small" @click="onGroupEditClicked(scope.$index)">
                Edit
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="group_permission" name="group_permission">group_permission</el-tab-pane>
    </el-tabs>
    <el-dialog v-model="local_value.showGroupEditor" title="edit group" width="500">
      <el-form v-if="local_value.editingGroupIndex != undefined && local_value.editingGroupIndex >= 0
        && local_value.auth_groups" :model="local_value.auth_groups[local_value.editingGroupIndex]">
        <el-form-item label="group id" :label-width="80">
          <div>{{ local_value.auth_groups[local_value.editingGroupIndex].group_id }}</div>
        </el-form-item>
        <el-form-item label="group id" :label-width="80">
          <div>{{ local_value.auth_groups[local_value.editingGroupIndex].group__name }}</div>
        </el-form-item>
        <el-form-item label="outer name" :label-width="80">
          <el-input v-model="local_value.auth_groups[local_value.editingGroupIndex].outer_name" autocomplete="off" />
        </el-form-item>
        <el-form-item label="description" :label-width="80">
          <el-input v-model="local_value.auth_groups[local_value.editingGroupIndex].description" autocomplete="off"
            type="textarea" maxlength="500" show-word-limit />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="() => {
            hideGroupEditDialog();
            ElMessage({
              type: 'info',
              message: 'calcel operation',
            })
          }">Cancel</el-button>
          <el-button type="primary" @click="() => {
            submitGroupInfo(); hideGroupEditDialog();
            ElMessage({
              type: 'success',
              message: 'success save',
            })

          }">
            Confirm
          </el-button>
        </div>
      </template>
    </el-dialog>
  </main>
</template>

<style></style>

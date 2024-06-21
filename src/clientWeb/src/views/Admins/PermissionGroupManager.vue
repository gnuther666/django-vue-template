<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getPermissions, getAuthGroups, getGroupPermissions, addGroupPermissions, delGroupPermissions } from '@/api/admin'
import type { type_permission_inner, type_auth_group_inner } from '@/api/admin'
import { ElMessage } from 'element-plus'

interface LocalValueInterface {
  could_auth_groups: type_auth_group_inner[],
  could_auth_permissions: type_permission_inner[],
  right_permissions: type_permission_inner[],
  current_choosed_group: undefined | number,
  current_left_perm_selected: string[],
  current_right_perm_selected: string[],
}

const local_value = ref<LocalValueInterface>({
  could_auth_groups: [],
  could_auth_permissions: [],
  right_permissions: [],
  current_choosed_group: undefined,
  current_left_perm_selected: [],
  current_right_perm_selected: []
})



onMounted(() => {
  getAuthGroups().then((res) => {
    local_value.value.could_auth_groups = res.data
  }
  )
  getPermissions().then((res) => {
    local_value.value.could_auth_permissions = res.data
  })
})


function onChooseGroupChanged(current_index: string | number | boolean) {
  console.log('group changed', current_index)
  updateGroupPermissions()
}

function updateGroupPermissions() {
  if (!local_value.value.current_choosed_group) {
    return
  }
  getGroupPermissions(local_value.value.current_choosed_group).then((res) => {
    local_value.value.right_permissions = res.data
    console.log('test1', local_value.value.could_auth_permissions, local_value.value.right_permissions)
  })
}

function onLeftPermssionChooseChanged(value: string[]) {
  console.log('left permission changed', value)
}

function onAddGroupPermissions() {
  if (local_value.value.current_choosed_group === undefined) {
    return;
  }
  if (local_value.value.current_left_perm_selected.length === 0) {
    ElMessage({
      message: 'please select which permission you need add, you can click on left checkbox select it.',
      type: 'warning',
    })
    return;
  }
  addGroupPermissions(local_value.value.current_choosed_group, local_value.value.current_left_perm_selected).then((res) => {
    console.log('has set ok', res)
    updateGroupPermissions()
    ElMessage({ message: 'update success', type: 'success', })
  })
}

function onDelGroupPermissions() {
  if (local_value.value.current_choosed_group === undefined) {
    return;
  }
  if (local_value.value.current_right_perm_selected.length === 0) {
    ElMessage({
      message: 'please select which permission you need delete, you can click on right checkbox select it.',
      type: 'warning',
    })
    return;
  }
  console.log('now add group', local_value.value.current_choosed_group, local_value.value.current_right_perm_selected)
  delGroupPermissions(local_value.value.current_choosed_group, local_value.value.current_right_perm_selected).then((res) => {
    console.log(res)
    updateGroupPermissions()
    ElMessage({ message: 'update success', type: 'success', })
  })
}



</script>

<template>
  <main class="w-full flex h-96">
    <div
      class="flex flex-col max-w-40 min-w-30 bg-slate-50 ml-2 mr-2 w-1/5  border-solid border-slate-300 rounded-lg border">
      <div class="h-8 ml-2 mt-2">choose a group:</div>
      <div class="flex-grow overflow-atuo">
        <el-radio-group v-model="local_value.current_choosed_group" class="ml-4" @change="onChooseGroupChanged">
          <el-radio v-for="item in local_value.could_auth_groups" :key="item.group_id" :value="item.group_id"
            size="large">{{
              item.outer_name }}</el-radio>
        </el-radio-group>
      </div>
    </div>

    <div v-if="local_value.current_choosed_group"
      class="flex flex-grow bg-slate-50 mr-2 border-solid border-slate-300 rounded-lg border disable">
      <div class="flex flex-col flex-grow min-w-56 border-solid border-slate-300 rounded-lg border">

          <div class="h-8 ml-2 mt-2">could auth permission</div>
          <div class="flex-grow overflow-atuo ml-2">
            <el-checkbox-group v-model="local_value.current_left_perm_selected" class="flex flex-col"
              @change="onLeftPermssionChooseChanged">
              <el-checkbox v-for="item in local_value.could_auth_permissions" :key="item.name" :label="item.value"
                :value="item.name"
                :disabled="local_value.right_permissions.filter(y => y.name === item.value).length ? true : false" />
            </el-checkbox-group>
          </div>


      </div>
      <div class="max-w-28 content-center ml-2 mr-2">
        <div class="flex">
          <el-button type="primary" @click="onDelGroupPermissions"><el-icon>
              <ArrowLeftBold />
            </el-icon></el-button>
          <el-button type="primary" @click="onAddGroupPermissions"><el-icon>
              <ArrowRightBold />
            </el-icon></el-button>
        </div>
      </div>
      <div class="flex flex-col flex-grow min-w-56 border-solid border-slate-300 rounded-lg border">
          <div class="h-8 ml-2 mt-2">has auth permission</div>
          <div class="flex-grow overflow-atuo ml-2"> <el-checkbox-group v-model="local_value.current_right_perm_selected" class="flex flex-col">
              <el-checkbox v-for="item in local_value.right_permissions" :key="item.value" :label="item.name"
                :value="item.value" />
            </el-checkbox-group>
          </div>

      </div>
    </div>

  </main>
</template>

<style></style>

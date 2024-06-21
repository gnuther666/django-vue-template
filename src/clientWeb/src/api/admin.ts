import { post, get, put, del } from "./base_method"
import type {common_response} from "./base_method"

export type type_auth_group_inner =  {
    group_id: number, 
    group__name: string, 
    outer_name:string, 
    description: null|string
}

export type type_permission_inner = {
    name: string,
    value: string
}


export type type_auth_groups = common_response<type_auth_group_inner[]>
export type type_one_group = common_response<type_auth_group_inner>
export type type_permissions = common_response<type_permission_inner[]>

const api_list: Record<string, string> = {
    'get_auth_groups': '/backend/api/permission/get_auth_groups/',
    'set_auth_group': '/backend/api/permission/set_auth_group_info/',
    'get_permissions': '/backend/api/permission/get_could_auth_permissions/',
    'get_group_permissions': '/backend/api/permission/get_group_permissions/',
    'add_group_permission': '/backend/api/permission/add_groups_permission/',
    'del_group_permission': '/backend/api/permission/del_groups_permission/',

}

export function getAuthGroups(): Promise<type_auth_groups>  {
    const data = get<type_auth_groups>(api_list.get_auth_groups)
    return data 
}

export function setAuthGroup(arg: type_auth_group_inner): Promise<type_one_group>  {
    const data = post<type_one_group>(api_list.set_auth_group, arg)
    return data 
}

export function getPermissions(): Promise<type_permissions>  {
    const data = get<type_permissions>(api_list.get_permissions)
    return data 
}

export function getGroupPermissions(group_id: string | number | boolean): Promise<type_permissions>  {
    const data = get<type_permissions>(api_list.get_group_permissions, {'group_id': group_id})
    return data 
}

export function addGroupPermissions(group_id: number, permissions: string[]): Promise<common_response<string>>  {
    const data = post<common_response<string>>(api_list.add_group_permission, {'group_id': group_id, 'permissions': permissions})
    return data 
}

export function delGroupPermissions(group_id: number, permissions: string[]): Promise<common_response<string>>  {
    const data = post<common_response<string>>(api_list.del_group_permission, {'group_id': group_id, 'permissions': permissions})
    return data 
}
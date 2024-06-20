import { post, get, put, del } from "./base_method"
import type {common_response} from "./base_method"

export type type_auth_group_inner =  {
    group_id: number, 
    group__name: string, 
    outer_name:string, 
    description: null|string
}

export type type_auth_groups = common_response<type_auth_group_inner[]>
export type type_one_group = common_response<type_auth_group_inner>

const api_list: Record<string, string> = {
    'get_auth_groups': '/backend/api/permission/get_auth_groups/',
    'set_auth_group': '/backend/api/permission/set_auth_group_info/',

}

export function getAuthGroups(): Promise<type_auth_groups>  {
    const data = get<type_auth_groups>(api_list.get_auth_groups)
    return data 
}

export function setAuthGroup(arg: type_auth_group_inner): Promise<type_one_group>  {
    const data = post<type_one_group>(api_list.set_auth_group, arg)
    return data 
}
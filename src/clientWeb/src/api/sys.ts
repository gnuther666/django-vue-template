import { post, get, put, del } from "./base_method"
import type {common_response} from "./base_method"

export type type_menu_tree_inner =  {
    item_key: string,
    item_title: string,
    item_url: null|string,
    sort_seq: number,
    is_active: boolean,
    item_description: null|string,
    children?: type_menu_tree_inner[]
}

export type type_menu_tree = common_response<type_menu_tree_inner[]>

const api_list: Record<string, string> = {
    'get_menu': '/backend/api/sys_menu/',

}

export function getMenuTree(): Promise<type_menu_tree>  {
    const data = get<type_menu_tree>(api_list.get_menu)
    return data 
}

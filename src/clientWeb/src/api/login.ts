import { post, get, put, del } from "./base_method"
import type {common_response} from "./base_method"

// 定义所有接口地址
const api_list: Record<string, string> = {
    login: '/backend/login/',
    getUserInfo: '/user/info',
    logout: '/user/logout',
    captcha: '/backend/captcha/'
}

type type_captcha  = {
    image_hex: string
    key: string
}
type type_Logininfo = {
    access_token: string
    refresh_token: string
    username: string
}

export function getCaptcha(): Promise<common_response<type_captcha>> {
    return get<common_response<type_captcha>>(api_list.captcha)
}

export function postLogin(data: any): Promise<common_response<type_Logininfo>> {
    return post<common_response<type_Logininfo>>(api_list.login, data)
}

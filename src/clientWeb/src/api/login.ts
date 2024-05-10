import { post, get, put, del } from "./base_method"

// 定义所有接口地址
const api_list: Record<string, string> = {
    login: '/backend/login/',
    getUserInfo: '/user/info',
    logout: '/user/logout',
    captcha: '/backend/captcha/'
}

interface Captcha {
    image_hex: string
    key: string
}
interface LoginInfo {
    access_token: string
    refresh_token: string
    username: string
}

export function getCaptcha(): Promise<Captcha> {
    return get<Captcha>(api_list.captcha)
}

export function postLogin(data: any): Promise<LoginInfo> {
    return post<LoginInfo>(api_list.login, data)
}

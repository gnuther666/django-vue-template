import http from './http'

 namespace LOGIN {
     interface Captcha {
        image_hex: string
        key: string
    }
    interface LoginInfo {
        access_token: string
        refresh_token: string
        username: string
    }
}

namespace EXAMPLE {
  interface get_image_list {
    images: Array<string>
  }
}

// 定义所有接口地址
interface API {
  login: string
  getUserInfo: string
  logout: string
  captcha: string
  get_image_list: string
}

const api: API = {
  login: '/backend/login/',
  getUserInfo: '/user/info',
  logout: '/user/logout',
  captcha: '/backend/captcha/',
  get_image_list: '/backend/api/example/get_image_list/',
}

// 封装 GET 请求
function get<T>(url: string, params?: any): Promise<T> {
  return http.get(url, { params })
}

// 封装 POST 请求
function post<T>(url: string, data?: any): Promise<T> {
  return http.post(url, data)
}

// 封装 PUT 请求
function put<T>(url: string, data?: any): Promise<T> {
  return http.put(url, data)
}

// 封装 DELETE 请求
function del<T>(url: string, params?: any): Promise<T> {
  return http.delete(url, { params })
}



export function getCaptcha(): Promise<LOGIN.Captcha> {
    return get<LOGIN.Captcha>(api.captcha)
}

export function postLogin(data: any): Promise<LOGIN.LoginInfo> {
    return post<LOGIN.LoginInfo>(api.login, data)
}

export function getImageList(): Promise<EXAMPLE.get_image_list> {
  return get<EXAMPLE.get_image_list>(api.get_image_list)
}
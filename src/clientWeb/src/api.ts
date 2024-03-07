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

// 定义所有接口地址
interface API {
  login: string
  getUserInfo: string
  logout: string
  captcha: string
}

const api: API = {
  login: '/app-api/login/',
  getUserInfo: '/user/info',
  logout: '/user/logout',
  captcha: '/captcha/',
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
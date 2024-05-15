import http from './base_http'

export interface common_response<T> {
    code: number,
    data: T,
    msg: string,
}

// 封装 GET 请求
export function get<T>(url: string, params?: any): Promise<T> {
    return http.get(url, { params })
}


// 封装 POST 请求
export function post<T>(url: string, data?: any): Promise<T> {
    return http.post(url, data)
}

// 封装 PUT 请求
export function put<T>(url: string, data?: any): Promise<T> {
    return http.put(url, data)
}

// 封装 DELETE 请求
export function del<T>(url: string, params?: any): Promise<T> {
    return http.delete(url, { params })
}

export function post_form<T>(url: string, params?: any): Promise<T> {
    return http.post(url, params, {'headers': {'Content-Type': 'multipart/form-data'}})
}
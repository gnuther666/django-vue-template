import { post, get, put, del } from "./base_method"
import type { common_response } from "./base_method"


export type type_example_image_list = {
    images: Array<string>
}
export type type_example_image_url = {
    file_url: string
}


const api_list: Record<string, string> = {
    'get_image_list': '/backend/api/example/get_image_list/',
    'get_example_image_url': '/backend/api/example/get_example_file/'
}

export function getImageList(): Promise<common_response<type_example_image_list>> {
    return get<common_response<type_example_image_list>>(api_list.get_image_list)
}


export function getTestImage(url_path: string): Promise<common_response<type_example_image_url>> {
    return get<common_response<type_example_image_url>>(url_path)
}
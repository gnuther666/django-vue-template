import { post, get, put, del } from "./base_method"


interface itfc_get_image_list {
    images: Array<string>
}
interface itfc_get_example_image_url {
    file_url: string
}


const api_list: Record<string, string> = {
    'get_image_list': '/backend/api/example/get_image_list/',
    'get_example_image_url': '/backend/api/example/get_example_file/'
}

export function getImageList(): Promise<itfc_get_image_list> {
    return get<itfc_get_image_list>(api_list.get_image_list)
}


export function getTestImage(url_path): Promise<itfc_get_example_image_url> {
    return get<itfc_get_example_image_url>(url_path)
}
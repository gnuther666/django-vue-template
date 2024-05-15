import { post, get, put, del, post_form } from "./base_method"

export type type_get_books = Record<number, string>

export type type_add_books =  {
    book_id: number,
    book_name: string
}

const api_list: Record<string, string> = {
    'get_books': '/backend/api/notebook/get_books/',
    'add_books': '/backend/api/notebook/add_books/',
    'delete_book': '/backend/api/notebook/delete_book/',
    'update_book': '/backend/api/notebook/update_book/',

    'get_tocs': '/backend/api/notebook_toc/get_tocs/',
    'add_note': '/backend/api/notebook_toc/add_note/',
    'get_doc_content': '/backend/api/notebook_doc/get_doc_content/',
    'save_content': '/backend/api/notebook_doc/save_content/',
    'upload_image': '/backend/api/notebook_doc/upload_image/'
}

export function getGetBooks(): Promise<type_get_books>  {
    const data = get<type_get_books>(api_list.get_books)
    return data 
}


export function addBooks(book_name:string): Promise<type_add_books> {
    return post<type_add_books>(api_list.add_books, {'book_name': book_name})
}

export function renameBooks(book_id:number, book_name:string): Promise<type_add_books> {
    return post<type_add_books>(api_list.update_book, {'book_id': book_id, 'book_name': book_name})
}

export function deleteBooks(book_id:number): Promise<type_add_books> {
    return post<type_add_books>(api_list.delete_book, {'book_id': book_id})
}

export function getTocBooks(book_id:number): Promise<type_get_books>  {
    const data = get<type_get_books>(api_list.get_tocs, {'book_id': book_id})
    return data 
}

export function addNote(parent_id:number|undefined, title:string, type:string, book_id: number): Promise<type_add_books> {
    return post<type_add_books>(api_list.add_note, {'parent_id': parent_id, 'title': title, 'type': type, 'book_id': book_id})
}

export function getDocContent(doc_id:number): Promise<type_get_books>  {
    const data = get<type_get_books>(api_list.get_doc_content, {'doc_id': doc_id})
    return data 
}

export function saveDocContent(doc_id:number, doc_content:string): Promise<type_get_books>  {
    const data = post<type_get_books>(api_list.save_content, {'doc_id': doc_id, 'doc_content': doc_content})
    return data 
}

export function upload_image(book_id: number, doc_id:number, image:Blob): Promise<type_get_books>  {
    const fromData = new FormData()
    console.log(typeof image)
    fromData.append('book_id', book_id.toString())
    fromData.append('doc_id', doc_id.toString())
    fromData.append('image', image, image.name||'image' )
    const data = post_form<type_get_books>(api_list.upload_image, fromData)
    return data 
}
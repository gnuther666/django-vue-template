
def findDocWithId(toc, id):
    if toc['id'] == id:
        return toc
    else:
        if 'children' in toc:
            for child in toc['children']:
                if child['id'] == id:
                    return child
                else:
                    if 'children' in child:
                        return findDocWithId(child, id)


if __name__ == '__main__':
    case1 = {
                'id': 1,
                'type': 'MarkDown',
                'label': 'chapter1',
            }
    search1 = findDocWithId(case1, 1)
    print('search1', search1)

    case2 = {
                'id': 1,
                'type': 'MarkDown',
                'label': 'chapter1',
                'children': [
                    {
                        'id': 2,
                        'type': 'MarkDown',
                        'label': 'chapter2',
                    }
                ]
    }
    search2 = findDocWithId(case2, 2)
    print('search2', search2)

    case3 = {
                'id': 1,
                'type': 'MarkDown',
                'label': 'chapter1',
                'children': [
                    {
                        'id': 2,
                        'type': 'MarkDown',
                        'label': 'chapter2',
                        'children': [
                            {
                                'id': 3,
                                'type': 'MarkDown',
                                'label': 'chapter3',
                            },
                            {
                                'id': 4,
                                'type': 'MarkDown',
                                'label': 'chapter4',

                            }
                        ]
                    }
                ]
    }
    search3 = findDocWithId(case3, 3)
    print('search3', search3)
    search4 = findDocWithId(case3, 4)
    print('search4', search4)
    search5 = findDocWithId(case3, 5)
    print('search5', search5)

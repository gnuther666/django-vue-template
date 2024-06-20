def multi_tree_dict(item_list, main_key_field_name='id', parent_key_field_name='parent_id'):
    """
    help me to complete this function code
    """
    id_to_item = {item[main_key_field_name]: item for item in item_list}

    # Initialize the root of the tree (items without parents)
    tree = [item for item in item_list if item[parent_key_field_name] is None]

    # Function to recursively add children to a node
    def add_children(node):
        node.setdefault('children', [])
        for item in item_list:
            if item[parent_key_field_name] == node[main_key_field_name]:
                node['children'].append(add_children(item))
        return node

    # Add children to each node in the tree
    for node in tree:
        add_children(node)

    def clean_empty_child(node:dict):
        if node.get('children', None) is not None and len(node['children']) > 0:
            for one_node in node['children']:
                clean_empty_child(one_node)
        if node.get('children', None)is not None and len(node['children']) == 0:
            del node['children']
        del node[parent_key_field_name]
    for node in tree:
        clean_empty_child(node)

    return tree if tree else None


if __name__ == '__main__':
    test_data1 = [{'id': 1, 'name': 'aaa', 'age': 15, 'parent_id': None},
                  {'id': 2, 'name': 'bbb', 'age': 20, 'parent_id': None},
                  {'id': 3, 'name': 'ccc', 'age': 20, 'parent_id': 2}]
    expected = [
        {'id': 1, 'name': 'aaa', 'age': 15, },
        {'id': 2, 'name': 'bbb', 'age': 20, 'children':
            [{'id': 1, 'name': 'aaa', 'age': 15}]
         },
    ]
    result = multi_tree_dict(test_data1, main_key_field_name='id', parent_key_field_name='parent_id')
    print('->', result)


    test_data_three_level = [{'id': 1, 'name': 'aaa', 'age': 15, 'parent_id': None},
                             {'id': 2, 'name': 'bbb', 'age': 20, 'parent_id': None},
                             {'id': 3, 'name': 'ccc', 'age': 20, 'parent_id': 2},
                             {'id': 4, 'name': 'ccc', 'age': 20, 'parent_id': 3},
                             {'id': 5, 'name': 'ccc', 'age': 20, 'parent_id': 3}]
    expected_three_level = [ {'id': 1, 'name': 'aaa', 'age': 15},
                             {'id': 2, 'name': 'bbb', 'age': 20, 'children': [
                                 {'id': 3, 'name': 'ccc', 'age': 20, 'children':[
                                     {'id': 4, 'name': 'ccc', 'age': 20},
                                     {'id': 5, 'name': 'ccc', 'age': 20}
                                 ]},
                             ]},

                           ]
    result_three_level = multi_tree_dict(test_data_three_level, main_key_field_name='id', parent_key_field_name='parent_id')
    print('->', result_three_level)

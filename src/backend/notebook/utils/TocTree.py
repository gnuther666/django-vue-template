from typing import Union
from treelib import Node, Tree
import json
from pprint import pprint
import pickle
import binascii

class MyTocTree:
    def __init__(self, tree:Tree):
        if isinstance(tree, Tree):
            self.tree = tree
        elif tree is None:
            self.tree = Tree()
        else:
            self.loadSaveStr(tree)

    def addDocToToc(self, doc_name:str, doc_id:int, parent = None):
        if parent is None:
            self.tree.create_node(doc_name, doc_id)
        else:
            self.tree.create_node(doc_name, doc_id, parent=parent)


    def TocToJson(self):
        data = self.tree.to_json()
        print(type(data))
        return data

    def JsonToTocTree(self, data) -> Tree :
        tree_dict = json.loads(data)
        tree = Tree()
        tree.from_map(tree_dict)
        return tree

    def findNodeWithId(self, doc_id:int) -> Union[Node, None]:
        return self.tree.get_node(doc_id)

    def getNodeAllChildrens(self, doc_id:int):
        return [one_node for one_node in self.tree.children(doc_id)]

    def renameDocName(self, doc_id:int, new_name:str):
        node = self.tree.get_node(doc_id)
        node.tag = new_name

    def deleteDoc(self, doc_id:int):
        self.tree.remove_node(doc_id)
        
    def toFrontEndFormat(self, node=None):
        if node is None:
            node = self.tree[self.tree.root]
        if node.is_leaf():
            return {'id': node.identifier, 'label': node.tag, 'type': None}
        chidren = [self.toFrontEndFormat(one_node) for one_node in self.tree.children(node.identifier)]
        return {'id': node.identifier, 'label': node.tag, 'type': None, 'children': chidren}

    def moveDocTo(self, doc_id:int, new_parent_id:int):
        self.tree.move_node(doc_id, new_parent_id)

    def toSaveStr(self):
        pickle_data = pickle.dumps(self.tree)
        hex_data = binascii.hexlify(pickle_data).decode()
        return hex_data
    
    def loadSaveStr(self, hex_data:str):
        pickle_data = binascii.unhexlify(hex_data.encode())
        ori_data = pickle.loads(pickle_data)
        self.tree = ori_data

    def is_tree_empty(self):
        return not bool(self.tree.root)
    

def test():
    tree = Tree()
    mTree = MyTocTree(tree)
    mTree.addDocToToc('test1', 11)
    mTree.addDocToToc('test2', 12, 11)
    mTree.addDocToToc('test3', 13, 11)
    mTree.addDocToToc('test4', 19, 13)
    mTree.addDocToToc('test5', 18, 13)
    mTree.addDocToToc('test88', 88, 12)
    mTree.addDocToToc('test89', 89, 12)
    mTree.addDocToToc('test90', 90, 88)
    search_node = mTree.findNodeWithId(13)
    print('搜索节点', type(search_node), search_node)
    childrens = mTree.getNodeAllChildrens(13)
    print('子节点',  childrens)
    mTree.renameDocName(13, 'test_new_13')
    print('重命名', mTree.TocToJson())
    tree_str = mTree.TocToJson()
    mTree.deleteDoc(88)
    print('删除', mTree.TocToJson())
    print('前端格式')
    pprint(mTree.toFrontEndFormat())
    print('移动节点')
    mTree.moveDocTo(13, 12)
    pprint(mTree.toFrontEndFormat())
    auto_save_str = mTree.toSaveStr()
    print('自动保存', auto_save_str)
    print('加载自动保存', MyTocTree(auto_save_str))

    print('\n\n测试阶段2')
    mTree2 = MyTocTree(None)
    print('是否为空', mTree2.is_tree_empty())
    out_toc = mTree2.toSaveStr()
    print('导入一个新树', out_toc)
    mTree3 = MyTocTree(out_toc)
    print('是否为空2', mTree3.is_tree_empty())

def test2():
    in_str1 = '80049569000000000000008c0c747265656c69622e74726565948c04547265659493942981947d94288c0b5f6964656e746966696572948c2431313539623835652d313163372d313165662d613436302d303234326230303030303032948c065f6e6f646573947d948c04726f6f74944e75622e'
    mTree1 = MyTocTree(in_str1)
    print(mTree1.tree.show())
    print(mTree1.toFrontEndFormat())

if __name__ == '__main__':
    test2()
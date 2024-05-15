from rest_framework import serializers
from notebook.models.user_books import BookTocModel, BookDocsModel
from rest_framework import viewsets
import logging
from rest_framework.permissions import IsAuthenticated
from util.response import CommonResponse
from rest_framework.decorators import action
from notebook.utils.TocTree import MyTocTree

logger = logging.getLogger('django')

class BookTocSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookTocModel
        fields = '__all__'


class BookTocViewset(viewsets.ModelViewSet):
    queryset = BookTocModel.objects.all()
    serializer_class = BookTocSerializer
    permission_classes = (IsAuthenticated,)  # 如果允许匿名用户访问则修改这里
    
    @action(methods=['GET'], detail=False)
    def get_tocs(self, request, *args, **kwargs):
        user = request.user
        book_id = request.GET.get('book_id')
        book = BookTocModel.objects.filter(book_id=book_id).first()
        if book:
            tree_obj = MyTocTree(book.toc)
            logger.error(f'tree_str:{tree_obj.toSaveStr()}')
            return CommonResponse(data={'msg': '获取成功', 'data': tree_obj.toFrontEndFormat()}, code=200)
        else:
            return CommonResponse(data={'msg': '获取成功', 'data': None}, code=200)

    
    @action(methods=['POST'], detail=False)
    def add_note(self, request, *args, **kwargs):
        user = request.user
        
        parent_id = request.data.get('parent_id', 0)
        book_id = request.data['book_id']
        title = request.data['title']
        type = request.data['type']
        doc = BookDocsModel()
        doc.title = title
        doc.content = 'empty'
        doc.book_id = book_id
        doc.save()
        precheck_toc = BookTocModel.objects.filter(book_id=book_id).first()
        if not precheck_toc:
            precheck_toc = BookTocModel()
            precheck_toc.book_id = book_id
            precheck_toc.toc = MyTocTree(None).toSaveStr()
            precheck_toc.save()
        precheck_tree = MyTocTree(precheck_toc.toc)
    
        if parent_id == 0:
            if not precheck_tree.is_tree_empty():
                return CommonResponse(data={'msg': '目录不为空，不能从根目录进行创建', 'data': None}, code=201)
            precheck_tree.addDocToToc(title, doc.id)
            precheck_toc.toc = precheck_tree.toSaveStr()
            precheck_toc.save() 
            resp = CommonResponse(data={'msg': '增加成功', 'data': precheck_tree.toFrontEndFormat()}, code=200)
            return resp
        else:
            node = precheck_tree.findNodeWithId(parent_id)
            if node is None:
                return CommonResponse(data={'msg': '未找到父级目录', 'data': None}, code=201)
            precheck_tree.addDocToToc(title, doc.id, parent_id)
            precheck_toc.toc = precheck_tree.toSaveStr()
            precheck_toc.save()
            resp = CommonResponse(data={'msg': '增加成功', 'data': precheck_tree.toFrontEndFormat()}, code=200) #
            return resp
    
    @action(methods=['POST'], detail=False)
    def delete_note(self, request, *args, **kwargs):
        user = request.user
        book_id = request.data['book_id']
        doc_id = request.data['doc_id']
        toc_model_obj = BookTocModel.objects.filter(book_id=book_id).first()
        toc_tree_obj = MyTocTree(toc_model_obj.toc)
        need_delete_doc_id = [one.identifier for one in toc_tree_obj.getNodeAllChildrens(doc_id)]
        BookDocsModel.objects.filter(id__in=need_delete_doc_id).delete()
        toc_tree_obj.deleteDoc(doc_id)
        logger.debug(toc_tree_obj.toFrontEndFormat()) 
        toc_model_obj.toc = toc_tree_obj.toSaveStr()
        toc_model_obj.save()
        resp = CommonResponse(data={'msg': '删除成功', 'data': need_delete_doc_id}, code=200)
        return resp
    
    @action(methods=['POST'], detail=False)
    def rename_note(self, request, *args, **kwargs):
        user = request.user
        book_id = request.data['book_id']
        doc_id = request.data['doc_id']
        title = request.data['title']
        toc_model_obj = BookTocModel.objects.filter(book_id=book_id).first()
        toc_tree_obj = MyTocTree(toc_model_obj.toc)
        toc_tree_obj.renameDocName(doc_id, title)
        toc_model_obj.toc = toc_tree_obj.toSaveStr()
        toc_model_obj.save()
        return CommonResponse(data={'msg': '修改成功:%s' % (request.data['book_id'], ), 'data': None}, code=200)
    
    @action(methods=['POST'], detail=False)
    def move_note(self, request, *args, **kwargs):
        user = request.user
        book_id = request.data['book_id']
        doc_id = request.data['doc_id']
        parent_id = request.data['parent_id']
        toc_model_obj = BookTocModel.objects.filter(book_id=book_id).first()
        toc_tree_obj = MyTocTree(toc_model_obj.toc)
        toc_tree_obj.moveDocTo(doc_id, parent_id)
        toc_model_obj.toc = toc_tree_obj.toSaveStr()
        toc_model_obj.save()
        return CommonResponse(data={'msg': '修改成功:%s' % (request.data['book_id'], ), 'data': None}, code=200)
    
    
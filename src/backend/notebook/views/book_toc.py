from rest_framework import serializers
from notebook.models.user_books import BookTocModel, BookDocsModel
from rest_framework import viewsets
import logging
from rest_framework.permissions import IsAuthenticated
from util.response import CommonResponse
from rest_framework.decorators import action
from notebook.utils.findDocWithId import findDocWithId

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
        book = BookTocModel.objects.filter(book_id=request.GET.get('book_id')).first()
        if book:
            return CommonResponse(data={'msg': '获取成功', 'data': book.toc}, code=200)
        else:
            toc = BookTocModel()
            toc.toc = {}
            toc.book_id = request.GET.get('book_id')
            toc.save()
            return CommonResponse(data={'msg': '获取成功', 'data': toc.toc}, code=200)

    
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

        if parent_id == 0:
            toc_data = {
                'id': doc.id,
                'type': type,
                'label': title,
            }
            toc_obj, _ = BookTocModel.objects.update_or_create(book_id=book_id,
                                                            defaults={'toc': toc_data})
            
            resp = CommonResponse(data={'msg': '增加成功', 'data': toc_obj.toc}, code=200)
            return resp
        else:
            ori_toc_obj = BookTocModel.objects.filter(book_id=book_id).first()
            if not ori_toc_obj:
                return CommonResponse(data={'msg': '未找到目录文件', 'data': None}, code=201)
            ori_toc = ori_toc_obj.toc
            insert_node = findDocWithId(ori_toc, parent_id)
            if insert_node is None:
                return CommonResponse(data={'msg': f'未找到指定节点 book_id:{book_id}, parent_id:{parent_id}', 'data': None}, code=201)
            if insert_node.get('children') is None:
                insert_node['children'] = []
            insert_node['children'].append({
                'id': doc.id,
                'type': type,
                'label': title,
            })
            ori_toc_obj.toc = ori_toc
            ori_toc_obj.save()
            resp = CommonResponse(data={'msg': '增加成功', 'data': ori_toc_obj.toc}, code=200) #
            return resp
    
    @action(methods=['POST'], detail=False)
    def delete_book(self, request, *args, **kwargs):
        user = request.user
        book_id = request.data['book_id']
        book = UserBooksModel.objects.filter(user_id=user.id, id=book_id).delete()
        resp = CommonResponse(data={'msg': '删除成功', 'data': None}, code=200)
        return resp
    
    @action(methods=['POST'], detail=False)
    def update_book(self, request, *args, **kwargs):
        user = request.user
        book = UserBooksModel.objects.filter(user_id=user.id, id=request.data['book_id']).first()
        if book:
            book.book_name = request.data['book_name']
            book.save()
            return CommonResponse(data={'msg': '修改成功:%s' % (request.data['book_id'], ), 'data': {'id': book.id, 'book_name': book.book_name}}, code=200)
        else:
            return CommonResponse(data={'msg': '未找到对应笔记簿:%s' % (request.data['book_id'], ), 'data': None}, code=201)
    
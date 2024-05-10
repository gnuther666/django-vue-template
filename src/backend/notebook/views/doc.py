from rest_framework import serializers
from notebook.models.user_books import BookDocsModel
from rest_framework import viewsets
import logging
from rest_framework.permissions import IsAuthenticated
from util.response import CommonResponse
from rest_framework.decorators import action

logger = logging.getLogger('django')

class BookDocserializer(serializers.ModelSerializer):

    class Meta:
        model = BookDocsModel
        fields = '__all__'


class BookDocViewset(viewsets.ModelViewSet):
    queryset = BookDocsModel.objects.all()
    serializer_class = BookDocserializer
    permission_classes = (IsAuthenticated,)  # 如果允许匿名用户访问则修改这里
    
    @action(methods=['GET'], detail=False)
    def get_doc_content(self, request, *args, **kwargs):
        doc_id = request.GET.get('doc_id')
        is_valid, doc = self.check_doc_id_valid(doc_id)
        if not is_valid:
            return doc
        return CommonResponse(data={'msg': '获取成功', 'data': doc.content}, code=200)
    
    @action(methods=['POST'], detail=False)
    def save_content(self, request, *args, **kwargs):        
        doc_id = request.data['doc_id']
        doc_content = request.data['doc_content']
        is_valid, doc = self.check_doc_id_valid(doc_id)
        if not is_valid:
            return doc
        doc.content = doc_content
        doc.save()
        resp = CommonResponse(data={'msg': '获取成功', 'data': None}, code=200)
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
        
    def check_doc_id_valid(self, doc_id):
        if not doc_id:
            return False, CommonResponse(data={'msg': '参数错误, 缺少doc_id', 'data': None}, code=400)
        doc = BookDocsModel.objects.filter(id=doc_id).first()
        if not doc:
            return False, CommonResponse(data={'msg': '文档不存在', 'data': None}, code=400)
        return True, doc
    
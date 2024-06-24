from rest_framework import serializers
from notebook.models.user_books import UserBooksModel
from rest_framework import viewsets
import logging
from rest_framework.permissions import IsAuthenticated
from public_tools.tools.response import CommonResponse
from rest_framework.decorators import action

logger = logging.getLogger('django')

class UserBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserBooksModel
        fields = '__all__'


class UserBookViewset(viewsets.ModelViewSet):
    queryset = UserBooksModel.objects.all()
    serializer_class = UserBookSerializer
    permission_classes = (IsAuthenticated,)  # 如果允许匿名用户访问则修改这里
    
    @action(methods=['GET'], detail=False)
    def get_books(self, request, *args, **kwargs):
        user = request.user
        books = UserBooksModel.objects.filter(user_id=user.id).all()
        datas = {one.id: one.book_name for one in books}
        resp = CommonResponse(data={'msg': '获取成功', 'data': datas}, code=200)
        return resp
    
    @action(methods=['POST'], detail=False)
    def add_books(self, request, *args, **kwargs):
        user = request.user
        
        book_name = request.data['book_name']
        book = UserBooksModel()
        book.user = user
        book.book_name = book_name
        book.save()
        datas = {'id': book.id, 'book_name': book.book_name}
        resp = CommonResponse(data={'msg': '获取成功', 'data': datas}, code=200)
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
    
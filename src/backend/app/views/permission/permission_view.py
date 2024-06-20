import logging, os
from app.views.permission.permission_serializer import PermissionSerializer
from app.models.app_user import AppUserModel
from rest_framework import viewsets
from rest_framework.decorators import action
from util.response import CommonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from public_tools.tools.read_env import GetEnv, get_web_res_web_url
from util.file_process import UserFileProcess
from app.models import AuthGroupExpander
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

logger = logging.getLogger('app')

class PermissionViewset(viewsets.ModelViewSet):
    queryset = AppUserModel.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = (IsAuthenticated, )

    @action(methods=['GET'], detail=False)
    def get_auth_groups(self, request, *args, **kwargs):
        values = AuthGroupExpander.objects.values('group_id', 'group__name', 'outer_name', 'description').all()
        return CommonResponse(data={'data': [dict(one) for one in values], 'msg': f'success'})
    
    @action(methods=['POST', ], detail=False)
    def set_auth_group_info(self, request, *args, **kwargs):
        obj = AuthGroupExpander.objects.get(group_id=request.data['group_id'])
        obj.outer_name = request.data['outer_name']
        obj.description = request.data['description']
        obj.save()
        data = {'group_id': obj.group_id, 'group__name': request.data['group_name'],
                'outer_name': request.data['outer_name'], 'description': request.data['description']}
        return CommonResponse(data={'msg': 'success', 'data': data}, code=200)

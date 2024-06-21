import logging, os
from app.views.permission.permission_serializer import PermissionSerializer
from app.models.app_user import AppUserModel
from rest_framework import viewsets
from rest_framework.decorators import action
from util.response import CommonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models.query import QuerySet
from public_tools.tools.read_env import GetEnv, get_web_res_web_url
from util.file_process import UserFileProcess
from app.models import AuthGroupExpander
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from app.Permissions import AppPermissions

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

    @action(methods=['GET'], detail=False)
    def get_could_auth_permissions(self, request, *args, **kwargs):
        datas = [{'name':one.name, 'value': one.value } for one in AppPermissions]
        return CommonResponse(data={'msg': 'success', 'data': datas})

    @action(methods=['GET'], detail=False)
    def get_group_permissions(self, request, *args, **kwargs):
        group_id = request.GET.get('group_id', None)
        group_obj = Group.objects.get(id=group_id)
        permissions = group_obj.permissions.all()
        datas = [{'value': one.id, 'name': one.name} for one in permissions]
        return CommonResponse(data={'msg': 'success', 'data': datas})

    @action(methods=['POST', ], detail=False)
    def add_groups_permission(self, request, *args, **kwargs):
        group_id = request.data['group_id']
        permissions = request.data['permissions']
        permission_objs = Permission.objects.filter(codename__in=permissions)
        group = Group.objects.get(id=group_id)
        logger.debug('add group %s, permission %s', group, type(permission_objs))
        group.permissions.add(*permission_objs)
        group.save()
        return CommonResponse(data={'msg': 'success', 'data': 'success'})

    @action(methods=['POST', ], detail=False)
    def del_groups_permission(self, request, *args, **kwargs):
        group_id = request.data['group_id']
        permissions = request.data['permissions']
        permission_objs = Permission.objects.filter(id__in=permissions)
        group = Group.objects.get(id=group_id)
        for permission in permission_objs:
            logger.debug('remove group %s, permission %s', group, permission)
            group.permissions.remove(permission)
        group.save()
        return CommonResponse(data={'msg': 'success', 'data': 'success'})


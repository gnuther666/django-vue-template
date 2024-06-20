from django.db import models
from django.contrib.auth.models import Group
from app.Permissions import AppAuthGroup

class AuthGroupExpander(models.Model):
    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    description = models.TextField(blank=True, null=True)
    outer_name = models.CharField(max_length=255, blank=True, null=True)

    @staticmethod
    def init():
        for one_group in AppAuthGroup:
            group_obj = Group.objects.filter(name=one_group.name).first()
            if group_obj:
                continue
            group_obj = Group()
            group_obj.name = one_group.name
            group_obj.save()
            expander_obj = AuthGroupExpander()
            expander_obj.group = group_obj
            expander_obj.description = one_group.value[1]
            expander_obj.outer_name = one_group.value[0]
            expander_obj.save()
    class Meta:
        verbose_name = 'Group Extension'
        verbose_name_plural = 'Group Extensions'
        db_table = 'auth_group_expander'

    def __str__(self):
        return self.group.name
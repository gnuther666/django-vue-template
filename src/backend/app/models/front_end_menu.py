from django.db import models



class FrontMenuModel(models.Model):
    item_key = models.CharField(max_length=25, primary_key=True, verbose_name='item key')
    item_title = models.CharField(max_length=100, verbose_name='item title')
    item_url = models.CharField(max_length=100, null=False, verbose_name='item url')
    father_menu_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, default=None, verbose_name='father menu id')
    sort_seq = models.IntegerField(default=0, verbose_name='sort seq')
    is_active = models.BooleanField(default=True, null=False, verbose_name='active')
    item_description = models.TextField(default=None, null=True, verbose_name='item description')
    class Meta:
        db_table = 'front_end_menu'
        ordering = ['sort_seq']
        verbose_name = 'front-end menu'






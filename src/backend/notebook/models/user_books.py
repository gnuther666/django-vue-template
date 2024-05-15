from django.db import models

class UserBooksModel(models.Model):
    user = models.ForeignKey('app.AppUserModel', on_delete=models.CASCADE)
    book_name = models.CharField(max_length=128, null=False, verbose_name='笔记本名称')

    def delete(self, using=None, keep_parents=False):
        BookDocsModel.objects.filter(book_id=self.id).delete()
        BookTocModel.objects.filter(book_id=self.id).delete()
        super().delete(using, keep_parents)

    class Meta:
        db_table = 'notebook_book'
        ordering = ['id']
        verbose_name = '笔记本'

class BookDocsModel(models.Model):
    book = models.ForeignKey(UserBooksModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, null=False, verbose_name='标题')
    content = models.TextField(null=False, verbose_name='内容')

    class Meta:
        db_table = 'notebook_docs'
        ordering = ['id']
        verbose_name = '笔记'

class BookTocModel(models.Model):
    book = models.ForeignKey(UserBooksModel, on_delete=models.CASCADE, unique=True)
    toc = models.TextField(null=True, verbose_name='目录')

    class Meta:
        db_table = 'notebook_toc'
        ordering = ['id']
        verbose_name = '目录'

class DocImages(models.Model):
    book = models.ForeignKey(UserBooksModel, on_delete=models.CASCADE)
    doc = models.ForeignKey(BookDocsModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='doc_images', null=True, verbose_name='图片')
    create_time = models.DateTimeField(auto_now=True)
    enable = models.BooleanField(default=True)

    class Meta:
        db_table = 'notebook_images'
        ordering = ['id']
        verbose_name = '图片'
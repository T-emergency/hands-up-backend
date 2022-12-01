from django.db import models
from user.models import User


class FreeArticle(models.Model):

    title = models.CharField('제목', null=True, max_length=20)
    content = models.TextField('내용', null=True, max_length=200)
    created_at = models.DateTimeField('생성 시간', auto_now_add=True)
    updated_at = models.DateTimeField('수정 시간', auto_now=True)
    image = models.ImageField(upload_to='', null=True, blank=True)
    author = models.ForeignKey(
        User, verbose_name='작성자', on_delete=models.CASCADE)

    class Meta:
        db_table = 'FreeArticle'
        ordering = ['id']

    def __str__(self):
        return str(self.title)


class ReportArticle(models.Model):

    title = models.CharField('제목', null=True, max_length=20)
    content = models.TextField('내용', null=True, max_length=200)
    created_at = models.DateTimeField('생성 시간', auto_now_add=True)
    updated_at = models.DateTimeField('수정 시간', auto_now=True)
    image = models.ImageField(upload_to='', null=True, blank=True)
    author = models.ForeignKey(
        User, verbose_name='작성자', on_delete=models.CASCADE)

    class Meta:
        db_table = 'ReportArticle'
        ordering = ['id']

    def __str__(self):
        return str(self.title)


class FreeArticleComment(models.Model):

    content = models.TextField('내용', max_length=200)
    create_at = models.DateTimeField('생성 시간', auto_now_add=True)
    update_at = models.DateTimeField('수정 시간', auto_now=True)
    author = models.ForeignKey(
        User, verbose_name='작성자', on_delete=models.CASCADE)

    article = models.ForeignKey(
        FreeArticle, verbose_name='제품게시글', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.content)

    class Meta:
        db_table = 'FreeArticleComment'
        ordering = ['-created_at']


class ReportArticleComment(models.Model):

    content = models.TextField('내용', max_length=200)
    create_at = models.DateTimeField('생성 시간', auto_now_add=True)
    update_at = models.DateTimeField('수정 시간', auto_now=True)
    author = models.ForeignKey(
        User, verbose_name='작성자', on_delete=models.CASCADE)

    article = models.ForeignKey(
        ReportArticle, verbose_name='제품게시글', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.content)

    class Meta:
        db_table = 'ReportArticleComment'
        ordering = ['-created_at']

from django.contrib import admin
from .models import FreeArticle, FreeArticleComment, ReportArticle, ReportArticleComment
# Register your models here.
admin.site.register(FreeArticle)
admin.site.register(FreeArticleComment)
admin.site.register(ReportArticle)
admin.site.register(ReportArticleComment)

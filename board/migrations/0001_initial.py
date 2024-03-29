# Generated by Django 4.1.3 on 2022-12-22 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FreeArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='제목')),
                ('content', models.TextField(blank=True, max_length=2000, null=True, verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 시간')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('hits', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'db_table': 'FreeArticle',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ReportArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='제목')),
                ('content', models.TextField(blank=True, max_length=2000, null=True, verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 시간')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'db_table': 'ReportArticle',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ReportArticleComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=200, verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='board.reportarticle', verbose_name='제품게시글')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'db_table': 'Reportcomment',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FreeArticleComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=200, verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 시간')),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='board.freearticle', verbose_name='제품게시글')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'db_table': 'Freecomment',
                'ordering': ['-created_at'],
            },
        ),
    ]

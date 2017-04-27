# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class UserProfile(AbstractUser):
    # avatar = models.ImageField(_(u'avatar'), upload_to='accounts/avatar/%Y/%m/', blank=True, max_length=1000)
    contents = models.TextField(verbose_name=u'Информация о пользователе', blank=True, null=True)
    birth_date = models.DateField(verbose_name=u'Дата рождения', null=True, blank=True)


class Like(models.Model):
    author = models.ForeignKey(to='text.UserProfile')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    like_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = ['content_type', 'object_id']


class Text(models.Model):
    title = models.CharField(verbose_name=u'Название', max_length=200)
    author = models.ForeignKey(verbose_name=u'Автор', to='text.UserProfile', blank=True, null=True)#, related_name="texts")
    TYPE_CHOICE = (
        (0, u'Стих'),
        (1, u'Рассказ'),
        (2, u'Повесть')
    )
    text_type = models.IntegerField(verbose_name=u'Тип произведения', choices=TYPE_CHOICE)
    created_at = models.DateField(verbose_name=u'Дата написания', blank=True, null=True, db_index=True)
    contents = models.TextField(verbose_name=u'Текст произведения')
    views = models.IntegerField(verbose_name=u'Просмотры')
    
    class Meta:
        ordering = ('created_at', )
        verbose_name = u'Текст'
        verbose_name_plural = u'Тексты'

    likes = GenericRelation(Like, object_id_field='object_id')

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(verbose_name=u'Автор', to='text.UserProfile')
    post = models.ForeignKey(verbose_name=u'Текст', to='text.Text')
    created_date = models.DateTimeField(verbose_name=u'Время написания', auto_now_add=True)
    contents = models.TextField(verbose_name=u'Комментарий', blank=True, null=True)

    class Meta:
        # ordering = ('created_at', )
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'

    likes = GenericRelation(Like, object_id_field='object_id')
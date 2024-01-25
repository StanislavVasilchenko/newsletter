from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Статья')
    image = models.ImageField(upload_to='blog/%Y/%m/%d', blank=True, null=True)
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    is_published = models.BooleanField(default=False, verbose_name='Опубликованно')

    def __str__(self):
        return f'{self.title} - {self.views} - {self.pub_date}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

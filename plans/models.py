from django.db import models
from django.conf import settings


class Place(models.Model):
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='添加者')
    name = models.CharField('地点名称', max_length=100)
    description = models.TextField('描述', blank=True)
    image = models.ImageField('图片', upload_to='travel/', blank=True)
    rating = models.IntegerField('想去程度', default=3, choices=[(i, '⭐' * i) for i in range(1, 6)])
    location = models.CharField('城市/区域', max_length=100, blank=True)
    is_visited = models.BooleanField('已去过', default=False)
    visited_photo = models.ImageField('打卡照片', upload_to='travel/visited/', blank=True)
    visited_date = models.DateField('打卡日期', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '想去的地方'
        verbose_name_plural = '想去的地方'
        ordering = ['-rating', '-created_at']

    def __str__(self):
        return self.name


class Movie(models.Model):
    TYPE_CHOICES = [
        ('movie', '🎬 电影'),
        ('tv', '📺 电视剧'),
        ('variety', '🎭 综艺'),
        ('anime', '🎌 动漫'),
    ]
    STATUS_CHOICES = [
        ('want', '想看'),
        ('watching', '在看'),
        ('done', '看完'),
    ]

    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='添加者')
    title = models.CharField('片名', max_length=200)
    movie_type = models.CharField('类型', max_length=20, choices=TYPE_CHOICES, default='movie')
    poster = models.ImageField('海报', upload_to='posters/', blank=True)
    description = models.TextField('简介', blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='want')
    rating = models.IntegerField('评分', null=True, blank=True,
                                  choices=[(i, '⭐' * i) for i in range(1, 6)])
    review = models.TextField('评价', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '观影清单'
        verbose_name_plural = '观影清单'
        ordering = ['status', '-created_at']

    def __str__(self):
        return f'{self.get_movie_type_display()} - {self.title}'

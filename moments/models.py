from django.db import models
from django.conf import settings


class Post(models.Model):
    MOOD_CHOICES = [
        ('happy', '😊 开心'),
        ('love', '🥰 恋爱'),
        ('miss', '🥺 想念'),
        ('grateful', '🙏 感恩'),
        ('calm', '😌 平静'),
        ('excited', '🤩 兴奋'),
        ('sad', '😢 难过'),
        ('angry', '😤 生气'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='作者')
    content = models.TextField('内容')
    mood = models.CharField('心情', max_length=20, choices=MOOD_CHOICES, blank=True)
    location = models.CharField('位置', max_length=100, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = '帖子'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author} - {self.content[:20]}'


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name='帖子')
    image = models.ImageField('图片', upload_to='posts/')
    thumbnail = models.ImageField('缩略图', upload_to='posts/thumbs/', blank=True)
    order = models.IntegerField('排序', default=0)

    class Meta:
        verbose_name = '帖子图片'
        verbose_name_plural = '帖子图片'
        ordering = ['order']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='帖子')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='作者')
    content = models.TextField('内容')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='replies', verbose_name='回复')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author} - {self.content[:20]}'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name='帖子')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = '点赞'
        unique_together = ['post', 'user']

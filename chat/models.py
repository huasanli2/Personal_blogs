from django.db import models
from django.conf import settings


class Message(models.Model):
    MESSAGE_TYPES = [
        ('text', '文本'),
        ('image', '图片'),
        ('emoji', '表情'),
        ('system', '系统'),
    ]

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='发送者')
    content = models.TextField('内容', blank=True)
    message_type = models.CharField('消息类型', max_length=10, choices=MESSAGE_TYPES, default='text')
    image = models.ImageField('图片', upload_to='chat/', blank=True)
    is_read = models.BooleanField('已读', default=False, db_index=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = '消息'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender}: {self.content[:20]}'

from django.db import models
from django.conf import settings


class FoodLog(models.Model):
    MEAL_CHOICES = [
        ('breakfast', '🌅 早餐'),
        ('lunch', '☀️ 午餐'),
        ('dinner', '🌙 晚餐'),
        ('snack', '🍰 加餐'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='作者')
    meal_type = models.CharField('餐次', max_length=20, choices=MEAL_CHOICES)
    title = models.CharField('菜名', max_length=100)
    description = models.TextField('描述', blank=True)
    image = models.ImageField('照片', upload_to='food/', blank=True)
    location = models.CharField('餐厅/地点', max_length=100, blank=True)
    date = models.DateField('日期')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '美食日记'
        verbose_name_plural = '美食日记'
        ordering = ['-date', 'meal_type']

    def __str__(self):
        return f'{self.get_meal_type_display()} - {self.title}'


class FoodLike(models.Model):
    food = models.ForeignKey(FoodLog, on_delete=models.CASCADE, related_name='likes', verbose_name='美食')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '美食点赞'
        verbose_name_plural = '美食点赞'
        unique_together = ['food', 'user']


class DailyLog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='作者')
    content = models.TextField('今天干了啥')
    mood = models.CharField('心情', max_length=10, blank=True, help_text='输入一个 emoji')
    image = models.ImageField('照片', upload_to='daily/', blank=True)
    date = models.DateField('日期')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '每日日记'
        verbose_name_plural = '每日日记'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.author} - {self.date} - {self.content[:20]}'


class Whisper(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='作者')
    content = models.TextField('悄悄话')
    image = models.ImageField('图片', upload_to='whispers/', blank=True)
    is_anonymous = models.BooleanField('匿名', default=False)
    visible_at = models.DateTimeField('定时显示', null=True, blank=True,
                                       help_text='留空则立即显示')
    is_read = models.BooleanField('已读', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '悄悄话'
        verbose_name_plural = '悄悄话'
        ordering = ['-created_at']

    def __str__(self):
        return f'悄悄话 - {self.content[:20]}'

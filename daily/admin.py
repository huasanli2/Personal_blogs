from django.contrib import admin
from .models import FoodLog, FoodLike, DailyLog, Whisper


@admin.register(FoodLog)
class FoodLogAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'meal_type', 'date']


@admin.register(FoodLike)
class FoodLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'food', 'created_at']


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ['author', 'content', 'mood', 'date']


@admin.register(Whisper)
class WhisperAdmin(admin.ModelAdmin):
    list_display = ['author', 'content', 'is_anonymous', 'is_read', 'created_at']

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from .models import FoodLog, FoodLike, DailyLog, Whisper


@login_required
def food_list(request):
    date_str = request.GET.get('date')
    if date_str:
        from datetime import date
        try:
            selected_date = date.fromisoformat(date_str)
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()

    foods = FoodLog.objects.filter(date=selected_date).select_related('author').prefetch_related('likes')
    return render(request, 'daily/food_list.html', {
        'foods': foods,
        'selected_date': selected_date,
    })


@login_required
def food_create(request):
    if request.method == 'POST':
        food = FoodLog.objects.create(
            author=request.user,
            meal_type=request.POST.get('meal_type', 'lunch'),
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
            location=request.POST.get('location', ''),
            date=request.POST.get('date', timezone.now().date()),
            image=request.FILES.get('image'),
        )
        return redirect('daily:food_list')

    return render(request, 'daily/food_create.html')


@login_required
@require_POST
def food_like(request, pk):
    food = get_object_or_404(FoodLog, pk=pk)
    like, created = FoodLike.objects.get_or_create(food=food, user=request.user)
    if not created:
        like.delete()
    return redirect('daily:food_list')


@login_required
def journal_list(request):
    logs = DailyLog.objects.select_related('author').all()[:30]
    return render(request, 'daily/journal_list.html', {'logs': logs})


@login_required
def journal_create(request):
    if request.method == 'POST':
        DailyLog.objects.create(
            author=request.user,
            content=request.POST.get('content', ''),
            mood=request.POST.get('mood', ''),
            date=timezone.now().date(),
            image=request.FILES.get('image'),
        )
        return redirect('daily:journal_list')

    return render(request, 'daily/journal_create.html')


@login_required
def whisper_list(request):
    now = timezone.now()
    from django.db.models import Q
    whispers = Whisper.objects.filter(
        Q(visible_at__isnull=True) | Q(visible_at__lte=now)
    ).select_related('author').order_by('-created_at')

    # Batch update: mark all unread whispers from other users as read in one query
    Whisper.objects.filter(
        Q(visible_at__isnull=True) | Q(visible_at__lte=now),
        is_read=False
    ).exclude(author=request.user).update(is_read=True)

    return render(request, 'daily/whisper_list.html', {'whispers': whispers})


@login_required
def whisper_create(request):
    if request.method == 'POST':
        Whisper.objects.create(
            author=request.user,
            content=request.POST.get('content', ''),
            is_anonymous=request.POST.get('is_anonymous') == 'on',
            image=request.FILES.get('image'),
        )
        return redirect('daily:whisper_list')

    return render(request, 'daily/whisper_create.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from moments.models import Post


@login_required
def storage_list(request):
    query = request.GET.get('q', '')
    mood_filter = request.GET.get('mood', '')

    posts = Post.objects.select_related('author').prefetch_related('images')

    if query:
        posts = posts.filter(content__icontains=query)
    if mood_filter:
        posts = posts.filter(mood=mood_filter)

    moods = Post.MOOD_CHOICES

    return render(request, 'storage/list.html', {
        'posts': posts,
        'query': query,
        'mood_filter': mood_filter,
        'moods': moods,
    })

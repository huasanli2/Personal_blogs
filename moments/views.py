from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from .models import Post, PostImage, Comment, Like


@login_required
def home(request):
    posts = Post.objects.select_related('author').prefetch_related('images', 'comments__author', 'likes')
    if request.headers.get('HX-Request'):
        try:
            page = int(request.GET.get('page', 1))
        except (TypeError, ValueError):
            page = 1
        paginator = Paginator(posts, 10)
        if page < 1 or page > paginator.num_pages:
            return HttpResponse('')
        page_obj = paginator.page(page)
        html = ''
        for post in page_obj:
            html += render_to_string('moments/partials/post_card.html', {'post': post, 'user': request.user})
        return HttpResponse(html)
    return render(request, 'moments/home.html', {'posts': posts[:10]})


@login_required
def post_create(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if not content:
            return redirect('moments:home')

        post = Post.objects.create(
            author=request.user,
            content=content,
            mood=request.POST.get('mood', ''),
            location=request.POST.get('location', ''),
        )

        for i, img in enumerate(request.FILES.getlist('images')):
            PostImage.objects.create(post=post, image=img, order=i)

        return redirect('moments:home')

    return render(request, 'moments/post_create.html')


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        post.content = request.POST.get('content', '').strip()
        post.mood = request.POST.get('mood', '')
        post.location = request.POST.get('location', '')
        post.save()

        for i, img in enumerate(request.FILES.getlist('images')):
            PostImage.objects.create(post=post, image=img, order=i)

        return redirect('moments:post_detail', pk=post.pk)

    return render(request, 'moments/post_edit.html', {'post': post})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related('author').prefetch_related(
        'images', 'comments__author', 'likes'), pk=pk)
    return render(request, 'moments/post_detail.html', {'post': post})


@login_required
@require_POST
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    if request.headers.get('HX-Request'):
        response = HttpResponse()
        response['HX-Trigger'] = 'postDeleted'
        return response
    return redirect('moments:home')


@login_required
@require_POST
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()

    post.refresh_from_db()
    liked = post.likes.filter(user=request.user).exists()

    html = render_to_string('moments/partials/like_button.html', {
        'post': post, 'liked': liked, 'user': request.user
    })
    return HttpResponse(html)


@login_required
@require_POST
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    content = request.POST.get('content', '').strip()
    if content:
        Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
        )

    post.refresh_from_db()
    html = render_to_string('moments/partials/comments.html', {
        'post': post, 'user': request.user
    })
    return HttpResponse(html)


@login_required
@require_POST
def delete_image(request, pk):
    image = get_object_or_404(PostImage, pk=pk, post__author=request.user)
    image.delete()
    return HttpResponse('')

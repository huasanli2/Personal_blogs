from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Place, Movie


@login_required
def place_list(request):
    places = Place.objects.select_related('added_by').all()
    return render(request, 'plans/place_list.html', {'places': places})


@login_required
def place_create(request):
    if request.method == 'POST':
        Place.objects.create(
            added_by=request.user,
            name=request.POST.get('name', ''),
            description=request.POST.get('description', ''),
            location=request.POST.get('location', ''),
            rating=int(request.POST.get('rating', 3)),
            image=request.FILES.get('image'),
        )
        return redirect('plans:place_list')

    return render(request, 'plans/place_create.html')


@login_required
@require_POST
def place_visit(request, pk):
    place = get_object_or_404(Place, pk=pk)
    place.is_visited = not place.is_visited
    if place.is_visited:
        from django.utils import timezone
        place.visited_date = timezone.now().date()
        if 'visited_photo' in request.FILES:
            place.visited_photo = request.FILES['visited_photo']
    place.save()
    return redirect('plans:place_list')


@login_required
def movie_list(request):
    status_filter = request.GET.get('status', '')
    type_filter = request.GET.get('type', '')
    movies = Movie.objects.select_related('added_by').all()
    if status_filter:
        movies = movies.filter(status=status_filter)
    if type_filter:
        movies = movies.filter(movie_type=type_filter)
    return render(request, 'plans/movie_list.html', {
        'movies': movies,
        'status_filter': status_filter,
        'type_filter': type_filter,
    })


@login_required
def movie_create(request):
    if request.method == 'POST':
        Movie.objects.create(
            added_by=request.user,
            title=request.POST.get('title', ''),
            movie_type=request.POST.get('movie_type', 'movie'),
            description=request.POST.get('description', ''),
            poster=request.FILES.get('poster'),
        )
        return redirect('plans:movie_list')

    return render(request, 'plans/movie_create.html')


@login_required
@require_POST
def movie_update_status(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    new_status = request.POST.get('status')
    if new_status in ['want', 'watching', 'done']:
        movie.status = new_status
        if new_status == 'done':
            rating = request.POST.get('rating')
            if rating:
                movie.rating = int(rating)
            movie.review = request.POST.get('review', '')
        movie.save()
    return redirect('plans:movie_list')


@login_required
@require_POST
def place_delete(request, pk):
    place = get_object_or_404(Place, pk=pk)
    if place.added_by != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'permission denied'}, status=403)
    place.delete()
    if request.headers.get('HX-Request'):
        response = HttpResponse()
        response['HX-Trigger'] = 'placeDeleted'
        return response
    return redirect('plans:place_list')


@login_required
@require_POST
def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if movie.added_by != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'permission denied'}, status=403)
    movie.delete()
    if request.headers.get('HX-Request'):
        response = HttpResponse()
        response['HX-Trigger'] = 'movieDeleted'
        return response
    return redirect('plans:movie_list')

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from ReeldIn.globals import ALL_MOVIES
from recommendations.models import Movie
import json


# Create your views here.
def is_admin(user):
    return user.is_superuser


def index(request):

    # if user is not logged in, redirect to home page
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    return render(request, "dashboard/index.html")


def get_all_movies(request):
    all_movies = ALL_MOVIES

    return render(request, "dashboard/movies_list.html", {"movies": all_movies})


def get_movie(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except:
        # Movie id doesn't exist
        return render(request, "dashboard/404.html")

    return render(request, "dashboard/movie_details.html", {"movie": movie})


if settings.DEBUG:

    @user_passes_test(is_admin)
    def create_movie(request, movie_id):
        return render(request, "dashboard/404.html")

    @user_passes_test(is_admin)
    @user_passes_test(is_admin)
    def delete_movie(request):
        try:
            data = json.loads(request.body)
            movie_ids = data.get("movies_to_remove", [])
            if not movie_ids:
                return JsonResponse(
                    {"error": "No movies specified to delete"}, status=400
                )

            # Perform the deletion
            Movie.objects.filter(id__in=movie_ids).delete()
            return JsonResponse({"success": "Movies deleted successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @user_passes_test(is_admin)
    def update_movie(request, movie_id):
        return render(request, "dashboard/404.html")

else:
    # Define placeholder views or return 404 response if debug mode is disabled
    def create_movie(request, movie_id):
        return render(request, "404.html", status=404)

    def delete_movie(request, movie_id):
        return JsonResponse({"error": "Page not found"}, status=404)

    def update_movie(request, movie_id):
        return render(request, "404.html", status=404)

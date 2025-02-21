import csv
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from fuzzywuzzy import fuzz

from recommendations.choices import STREAMING, TRIGGERS
from recommendations.models import Movie

# Create your views here.


@staff_member_required
def delete_movies_view(request):
    return render(
        request,
        "dev_tools/delete_movies.html",
    )


@staff_member_required
def delete_movie(request):
    print("Deleting movies sent in POST request...")
    try:
        data = json.loads(request.body)
        movie_ids = data.get("movies_to_remove", [])
        if not movie_ids:
            print("No movies specified to delete")
            return JsonResponse({"error": "No movies specified to delete"}, status=400)

        # Perform the deletion
        Movie.objects.filter(id__in=movie_ids).delete()
        print("Movies deleted!")

        return JsonResponse({"success": "Movies deleted successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

from django.contrib import admin
from .models import Movie, Recommendation, RecentRecommendations

# Register your models here.

admin.site.register(Movie, admin.ModelAdmin)
admin.site.register(Recommendation, admin.ModelAdmin)
admin.site.register(RecentRecommendations, admin.ModelAdmin)

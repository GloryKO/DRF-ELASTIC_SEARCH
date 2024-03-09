from django.urls import path
from .views import *

urlpatterns = [
    path("user/<str:query>/", UserSearch.as_view()),
    path("category/<str:query>/", SearchCategories.as_view()),
    path("article/<str:query>/", SearchArticles.as_view()),
]
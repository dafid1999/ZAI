from django.urls import path

from filmy.views import szczegoly, wszystkie

urlpatterns = [
    path('wszystkie/', wszystkie),
    path('szczegoly/', szczegoly),
]

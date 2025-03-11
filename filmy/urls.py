from django.urls import path
from filmy.views import wszystkie, szczegoly

urlpatterns = [
    path('wszystkie/', wszystkie),
    path('szczegoly/<int:film_id>/', szczegoly)
]

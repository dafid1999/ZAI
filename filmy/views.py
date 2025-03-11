from django.http import HttpResponse

from filmy.models import Film


def wszystkie(request):
    return HttpResponse(["<h1>", [[f.id, f.tytul, f.rok] for f in Film.objects.all()], "</h1>"])


def szczegoly(request, film_id):
    f = Film.objects.get(id=film_id)
    return HttpResponse(
        "<h3> Tytuł filmu: {},</br> rok produkcji: {}, </br> data premiery: {}, </br> opis: {}, </br> punkty od widzów: {} </h3>"
        .format(f.tytul, f.rok, f.premiera, f.opis, f.imdb_pkts))

from django.http import HttpResponse


def wszystkie(request):
    return HttpResponse("<h1>Tu będzie wyświetlana lista filmów z bazy danych.</h1>")

def szczegoly(request):
    return HttpResponse("<h1>Tu będą wyświetlane szczególy wybranego filmu.</h1>")

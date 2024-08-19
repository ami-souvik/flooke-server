# from django.contrib import admin
from django.urls import path
from .v1 import urlpatterns as v1_urlpatterns

def create_urlpatters():
    urlpatterns = []
    for url in v1_urlpatterns:
        _url = list(url[1:])
        _url.insert(0, f'api/v1/{url[0]}')
        urlpatterns.append(path(*tuple(_url)))
    return urlpatterns

urlpatterns = [
    # path('admin/', admin.site.urls)
] + create_urlpatters()
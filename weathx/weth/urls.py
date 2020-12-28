from django.urls import path
from . import views
from weth.views import index

app_name="weathx"


urlpatterns = [
    # path("", index.as_view(),name= "index"),
    path("", views.index, name="index"),
    path("editing/", views.editing, name="editing"),
    path("index1/", views.index1, name="index1"),
    path("delete/", views.delete, name="delete"),
    path("autosuggest", views.autosuggest, name="autosuggest"),
]

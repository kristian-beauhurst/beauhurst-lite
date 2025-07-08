from django.urls import path
from .views import SearchView, RawSearchView, FilterConfigView

app_name = "search"

urlpatterns = [
    path("", SearchView.as_view(), name="search"),
    path("raw/", RawSearchView.as_view(), name="raw_search"),
    path(
        "config/filteroptions/",
        FilterConfigView.as_view(),
        name="filter_config",
    ),
]

from django.urls import path
from graph_api.views import GraphAPI
# from .views import filter, metric, topology

urlpatterns = [
    path("", GraphAPI.as_view()),
    # path("filter/", filter),
    # path("metric/", metric),
    # path("topology/", topology),
]

""" 
APP URLs
"""

from django.urls import path
# from django.urls.resolvers import URLPattern
from . import views

app_name = "first_app"
# reverse(app_name:path name)

urlpatterns = [
    path('first', views.first_view, name="first_view"),
    path('second', views.second_view, name="second_view"),
    path('third', views.third_view, name="third_view"),
    path('fourth', views.fourth_view, name="fourth_view")
]

import django
from django.urls import path

from .views import main, menu_view, main_view

urlpatterns = [
    path('<slug:menu_slug>/<path:p>/', menu_view, name='menu'),
    path('<slug:menu_slug>/', main_view, name='main'),
    path('', main, name='home'),
]

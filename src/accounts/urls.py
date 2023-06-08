from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('sign-up', views.sign_up, name='sign_up'),
    path('sign-in', views.sign_in, name='sign_in'),
    path('my-profile/<str:login>/', views.my_profile, name='my_profile'),
    path('my-profile/<str:login>/settings', views.settings, name='settings')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
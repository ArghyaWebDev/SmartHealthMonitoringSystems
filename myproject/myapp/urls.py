from django.urls import path, include

from backend.accounts import views
from .views import authView, home
urlpatterns= [ 
              path("accounts/", include("django.contrib.auth.urls")),
              path('',views.home ,name='home'),
            #   path('login/',views.login ,name='login'), 
            #   path('registration/',views.registration ,name='registration'),
              path("signup/", authView, name="authView"),
                path("accounts/", include("django.contrib.auth.urls")),
              ]
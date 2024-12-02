# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),  # Home page
#     path('login/', views.login, name='login'),  # Login page
#     # path('login/',views.login,name='login'),
#     path('logout/', views.logout, name='logout'),
#     path('registration/', views.registration, name='registration'),  # Registration page
#     path('healthinsights/',views.healthinsights,name='healthinsights'),
#     path('wellnesstracking/',views.wellnesstracking,name='wellnesstracking'),
#     path('dashboard/', views.dashboard, name='dashboard'), 
#     path("suggestions/", views.health_suggestions, name="suggestions"),
#     path('suggest-medicine/', views.suggest_medicine, name='suggest_medicine'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    # Home and Authentication
    path('', views.home, name='home'),  # Home page
    path('login/', views.login, name='login'),  # Login page
    path('logout/', views.logout, name='logout'),  # Logout
    path('registration/', views.registration, name='registration'),  # Registration page

    # Health and Wellness Features
    path('healthinsights/', views.healthinsights, name='healthinsights'),  # Health insights
    path('wellnesstracking/', views.wellnesstracking, name='wellnesstracking'),  # Wellness tracking
    path('suggestions/', views.health_suggestions, name='suggestions'),  # Health suggestions
    path('suggest-medicine/', views.suggest_medicine, name='suggest_medicine'),  # Medicine suggestions

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),  # User dashboard
]

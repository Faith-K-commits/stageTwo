from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('auth/register', views.register_user, name='register'),
    path('auth/login', views.login_user, name='login'),
    path('api/users/<str:id>/', views.get_user, name='user_detail'),
    path('api/organisations/', views.get_organisations, name='organisation_list'),
    path('api/organisations/<str:orgId>/', views.get_organisation, name='organisation_detail'),
    path('api/organisations/', views.create_organisation, name='create_organisation'),
    path('api/organisations/<str:orgId>/users', views.add_user_to_organisation, name='add_user_to_organisation'),

]

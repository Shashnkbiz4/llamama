from django.urls import path
from . import views

app_name = 'superadmin'

urlpatterns = [
    # Add your superadmin URLs here
    path('', views.index_view, name='index'),
    path('create_client_admin/', views.create_client_admin_view, name='create_client_admin'),
    path('login/', views.login_view, name='login'),

]
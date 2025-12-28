from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.note_list_view, name='list'),
    path('add/', views.note_create_view, name='add'),
    path('<int:pk>/edit/', views.note_update_view, name='edit'),
    path('<int:pk>/delete/', views.note_delete_view, name='delete'),
    # auth routes now inside notes namespace
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

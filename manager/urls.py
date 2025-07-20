from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='index'),  
   path('logout/', views.manager_logout, name='logout'),
    path('event/<int:event_id>/', views.view_event, name='view_event'),
     path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
]
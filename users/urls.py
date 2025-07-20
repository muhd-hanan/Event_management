from django.urls import path
from users import views

app_name = "users"


urlpatterns = [
   path('', views.index, name="index"),
   path('login/', views.login, name="login"),
   path('register/', views.register, name="register"),
   path('logout/', views.logout, name="logout"),

    path('createevent/', views.createevent, name='createevent'),
    path('manageevent/', views.manageevent, name='manageevent'),
    path('editevent/<int:id>/', views.editevent, name='editevent'),
    path('deleteevent/<int:id>/', views.deleteevent, name='deleteevent'),



    path('allevent/', views.allevent, name='allevent'),

    path('singleevent/<int:id>/', views.singleevent, name='singleevent'),
    path('registerevent/<int:id>/', views.register_event, name='register_event'),

      path('registeredevent/', views.registeredevent, name='registeredevent'),

      path('unregisterevent/<int:id>/', views.unregister_event, name='unregister_event'),




    path('singleeventstatus/<int:id>/', views.singleeventstatus, name='singleeventstatus'),
    path('delete-registration/<int:event_id>/<int:user_id>/', views.delete_registration, name='delete_registration'),

  ]
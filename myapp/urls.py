from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('chat/', views.chatbot_view, name='chatbot'),
    path('resources/',views.resources,name='resources'),
    path('profile/', views.my_profile, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('yoga/',views.yoga,name='yoga'),
    path('issues/',views.issues,name='issues'),
    path('anxietyissue/',views.anxietyissue,name='anxietyissue'),
    path('music/',views.music,name='music')
]




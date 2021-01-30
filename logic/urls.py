'''
* Grupo 1363
* Pareja 8
* File: urls.py
'''

from django.urls import path
from logic import views

urlpatterns = [
    path('', views.index_service, name='landing'),
    path('index/', views.index_service, name='index'),
    path('login/', views.login_service, name='login'),
    path('logout/', views.logout_service, name='logout'),
    path('signup/', views.signup_service, name='signup'),
    path('counter/', views.counter_service, name='counter'),
    path('create_game/', views.create_game_service, name='create_game'),
    path('join_game/', views.join_game_service, name='join_game'),
    path('join_game/<int:game_id>', views.join_game_service, name='join_game'),
    path('select_game/', views.select_game_service, name='select_game'),
    path('select_game/<int:game_id>', views.select_game_service, name='select_game'),
    path('show_game/', views.show_game_service, name='show_game'),
    path('move/', views.move_service, name='move'),
    path('repeat_game/', views.repeat_game_service, name='repeat_game'),
    path('repeat_game/<int:game_id>', views.repeat_game_service, name='repeat_game'),
    path('get_move/', views.get_move_service, name='get_move'),
]

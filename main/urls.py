from django.urls import path
from .views import create_room_view, game_view, home_view, intro_view ,subject_select_modal_view


urlpatterns = [
    path('', intro_view, name='intro'),
    path('home/', home_view, name='home'),
    path('game/', game_view, name='game'),
    path('create-room/', create_room_view, name='create-room'),
    path('game/<str:room_id>/', game_view, name='game'),
    path('subject-select/<uuid:room_id>/', subject_select_modal_view, name='subject_select'),

]
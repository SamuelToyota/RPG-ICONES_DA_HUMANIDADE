from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView, name='home'),
    path('character/<int:pk>/', views.CharacterDetailView, name='character_detail'),
    path('character/novo/', views.CharacterCreateView, name='character_create'),
    path('personagem/<int:pk>/editar/', views.CharacterUpdateView, name='character_update'),
    path('personagem/<int:pk>/deletar/', views.CharacterDeleteView, name='character_delete'),
]
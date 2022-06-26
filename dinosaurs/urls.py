from django.urls import path

from . import views

urlpatterns = [
    path('', views.DinosaurListView.as_view(), name='dinosaur'),
    path('dinosaur/<int:pk>', views.DinosaurDetailView.as_view(), name='dinosaur-detail'),
    path('search/', views.SearchResultsView.as_view(), name='search-results'),
    path('create/', views.DinosaurCreate.as_view(), name='dinosaur-create'),
    path('update/<int:pk>/', views.DinosaurUpdate.as_view(), name='dinosaur-update'),
    path('delete/<int:pk>/', views.DinosaurDelete.as_view(), name='dinosaur-delete'),
    path('favorites/add/<int:dinosaur_id>/', views.add_favorites, name='dinosaur-favorite'),
    path('favorites/', views.FavoritesDinosaurListView.as_view(), name='favorite-dinosaurs')
]

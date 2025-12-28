from django.urls import path

from . import views

urlpatterns = [

    path('',views.HomeView.as_view(),name='home'),

    path('movie-list/',views.MovieListView.as_view(),name='movie-list'),

    path('movie-create/',views.MovieCreateView.as_view(),name='movie-create'),

    path('movie-details/',views.MovieDetailsView.as_view(),name='movie-details'),

    path('movie-details/<str:uuid>/',views.MovieDetailsView.as_view(),name='movie-details'),

    path('movie-edit/<str:uuid>/',views.MovieEditView.as_view(),name='movie-edit'),

    path('movie-delete/<str:uuid>/',views.MovieDeleteView.as_view(),name='movie-delete'),

    path('movie-play/<str:uuid>/',views.PlayMovie.as_view(),name='movie-play'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('train/', views.train_model_view, name='train'),
    path('explanation/', views.explanation, name='explanation'),
]

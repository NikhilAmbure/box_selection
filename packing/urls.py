from django.urls import path
from . import views

urlpatterns = [
    path("recommend-box/", views.recommend_for_payload),
    path("orders/<str:reference>/recommend-box/", views.recommend_for_order),
]

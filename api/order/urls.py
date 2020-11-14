from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'', views.OrderViewSet)

urlpatterns = [
    path('add-order/<str:id>/<str:token>/', views.add_order, name='add-order'),
    path('', include(router.urls)),
]

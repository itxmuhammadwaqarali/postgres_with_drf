from django.urls import path
from .views import ProductListCreateView, ProductRetrieveView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductRetrieveView.as_view(), name='product-detail'),
]

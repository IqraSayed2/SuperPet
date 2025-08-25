from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('product-list',views.ProductList.as_view(),name="product-list"),
    path('<int:pk>',views.ProductDetailView.as_view(),name="product-detail"),
    path('<slug:slug>',views.CategoryDetailView.as_view(),name="category-detail")
]

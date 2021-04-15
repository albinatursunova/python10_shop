"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from product.views import IndexPageView, ProductDetailsView, ProductListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('account.urls')),
    path('', IndexPageView.as_view(), name='index-page'),
    path('products/<slug:category_slug>/', ProductListView.as_view(), name='products-list'),
    path('products/details/<int:pk>/', ProductDetailsView.as_view(), name="product-details"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

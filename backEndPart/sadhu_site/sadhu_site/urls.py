"""
URL configuration for sadhu_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from products.views import ProductDetailView, create_order, engraving_page
from admin_panel.views import login_page, logout_view, edit_site, add_carousel_slide_ajax, delete_carousel

urlpatterns = [
    path('', include('content.urls')),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create-order/', create_order, name='create_order'),
    path('catalog-of-engravings', engraving_page, name='engraving_page'),
    path('admin/crm', login_page, name='login_page'),
    path('admin/crm/edit-site', edit_site, name='edit_site'),
    path('add-slide-ajax/', add_carousel_slide_ajax, name='add_carousel_slide_ajax'),
    path('delete-carousel/', delete_carousel, name='delete_carousel'),
    path('logout', logout_view, name='logout'),
    path('admin/django-admin', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


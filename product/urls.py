from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'products', ProductView)

app_name = 'products'
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('new/', AddProductView.as_view(), name='new_product'),
    path('list_product', list_product, name='list_product'),
    path('list_product/wallpaper/', list_product_wallpaper, name='list_product_wallpaper'),
    path('list_product/artifact/', list_product_artifact, name='list_product_artifact'),
    path('search/', search, name='filter_product'),
    path('index/', index, name='youtube_search'),
    path('<pk>/', product_detail, name='product_detail'),
]


# list of namespace urls for templates:
#     products:new_product
#     products:product_list
#     products:detailed_product
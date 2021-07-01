"""blog_api URL Configuration

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
from rest_framework.routers import DefaultRouter

from main.views import CategoryListView, PostsViewSet, PostImageView, RetrieveViewSet, ListCart, DetailCart, Like, \
    FavoriteList, FavoriteDetail, FavoriteImageView, CorzinaDetailView, CorzinaList, ProfileViewSet

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny





router = DefaultRouter()
router.register('posts', PostsViewSet)
router.register('reviews', RetrieveViewSet)
router.register('favoriterrrrs', Like)
router.register('Profile', ProfileViewSet)



#documen
schema_view = get_schema_view(
    openapi.Info(
        title='My Api',
        default_version='v1',
        description='My ecommerce API'
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('v1/api/categories/', CategoryListView.as_view()),
    path('v1/api/add-image/', PostImageView.as_view()),
    path('v1/api/account/', include('account.urls')),
    path('docs/', schema_view.with_ui('swagger')),
    path('v1/api/', include(router.urls)),
    path('v1/api/carts/', ListCart.as_view()),
    path('v1/api/carts/<int:pk>', DetailCart.as_view()),
    #auth
        path('v1/api/account/auth/', include('rest_framework_social_oauth2.urls')),

    #favorite
    path('v1/api/favorites/', FavoriteList.as_view()),
    path('v1/api/add-favorite/', FavoriteImageView.as_view()),
    #Corzina
    path('v1/api/Corzinas/', CorzinaList.as_view()),
    path('v1/api/add-Corzina/', CorzinaDetailView.as_view()),


    #profile
    # path('v1/api/Profile/', ProfileList.as_view()),
    # path('v1/api/add-Profile/', ProfileDetailView.as_view()),


    path('v1/api/favorites/', FavoriteDetail.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




#TODO:models
#TODO:register/login
#TODO:permission
#TODO:crud
#TODO:Pillow
#TODO:paginassion
#TODO:search
#TODO:filter
#TODO:otzyv
#TODO:chancge password
#TODO:favorite
#TODO:korzina
#TODO:like
#TODO:
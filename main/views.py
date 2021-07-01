from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import action, api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, viewsets, status, mixins, permissions
from rest_framework.reverse import reverse
# from core.permissions import *
from account.models import MyUser
from .models import Category, Post, PostImage, WishList, Review, Cart, Favorite, Corzina, Profile
from .serializers import CategorySerializer, PostSerializer, PostImageSerializer, ReviewSerializer, \
    ProductDetailSerializer, CartSerializer, LkeSerialixer, FavoriteSerializer, CorzinaSerializer, ProfileSerializer
from .permissions import  IsPostAuthor
from django.contrib.auth.models import User

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]

class ProductDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = ProductDetailSerializer



'''сделаем крад на 3 строчек'''
class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):   #----------added
        return {'request':self.request}

    def get_permissions(self):
        """Переопределим данный метод"""
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsPostAuthor, ]
        else:
            permissions = [IsAuthenticated, ]
        return [permission() for permission in permissions]

    # здесь показывает посты которые мы добовляли по дате
    def get_queryset(self):
        queryset = super().get_queryset()
        weeks_count = int(self.request.query_params.get('hours', 0))
        if weeks_count > 0:
            start_date = timezone.now() - timedelta(weeks=weeks_count)
            queryset = queryset.filter(created_at__gte=start_date)
        return queryset

    #здесь показывает посты которые мы добовляли
    @action(detail=False, methods=['get'])
    def my_posts(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])  #для чего нам нужен action -> router builds path posts/search
    def search(self, request, pk=None):
        q            =    request.query_params.get('q')     # request.query_params = request.GET
        queryset     =    self.get_queryset()
        queryset     =    queryset.filter(Q(marka_model__icontains=q)| Q(text__icontains=q)| Q(year__icontains=q) )
        serializer   =    PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
#like
    @action(detail=True, methods=['POST'])
    def like(self, request, pk):
        product = self.get_object()
        user = request.user
        like_obj, created = WishList.objects.get_or_create(product=product, user=user)

        if like_obj.is_liked:
            like_obj.is_liked = False
            like_obj.save()
            return Response('dislike')
        else:
            like_obj.is_liked = True
            like_obj.save()
            return Response('liked')


class PostImageView(generics.ListCreateAPIView):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}

#Cart
class ListCart(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class DetailCart(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

#Отзыв
class RetrieveViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthenticated()]

class Like(viewsets.ReadOnlyModelViewSet):
    queryset = WishList.objects.all()
    serializer_class = LkeSerialixer

#favorite
class FavoriteList(generics.ListCreateAPIView):
    """
    List all favorites
    """
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FavoriteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

class FavoriteImageView(generics.ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_serializer_context(self):
        return {'request': self.request}
#corzina
class CorzinaList(generics.ListCreateAPIView):
    """
    List all favorites
    """
    queryset = Corzina.objects.all()
    serializer_class = CorzinaSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CorzinaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Corzina.objects.all()
    serializer_class = CorzinaSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )



class CorzinaDetailView(generics.ListCreateAPIView):
    queryset = Corzina.objects.all()
    serializer_class = CorzinaSerializer

    def get_serializer_context(self):
        return {'request': self.request}

#profile

class ProfileViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# class ProfileList(generics.ListCreateAPIView):
#     """
#     List all favorites
#     """
#     queryset = Profile.objects.all()
#     serializer_class = Profile
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#
# class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
#
#
#
# class ProfileDetailView(generics.ListCreateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#
#     def get_serializer_context(self):
#         return {'request': self.request}
from django.contrib.auth import get_user_model
from rest_framework import serializers
from account.models import MyUser
from .models import Category, Post, PostImage, Review, Cart, WishList, Favorite, Corzina, Profile

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y', read_only=True)
    class Meta:
        model = Post
        fields = ('id',  'category', 'marka_model', 'created_at', 'text', 'year', 'price', 'probeg', 'karobka', 'color')
    #здесь определяем в каком виде должен отправлять Response
    def to_representation(self, instance):
        representation = super().to_representation(instance) #объект поста
        representation['author']   =  instance.author.email
        representation['images']   =  PostImageSerializer(instance.images.all(), many=True, context=self.context).data
        representation['reviews']  =  ReviewSerializer(instance.reviews.all(), many=True).data
        representation['likes']    =  LkeSerializer(instance.likes.all(), many=True, context=self.context).data

        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        post = Post.objects.create(**validated_data)
        return post

# class LkeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WishList
#         fields = '__all__'
#
#         def to_representation(self, instance):
#             rep = super().to_representation(instance)
#             rep['author'] = ReviewAuthorSerializer(instance.author).data
#             return rep


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
            else:
                url = ''
            return url

    def to_representation(self, instance):
        representations = super().to_representation(instance)
        representations['image'] = self._get_image_url(instance)
        return representations

#Cart
class CartUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class CartSerializer(serializers.ModelSerializer):
    user = CartUserSerializer(read_only=True, many=False)
    post = PostSerializer(read_only=True, many=True)
    class Meta:
        model = Cart
        fields = ('user', 'created_at', 'post')


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

        # здесь likes
    # def get_like(self, instance):
    #     total_like = sum(instance.likes.values_list('likes', flat=True))
    #     likes_count = instance.likes.count()
    #     like = total_like / likes_count if likes_count > 0 else 0
    #     return round(like, 1)


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
        # representation['likes'] = self.get_like(instance)
        representation['rating'] = self.get_rating(instance)

        return representation

# чтобы показать кто оставил отзыв
class ReviewAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            if not instance.first_name and not instance.last_name:
                representation['full'] = 'Анонимный пользователь'
            return representation

class LkeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep['author'] = ReviewAuthorSerializer(instance.author).data
            return rep




class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('id',)

        def validate_product(self, Post):
            request = self.context.get('request')
            if Post.reviews.filter(author=request.user).exists():
                raise serializers.ValidationError('вы не иожете добавить отзыв')
            return Post


        def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep['author'] = ReviewAuthorSerializer(instance.author).data
            return rep

class LkeSerialixer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'

#favorite
class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

#Корзина
class CorzinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corzina
        fields = ('category', 'product', 'added_to')

#profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'Corzina', 'Favorite')

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation['author'] = instance.author.email





# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ('user', 'email')
#

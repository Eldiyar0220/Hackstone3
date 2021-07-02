from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from account.models import MyUser
from model_utils.models import TimeStampedModel
User = get_user_model()

class Category(models.Model):
    slug        =   models.SlugField(max_length=100, primary_key=True)
    name        =   models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author      =   models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts')
    category    =   models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    marka_model =   models.CharField(max_length=255)
    year        =   models.CharField(max_length=255)
    probeg      =   models.CharField(max_length=255)
    karobka     =   models.CharField(max_length=255)
    color       =   models.CharField(max_length=255)
    text        =   models.TextField()
    price       =   models.DecimalField(max_digits=10, decimal_places=2) #это после запятой decimal
    created_at  =   models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.marka_model


class PostImage(models.Model):
    image       =   models.ImageField(upload_to='posts', blank=True, null=True)
    post        =   models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')

#like
class WishList(models.Model):
    user        =    models.ForeignKey(User, on_delete=models.CASCADE,related_name='likes')
    product     =    models.ForeignKey(Post, on_delete=models.CASCADE,related_name='likes')
    #при нажатии лайкает и удаляется
    is_liked    =    models.BooleanField(default=False)


class Cart(models.Model):
    cart_id     =    models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    created_at  =    models.DateTimeField(auto_now_add=True)
    post        =    models.ManyToManyField(Post)

    class Meta:
        ordering = ['cart_id', 'created_at']

    def __str__(self):
        return f'{self.cart_id}'

#otzyv
class Review(models.Model):
    author      =   models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product     =   models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reviews')
    text        =   models.TextField()
    create_at   =   models.DateTimeField(auto_now_add=True)
    update_at   =   models.DateTimeField(auto_now=True)

#favorite
class Favorite(TimeStampedModel):
    product     =   models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')
    text        =   models.CharField(max_length=1000)
    added       =   models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.text

#корзина
class Corzina(models.Model):
    category     =   models.ForeignKey(Category, on_delete=models.CASCADE, related_name='Carzinas')
    product      =   models.ForeignKey(Post, on_delete=models.CASCADE, related_name='Carzinas')
    added_to       =   models.DateTimeField(auto_now_add=True)


#профиль
class Profile(models.Model):
    user            =    models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='Profile')
    Corzina         =    models.ManyToManyField(Corzina)
    Favorite        =    models.ManyToManyField(Favorite)





# class Profile(models.Model):
#     author      =   models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts')
#     email       =   models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts')

from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from rest_framework import serializers
from account.models import MyUser
#TODO: register serializer
from account.utils import send_activation_code
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password           = serializers.CharField(min_length=6,write_only=True)
    password_confirm   = serializers.CharField(min_length=6,write_only=True)
    class Meta:
        model = MyUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Password do not match')
        return validated_data

    def create(self, validate_data):
        email = validate_data.get('email')
        password = validate_data.get('password')
        user = MyUser.objects.create_user(email=email, password=password)
        send_activation_code(email=user.email, activation_code=user.activation_code)
        return user

#TODO: login serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='Password',
        style={'input_type':'password'},
        trim_whitespace=False
    )
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                message = 'unable to log in with provided credentials'
                raise serializers.ValidationError(message, code='authorization')
        else:
            message = 'Must include "email" and "password".'
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs
#TODO: valid


#Reset Password
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError()
        return email
    #просто код скинем
    def send_reset_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_coder()
        # User.send_activation_mail(email, user.activation_code)
        message = f'код для смены пароля {user.activation_code}'
        send_mail(
            'Смены пароля',
            message,
            'test@gmail.com',
            [email]
        )


class CreateNewPasswordSerializer(serializers.Serializer):
    activation_code = serializers.CharField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)

    #check
    def validate_activation_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Неверный код активации')
        return code

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('пароли не совпадают')
        return attrs

    def create_pass(self):
        code = self.validated_data.get('activation-code')
        password = self.validated_data.get('password')
        user = User.objects.get(activation_code=code)
        user.set_password(password)
        user.save()


# 2222
class ChangePasswordSerializer(serializers.Serializer):
    activation_code = serializers.CharField(required=True)
    new_pass = serializers.CharField(min_length=6, required=True)
    new_pass_confirm = serializers.CharField(min_length=6, required=True)

    #здесь проверяем старый пароль
    def validate_old_pass(self, password):
        request = self.context.get('request')
        if request.user.check_password(password):
            raise serializers.ValidationError('введен неправильный пароль')
        return password


    def validate(self, attrs):
        pass_ = attrs.get('new_pass')
        pass_confirm = attrs.get('new_pass_confirm')
        if pass_ != pass_confirm:
            raise serializers.ValidationError('неверное подтверждения')
        return attrs

    def set_new_password(self):
        request = self.context.get('request')
        new_pass = self.validated_data.get('new_pass')
        user = request.user
        user.set_password(new_pass)
        user.save()

#profile

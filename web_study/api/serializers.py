import djoser.serializers

from rest_framework.validators import UniqueTogetherValidator
from users.models import User


class UserSerializer(djoser.serializers.UserSerializer):
    """ Сериализатор пользователя """
    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'balance')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]


class UserCreateSerializer(djoser.serializers.UserCreateSerializer):
    """ Сериализатор создания пользователя """

    class Meta:
        model = User
        fields = (
            'email', 'username', 'password', 'balance')

from rest_framework import serializers
from diary.models import Entry
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .jwtauthentication import JWTAuthentication


class EntrySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Entry
        fields = ('id', 'title', 'entry', 'owner')


class UserSerializer(serializers.ModelSerializer):
    entries = serializers.PrimaryKeyRelatedField(many=True, queryset=Entry.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'entries')


class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        # must set password so that it is properly hashed.
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    def validate(self, attrs):
        credentials = {
            'username': self.initial_data.get('username'),
            'password': self.initial_data.get('password'),
        }

        if all(credentials.values()):
            user = authenticate(**credentials)
            if user:
                payload = {
                    'username': user.username
                }
                return {
                    'token': JWTAuthentication.create_jwt(payload),
                    'user': user
                }
            else:
                raise serializers.ValidationError('Bad credentials')
        else:
            raise serializers.ValidationError('Must provide "username" and "password"')

from diary.models import Entry
from diary.serializers import EntrySerializer, UserSerializer, UserSerializer2, LoginSerializer, EntryListSerializer
from rest_framework import generics, permissions, viewsets, views
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from .permissions import IsOwner
from django.conf import settings


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer2
    model = User


class LoginView(views.APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data={
            'username': request.data['username'],
            'password': request.data['password']
        })
        if serializer.is_valid():
            token = serializer.validated_data.get('token').decode()
            response_data = {'token': token}
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicKeyView(views.APIView):
    def get(self, request, format=None):
        return Response({"public_key":settings.JWT_PUBLIC_KEY.decode()})


class EntryList(generics.ListCreateAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntryListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EntryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = (IsOwner,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

from diary.models import Entry
from diary.serializers import EntrySerializer, UserSerializer, UserSerializer2, LoginSerializer
from rest_framework import generics, permissions, viewsets, views
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .permissions import IsStaffOrTargetUser
from rest_framework import status
from rest_framework.response import Response


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer2
    model = User

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST' or self.request.metnod == 'GET'
                else IsStaffOrTargetUser()),


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


class EntryList(generics.ListCreateAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EntryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

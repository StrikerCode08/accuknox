from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import FriendRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer,FriendRequestSerializer

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    from_user = request.user
    to_user = get_object_or_404(User, username=request.data['username'])
    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        return Response("Friend request already sent", status=status.HTTP_400_BAD_REQUEST)
    friend_request = FriendRequest(from_user=from_user, to_user=to_user)
    friend_request.save()
    return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def respond_to_friend_request(request):
    friend_request = get_object_or_404(FriendRequest, id=request.data['request_id'])
    if friend_request.to_user != request.user:
        return Response("Not authorized", status=status.HTTP_403_FORBIDDEN)
    if request.data['status'] == 'accepted':
        friend_request.status = 'accepted'
        friend_request.save()
    elif request.data['status'] == 'rejected':
        friend_request.status = 'rejected'
        friend_request.save()
    else:
        return Response("Invalid status", status=status.HTTP_400_BAD_REQUEST)
    return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_users_with_friend_requests(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)